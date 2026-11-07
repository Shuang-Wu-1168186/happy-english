"""Authoritative, idempotent moves, vocabulary acknowledgements and bottle rewards."""

from copy import deepcopy
import hashlib
import json
import random
import secrets
from uuid import uuid4

from fastapi import HTTPException

from app.dao.water_sort import WaterSortAttemptDAO, WaterSortProgressDAO
from app.services.water_sort_catalog import WaterSortCatalog


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def full(tube, capacity):
    return len(tube) == capacity and len(set(tube)) == 1


def pour(tubes, revealed, capacities, source, target, lock_completed=False):
    if source == target or not (0 <= source < len(tubes) and 0 <= target < len(tubes)):
        raise HTTPException(422, "请选择两支不同的瓶子。")
    a, b = tubes[source], tubes[target]
    if lock_completed and full(a, capacities[source]):
        raise HTTPException(409, "这瓶已装满同色水，不能再倒出。")
    if not a or len(b) >= capacities[target] or (b and a[-1] != b[-1]):
        raise HTTPException(409, "只能倒进空瓶或相同颜色的水上。")
    amount = 0
    for color, visible in zip(reversed(a), reversed(revealed[source])):
        if color != a[-1] or not visible or amount >= capacities[target] - len(b):
            break
        amount += 1
    if amount == 0:
        raise HTTPException(409, "瓶口水层尚未显色。")
    b.extend(a[-amount:])
    del a[-amount:]
    revealed[target].extend(revealed[source][-amount:])
    del revealed[source][-amount:]
    for index, tube in enumerate(tubes):
        if tube:
            revealed[index][-1] = True
        if full(tube, capacities[index]):
            revealed[index] = [True] * len(tube)
    return amount


class WaterSortProgressService:
    dao_type = WaterSortProgressDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)

    def get(self, user):
        row = self.dao.for_user(user["id"])
        return json.loads(row["state_json"]) if row else {"completed_levels": [], "learned_word_ids": []}

    def save(self, user, progress):
        row = self.dao.for_user(user["id"])
        if row:
            self.dao.update(row["id"], {"state_json": encode(progress)})
        else:
            self.dao.insert({"user_id": user["id"], "state_json": encode(progress)})


class WaterSortService:
    dao_type = WaterSortAttemptDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)
        self.progress = WaterSortProgressService(db)

    @staticmethod
    def create_quiz(catalog, progress):
        """Create a fresh three-question streak from the learner's entire history."""
        pool = [catalog.by_id[key] for key in progress["learned_word_ids"]
                if key in catalog.by_id and catalog.allowed(catalog.by_id[key])]
        unique, spellings, meanings = [], set(), set()
        for word in pool:
            if word["word"].casefold() not in spellings and word["translation"] not in meanings:
                unique.append(word)
                spellings.add(word["word"].casefold())
                meanings.add(word["translation"])
        if len(unique) < 3:
            raise HTTPException(409, "先学会至少 3 个不同单词，再答题解锁空瓶。")
        rng = random.SystemRandom()
        targets = rng.sample(unique, 3)
        questions = []
        for index, word in enumerate(targets):
            options = rng.sample([w for w in unique if w != word], min(3, len(unique) - 1)) + [word]
            rng.shuffle(options)
            direction = "english_to_chinese" if index % 2 == 0 else "chinese_to_english"
            answer = ""
            choices = []
            for option in options:
                option_id = secrets.token_urlsafe(12)
                choices.append({"option_id": option_id, "label": option["translation"] if index % 2 == 0 else option["word"]})
                if option == word:
                    answer = option_id
            questions.append({"question_id": str(uuid4()), "direction": direction,
                              "prompt": f"“{word['word']}” 的中文含义是？" if index % 2 == 0 else f"“{word['translation']}” 对应哪个英文单词？",
                              "options": choices, "answer": answer})
        return {"challenge_id": str(uuid4()), "correct_count": 0, "questions": questions,
                "bonus_word": {k: v for k, v in targets[0].items() if not k.startswith("_")}}

    def start(self, user, number, request_id, version=7):
        self.progress.dao.lock_user(user["id"])
        # The client-generated UUID is also the idempotency key for level creation.
        existing = self.dao.for_user(request_id, user["id"])
        if existing:
            if existing["level_number"] != number:
                raise HTTPException(409, "请求编号已用于其他关卡。")
            state = json.loads(existing["state_json"])
            WaterSortCatalog(self.db, user).require([w["word_id"] for w in state["board"]["words"]])
            return self.response(state, self.progress.get(user))
        progress = self.progress.get(user)
        unlocked = next((n for n in range(1, 811) if n not in progress["completed_levels"]), 810)
        if number > unlocked:
            raise HTTPException(409, "请先完成前面的关卡。")
        board = WaterSortCatalog(self.db, user).level(number, version)
        state = {
            "attempt_id": request_id, "revision": 0, "board": board,
            "tubes": [b["color_layers_bottom_to_top"][:] for b in board["bottles"]],
            "revealed": [b["revealed"][:] for b in board["bottles"]],
            "capacities": [b["capacity"] for b in board["bottles"]],
            "history": [], "acknowledged": [], "reward": None, "rewards": [], "reward_limit": 3 if version >= 3 else 1, "quiz": None,
            "completed": False, "requests": {},
        }
        self.dao.insert({"id": request_id, "user_id": user["id"], "level_number": number, "state_json": encode(state)})
        self.db.commit()
        return self.response(state, progress)

    @staticmethod
    def response(state, progress, **extra):
        quiz = state["quiz"]
        question = None
        if quiz and quiz["correct_count"] < 3:
            current = quiz["questions"][quiz["correct_count"]]
            question = {key: current[key] for key in ("question_id", "direction", "prompt", "options")}
        return {
            "attempt_id": state["attempt_id"], "revision": state["revision"],
            "board": state["board"], "tubes": state["tubes"], "revealed": state["revealed"],
            "capacities": state["capacities"], "completed": state["completed"],
            "reward": state["reward"], "reward_count": len(state.get("rewards", [state["reward"]] if state["reward"] else [])), "progress": progress,
            "challenge": ({"challenge_id": quiz["challenge_id"], "correct_count": quiz["correct_count"],
                           "question": question} if quiz else None),
            **extra,
        }

    def action(self, user, attempt_id, data):
        self.progress.dao.lock_user(user["id"])
        row = self.dao.for_user(attempt_id, user["id"])
        if not row:
            raise HTTPException(404, "找不到这次挑战，请重新进入关卡。")
        state = json.loads(row["state_json"])
        state.setdefault("rewards", [state["reward"]] if state["reward"] else [])
        catalog = WaterSortCatalog(self.db, user)
        catalog.require([w["word_id"] for w in state["board"]["words"]])
        progress = self.progress.get(user)
        fingerprint = hashlib.sha256(encode(data.model_dump(mode="json")).encode()).hexdigest()
        request_id = str(data.request_id)
        previous = state["requests"].get(request_id)
        if previous:
            if previous["fingerprint"] != fingerprint:
                raise HTTPException(409, "请求编号不能用于不同操作。")
            return self.response(state, progress, **previous["result"])
        if data.revision != state["revision"]:
            raise HTTPException(409, "关卡状态已变化，请返回地图重新进入。")
        if state["completed"]:
            raise HTTPException(409, "本次挑战已完成，请返回地图。")
        result = {}
        kind = data.action
        if kind == "pour":
            before = deepcopy([state["tubes"], state["revealed"]])
            amount = pour(state["tubes"], state["revealed"], state["capacities"], data.source, data.target,
                          lock_completed=state["board"].get("campaign_version", 2) >= 5)
            if amount != data.amount:
                raise HTTPException(409, "倒水数量与服务器不一致，请重新进入关卡。")
            state["history"] = (state["history"] + [before])[-200:]
            result["amount"] = amount
        elif kind == "undo":
            if not state["history"]:
                raise HTTPException(409, "没有可以撤回的操作。")
            state["tubes"], state["revealed"] = state["history"].pop()
        elif kind == "restart":
            state["tubes"] = [b["color_layers_bottom_to_top"][:] for b in state["board"]["bottles"]]
            state["revealed"] = [b["revealed"][:] for b in state["board"]["bottles"]]
            for _ in state["rewards"]:
                state["tubes"].append([])
                state["revealed"].append([])
            state["history"], state["acknowledged"] = [], []
        elif kind == "acknowledge":
            index = data.bottle
            if not 0 <= index < len(state["tubes"]) or not full(state["tubes"][index], state["capacities"][index]):
                raise HTTPException(409, "装满同色水后才能学习这支瓶子的单词。")
            word_id = (state["board"]["bottles"][index]["word_id"] if index < len(state["board"]["bottles"])
                       else state["rewards"][index - len(state["board"]["bottles"])]["word"]["word_id"])
            progress["learned_word_ids"] = sorted(set(progress["learned_word_ids"]) | {word_id})
            state["acknowledged"] = sorted(set(state["acknowledged"]) | {index})
        elif kind == "complete":
            if not all(not tube or full(tube, state["capacities"][i]) for i, tube in enumerate(state["tubes"])):
                raise HTTPException(409, "请先完成彩水排序。")
            progress["learned_word_ids"] = sorted(set(progress["learned_word_ids"]) | {
                b["word_id"] for b in state["board"]["bottles"]})
            progress["completed_levels"] = sorted(set(progress["completed_levels"]) | {row["level_number"]})
            state["completed"] = True
            state["history"] = []
        elif kind == "challenge":
            if len(state["rewards"]) >= state.get("reward_limit", 1):
                raise HTTPException(409, "本关奖励空瓶已达上限。")
            if not state["quiz"] or state["quiz"]["correct_count"] == 3:
                state["quiz"] = self.create_quiz(catalog, progress)
        elif kind == "answer":
            quiz = state["quiz"]
            if not quiz or quiz["correct_count"] >= 3 or data.challenge_id != quiz["challenge_id"]:
                raise HTTPException(409, "这次空瓶挑战已结束。")
            question = quiz["questions"][quiz["correct_count"]]
            if data.question_id != question["question_id"] or data.option_id not in {o["option_id"] for o in question["options"]}:
                raise HTTPException(409, "题目已更新，请重新作答。")
            correct = secrets.compare_digest(data.option_id, question["answer"])
            result["correct"] = correct
            if correct:
                quiz["correct_count"] += 1
            else:
                # A mistake resets the streak and returns a new first question.
                # The old question ID becomes invalid, so stale taps cannot count.
                state["quiz"] = quiz = self.create_quiz(catalog, progress)
            if quiz["correct_count"] == 3:
                state["reward"] = {"reward_id": str(uuid4()), "bottle_id": "bonus", "capacity": 4, "word": quiz["bonus_word"]}
                state["reward"]["bottle_id"] = f"bonus-{len(state['rewards']) + 1}"
                state["rewards"].append(state["reward"])
                state["tubes"].append([])
                state["revealed"].append([])
                state["capacities"].append(4)
                state["history"] = []
        state["revision"] += 1
        state["requests"][request_id] = {"fingerprint": fingerprint, "result": result}
        # Bounded state; stale retries outside this window fail revision validation safely.
        state["requests"] = dict(list(state["requests"].items())[-32:])
        self.dao.update(attempt_id, {"state_json": encode(state)})
        self.progress.save(user, progress)
        self.db.commit()
        return self.response(state, progress, **result)


WATER_SORT_TABLE_SERVICE_TYPES = {
    "game_water_sort_progress": WaterSortProgressService,
    "game_water_sort_attempt": WaterSortService,
}
