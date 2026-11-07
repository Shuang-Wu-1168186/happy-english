import json
from uuid import uuid4

import pytest
from sqlalchemy import select

from app import models as m
from app.services.water_sort import pour
from app.services.water_sort_catalog import manifest
from tests.conftest import sign_in

BASE = "/api/game/v1/water-sort"


@pytest.fixture
def game(client):
    with client.app.state.engine.begin() as db:
        course_id = db.execute(m.learning_course.insert().values(course_code="wordly-wise-1-preview", title="Wordly Wise 1", access_policy="free", is_published=1)).inserted_primary_key[0]
        material_id = db.execute(m.learning_material.insert().values(material_code="wordlywise-3000", material_type="textbook", title="Wordly Wise 1", is_published=1)).inserted_primary_key[0]
        db.execute(m.learning_course_material.insert().values(course_id=course_id, material_id=material_id))
        for lesson in range(1, 16):
            items = [{"item_title": f"{i} · test", "english_text": f"word-{lesson}-{i}",
                      "chinese_text": f"词义{lesson}-{i}", "example_sentence": "An original test sentence."} for i in range(1, 11)]
            db.execute(m.learning_material_lesson.insert().values(material_id=material_id,
                       lesson_code=f"lesson-{lesson}", title=f"Lesson {lesson}", sort_order=lesson,
                       is_published=1, content_status="published",
                       content_json=json.dumps({"source": {"page_kind": "story-words", "source_lesson": lesson}, "items": items})))
    return client, sign_in(client, "learner_test"), course_id


def start(game, number=1, request_id=None, version=7):
    client, headers, _ = game
    return client.post(BASE + "/levels:next", headers=headers, json={
        "level_number": number, "campaign_version": version, "request_id": request_id or str(uuid4())})


def act(game, state, action, **values):
    client, headers, _ = game
    body = {"action": action, "revision": state["revision"], "request_id": str(uuid4()), **values}
    return client.post(BASE + f"/attempts/{state['attempt_id']}/actions", headers=headers, json=body)


def solve(game, state):
    for a, b, amount in manifest(state["board"].get("campaign_version", 7))[state["board"]["level"] - 1]["solution_certificate"]:
        remaining = amount
        while remaining:
            tubes, flags = state["tubes"], state["revealed"]
            available = 0
            for color, visible in zip(reversed(tubes[a]), reversed(flags[a])):
                if not visible or color != tubes[a][-1] or available == state["capacities"][b] - len(tubes[b]):
                    break
                available += 1
            response = act(game, state, "pour", source=a, target=b, amount=available)
            assert response.status_code == 200, response.text
            state = response.json()
            remaining -= available
    return state


def test_login_scope_and_server_words(game):
    client, headers, _ = game
    state = start(game).json()
    assert state["board"]["vocabulary_source"] == "wordly-wise-3000"
    assert all(w["book"] == 1 and w["lesson"] in {1, 2} for w in state["board"]["words"])
    assert len(state["board"]["words"]) == 12
    assert "solution_certificate" not in state["board"]
    assert start(game, 2).status_code == 409
    assert act(game, state, "complete").status_code == 409
    assert act(game, state, "acknowledge", bottle=0).status_code == 409
    assert act(game, state, "challenge").status_code == 409
    other_headers = sign_in(client)
    response = client.post(BASE + f"/attempts/{state['attempt_id']}/actions", headers=other_headers,
                           json={"action": "restart", "revision": 0, "request_id": str(uuid4())})
    assert response.status_code == 404
    client.cookies.clear()
    assert client.get(BASE + "/progress").status_code == 401


def test_moves_retry_completion_eighty_percent_review_and_progress(game):
    state = start(game).json()
    request_id = str(uuid4())
    a, b, amount = manifest()[0]["solution_certificate"][0]
    first = act(game, state, "pour", request_id=request_id, source=a, target=b, amount=amount)
    retry = act(game, state, "pour", request_id=request_id, source=a, target=b, amount=amount)
    assert first.json() == retry.json()
    assert act(game, state, "pour", source=a, target=b, amount=amount).status_code == 409
    # Restart is also server validated.
    state = act(game, first.json(), "restart").json()
    state = solve(game, state)
    response = act(game, state, "complete")
    assert response.status_code == 200
    progress = response.json()["progress"]
    assert progress["completed_levels"] == [1]
    assert len(progress["learned_word_ids"]) == 12
    second = start(game, 2).json()
    roles = [b["word_role"] for b in second["board"]["bottles"]]
    assert roles.count("new") == 3 and roles.count("review") == 12
    assert all(b["word_id"] in progress["learned_word_ids"] for b in second["board"]["bottles"] if b["word_role"] == "review")


def test_server_quiz_no_answers_leaked_and_reward_exactly_once(game):
    state = act(game, solve(game, start(game).json()), "complete").json()
    state = start(game, 2).json()
    state = act(game, state, "challenge").json()
    assert "answer" not in json.dumps(state["challenge"])
    client = game[0]
    question = state["challenge"]["question"]
    with client.app.state.engine.connect() as db:
        raw = db.scalar(select(m.game_water_sort_attempt.c.state_json).where(m.game_water_sort_attempt.c.id == state["attempt_id"]))
    wrong = next(o["option_id"] for o in question["options"] if o["option_id"] != json.loads(raw)["quiz"]["questions"][0]["answer"])
    state = act(game, state, "answer", challenge_id=state["challenge"]["challenge_id"], question_id=question["question_id"], option_id=wrong).json()
    assert state["challenge"]["correct_count"] == 0
    assert state["challenge"]["question"]["question_id"] != question["question_id"]
    for count in range(3):
        question = state["challenge"]["question"]
        with client.app.state.engine.connect() as db:
            raw = db.scalar(select(m.game_water_sort_attempt.c.state_json).where(m.game_water_sort_attempt.c.id == state["attempt_id"]))
        stored = json.loads(raw)["quiz"]["questions"][count]
        assert stored["direction"] == ("english_to_chinese" if count % 2 == 0 else "chinese_to_english")
        old = state
        request_id = str(uuid4())
        values = dict(challenge_id=state["challenge"]["challenge_id"], question_id=question["question_id"], option_id=stored["answer"], request_id=request_id)
        state = act(game, old, "answer", **values).json()
        assert act(game, old, "answer", **values).json() == state
        assert state["challenge"]["correct_count"] == count + 1
    assert len(state["tubes"]) == 16
    assert state["reward"]["word"]["word_id"] in state["progress"]["learned_word_ids"]
    # v7 permits up to three reward bottles in a level, so a second round may begin.
    next_round = act(game, state, "challenge")
    assert next_round.status_code == 200
    state = next_round.json()
    assert state["reward_count"] == 1
    assert act(game, state, "undo").status_code == 409
    restarted = act(game, state, "restart").json()
    assert len(restarted["tubes"]) == 16 and restarted["reward"] == state["reward"]


def test_membership_not_bypassed_by_game(game):
    client, headers, course_id = game
    with client.app.state.engine.begin() as db:
        db.execute(m.learning_course.update().where(m.learning_course.c.id == course_id).values(access_policy="benefit"))
        # Test a legitimately advanced account whose entitlement subsequently expired.
        db.execute(m.game_water_sort_progress.insert().values(user_id=2,
                   state_json=json.dumps({"completed_levels": list(range(1, 9)), "learned_word_ids": []})))
    assert start(game).status_code == 200  # Existing two-lesson preview.
    assert start(game, 8).status_code == 403
    vocab = client.get(BASE + "/vocabulary?book=1", headers=headers).json()
    assert vocab["accessible_words"] == 20 and vocab["total_words"] == 150


def test_hidden_same_color_stops_and_all_810_boards_replay():
    tubes, flags = [["color-0", "color-0"], []], [[False, True], []]
    assert pour(tubes, flags, [4, 4], 0, 1) == 1
    assert flags == [[True], [True]]
    assert pour(tubes, flags, [4, 4], 0, 1) == 1
    for board in manifest():
        tubes = [b["color_layers_bottom_to_top"][:] for b in board["bottles"]]
        flags = [b["revealed"][:] for b in board["bottles"]]
        capacities = [b["capacity"] for b in board["bottles"]]
        for source, target, amount in board["solution_certificate"]:
            while amount > 0:
                amount -= pour(tubes, flags, capacities, source, target, lock_completed=True)
            assert amount == 0
        assert all(not t or len(t) == capacities[i] and len(set(t)) == 1 for i, t in enumerate(tubes))


def test_three_rewards_are_independent_and_restart_keeps_all(game):
    act(game, solve(game, start(game).json()), "complete")
    client, headers, _ = game
    state = client.post(BASE + "/levels:next", headers=headers, json={
        "level_number": 1, "campaign_version": 7, "request_id": str(uuid4())}).json()
    assert len(state["tubes"]) == 12
    for reward in range(1, 4):
        state = act(game, state, "challenge").json()
        assert state["challenge"]["correct_count"] == 0
        for index in range(3):
            with client.app.state.engine.connect() as db:
                raw = db.scalar(select(m.game_water_sort_attempt.c.state_json).where(m.game_water_sort_attempt.c.id == state["attempt_id"]))
            answer = json.loads(raw)["quiz"]["questions"][index]["answer"]
            old = state
            values = dict(challenge_id=state["challenge"]["challenge_id"], question_id=state["challenge"]["question"]["question_id"], option_id=answer, request_id=str(uuid4()))
            state = act(game, old, "answer", **values).json()
            assert act(game, old, "answer", **values).json() == state
        assert state["reward_count"] == reward
        assert len(state["tubes"]) == 12 + reward
    assert act(game, state, "challenge").status_code == 409
    state = act(game, state, "restart").json()
    assert len(state["tubes"]) == 15 and state["reward_count"] == 3


def test_v5_api_rejects_moving_a_completed_bottle_without_mutating_state(game):
    client, headers, _ = game
    state = client.post(BASE + "/levels:next", headers=headers, json={
        "level_number": 1, "campaign_version": 7, "request_id": str(uuid4())}).json()
    state = solve(game, state)
    source = next(i for i, t in enumerate(state["tubes"]) if t)
    target = next(i for i, t in enumerate(state["tubes"]) if not t)
    with client.app.state.engine.connect() as db:
        before = db.scalar(select(m.game_water_sort_attempt.c.state_json).where(m.game_water_sort_attempt.c.id == state["attempt_id"]))
    response = act(game, state, "pour", source=source, target=target, amount=len(state["tubes"][source]))
    assert response.status_code == 409 and "不能再倒出" in response.json()["detail"]
    with client.app.state.engine.connect() as db:
        after = db.scalar(select(m.game_water_sort_attempt.c.state_json).where(m.game_water_sort_attempt.c.id == state["attempt_id"]))
    assert before == after


@pytest.mark.parametrize("capacity", [4, 5])
def test_completed_source_is_locked_for_empty_and_matching_destinations(capacity):
    from fastapi import HTTPException
    for destination in ([], ["red"]):
        tubes = [["red"] * capacity, destination[:]]
        flags = [[True] * capacity, [True] * len(destination)]
        with pytest.raises(HTTPException) as failure:
            pour(tubes, flags, [capacity, capacity], 0, 1, lock_completed=True)
        assert failure.value.status_code == 409
        assert tubes == [["red"] * capacity, destination]
