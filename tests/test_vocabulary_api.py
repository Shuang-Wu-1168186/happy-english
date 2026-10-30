from datetime import UTC, datetime, timedelta

from app import models as m
from tests.conftest import opaque_id, sign_in


def _seed_vocabulary_card(client):
    with client.app.state.engine.begin() as connection:
        deck_id = connection.execute(
            m.vocabulary_deck.insert().values(
                deck_code="software-english-api",
                title="技术英语（软件开发）",
                title_en="Software Development English",
                description="软件开发中常见的核心表达。",
                category="技术英语",
                difficulty_code="B1",
                sort_order=10,
                is_published=1,
            )
        ).inserted_primary_key[0]
        word_id = connection.execute(
            m.vocabulary_word.insert().values(
                word="refine",
                normalized_word="refine",
                phonetic_uk="/rɪˈfaɪn/",
                phonetic_us="/rɪˈfaɪn/",
                word_level="B1",
                is_active=1,
            )
        ).inserted_primary_key[0]
        sense_id = connection.execute(
            m.vocabulary_word_sense.insert().values(
                word_id=word_id,
                part_of_speech="verb",
                translation="完善；提炼",
                definition="通过小幅调整，让内容或方案变得更好。",
                memory_hint="反复打磨，让内容更精细。",
                sort_order=1,
            )
        ).inserted_primary_key[0]
        connection.execute(
            m.vocabulary_word_example.insert().values(
                sense_id=sense_id,
                english_text="We need to refine the design before launch.",
                chinese_text="我们需要在上线前完善这个设计。",
                sort_order=1,
            )
        )
        card_id = connection.execute(
            m.vocabulary_deck_word.insert().values(
                deck_id=deck_id,
                word_id=word_id,
                sort_order=10,
                is_enabled=1,
            )
        ).inserted_primary_key[0]
    return deck_id, word_id, card_id


def test_vocabulary_memory_api_exposes_cards_and_persists_reviews(client):
    deck_id, word_id, card_id = _seed_vocabulary_card(client)
    assert client.get("/api/learning/vocabulary/decks").status_code == 401

    headers = sign_in(client, "learner_test")
    deck_token = opaque_id(client, deck_id)
    card_token = opaque_id(client, card_id)

    assert client.get(f"/api/learning/vocabulary/decks/{deck_id}", headers=headers).status_code == 422

    decks = client.get("/api/learning/vocabulary/decks", headers=headers)
    assert decks.status_code == 200
    deck = decks.json()["items"][0]
    assert deck["id"] == deck_token
    assert deck["deck_code"] == "software-english-api"
    assert deck["word_count"] == 1
    assert deck["started_count"] == 0
    assert deck["mastered_count"] == 0

    detail = client.get(f"/api/learning/vocabulary/decks/{deck_token}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["deck"]["id"] == deck_token
    assert detail.json()["summary"] == {
        "total_count": 1,
        "started_count": 0,
        "mastered_count": 0,
        "marked_count": 0,
    }
    progress = client.get(
        f"/api/learning/vocabulary/decks/{deck_token}/progress",
        headers=headers,
    )
    assert progress.status_code == 200
    assert progress.json()["summary"]["total_count"] == 1

    cards = client.get(f"/api/learning/vocabulary/decks/{deck_token}/cards", headers=headers)
    assert cards.status_code == 200
    card = cards.json()["items"][0]
    assert card["card_id"] == card_token
    assert card["word"]["id"] == opaque_id(client, word_id)
    assert card["sense"]["translation"] == "完善；提炼"
    assert card["example"]["english_text"] == "We need to refine the design before launch."
    assert card["progress"] is None

    word = client.get(
        f"/api/learning/vocabulary/words/{opaque_id(client, word_id)}",
        headers=headers,
    )
    assert word.status_code == 200
    assert word.json()["word"]["word"] == "refine"
    assert word.json()["senses"][0]["examples"][0]["chinese_text"] == "我们需要在上线前完善这个设计。"

    review = client.post(
        f"/api/learning/vocabulary/cards/{card_token}/reviews",
        headers=headers,
        json={"rating": "review", "duration_millis": 1500},
    )
    assert review.status_code == 200
    assert review.json()["card_id"] == card_token
    assert review.json()["progress"]["learning_state"] == "review"
    assert review.json()["progress"]["mastery_level"] == 1
    assert review.json()["summary"]["started_count"] == 1

    marked = client.put(
        f"/api/learning/vocabulary/cards/{card_token}/mark",
        headers=headers,
        json={"is_marked": True},
    )
    assert marked.status_code == 200
    assert marked.json()["progress"]["is_marked"] is True
    assert marked.json()["summary"]["marked_count"] == 1

    history = client.get(
        f"/api/learning/vocabulary/cards/{card_token}/review-history",
        headers=headers,
    )
    assert history.status_code == 200
    assert history.json()["items"][0]["rating"] == "review"
    assert history.json()["items"][0]["duration_millis"] == 1500

    with client.app.state.engine.begin() as connection:
        connection.execute(
            m.user_vocabulary_progress.update()
            .where(
                m.user_vocabulary_progress.c.user_id == 2,
                m.user_vocabulary_progress.c.deck_word_id == card_id,
            )
            .values(
                next_review_at=datetime.now(UTC).replace(tzinfo=None) - timedelta(seconds=1),
                is_marked=0,
            )
        )
    due = client.get(
        f"/api/learning/vocabulary/decks/{deck_token}/review-cards",
        headers=headers,
    )
    assert due.status_code == 200
    assert [item["card_id"] for item in due.json()["items"]] == [card_token]

    assert (
        client.post(
            f"/api/learning/vocabulary/cards/{card_token}/reviews",
            headers=headers,
            json={"rating": "unknown"},
        ).status_code
        == 422
    )
    assert (
        client.post(
            f"/api/learning/vocabulary/cards/{card_id}/reviews",
            headers=headers,
            json={"rating": "review"},
        ).status_code
        == 422
    )
