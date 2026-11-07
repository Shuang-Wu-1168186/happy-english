"""Wordly Wise words come from published textbook lessons, never client fixtures."""

import json
from functools import lru_cache
from pathlib import Path
import re

from fastapi import HTTPException
from sqlalchemy import select

from app import models as m
from app.services.membership import LearningUserCourseService

DATA = Path(__file__).resolve().parents[1] / "data" / "water_sort"


@lru_cache(maxsize=1)
def manifest(version=7):
    if version != 7:
        raise HTTPException(422, "请更新游戏版本后继续。")
    filename = "campaign-810-v7.json"
    return json.loads((DATA / filename).read_text())["levels"]


@lru_cache(maxsize=1)
def translations():
    return json.loads((DATA / "translations.json").read_text())["words"]


def extract_words(rows):
    words = []
    for row in rows:
        content = json.loads(row["content_json"] or "{}")
        source = content.get("source", {})
        if source.get("page_kind") not in {"story-words", "word-list"}:
            continue
        book = 1 if row["material_code"] == "wordlywise-3000" else int(row["material_code"].rsplit("-", 1)[1])
        lesson = int(source["source_lesson"])
        for item in content.get("items", []):
            match = re.match(r"^(\d+)\s*·", item.get("item_title", ""))
            if not match:
                continue
            index = int(match[1])
            word = item["english_text"].strip()
            supplement = translations().get(word.casefold(), {})
            chinese = item.get("chinese_text") or supplement.get("translation", "")
            if not chinese:
                raise HTTPException(503, "教材词条缺少中文释义，请稍后重试。")
            # Original examples are retained; never manufacture a textbook attribution.
            paragraphs = [p.strip() for p in item.get("source_text", "").split("\n\n") if p.strip()]
            example = item.get("example_sentence") or (paragraphs[1] if len(paragraphs) > 1 else "")
            words.append({
                "word_id": f"ww-b{book:02}-l{lesson:02}-w{index:02}",
                "word": word, "translation": chinese, "example_sentence": example,
                "book": book, "lesson": lesson, "word_order": index,
                "translation_source": "course_content" if item.get("chinese_text") else supplement["source"],
                "_lesson_id": row["id"], "_material_id": row["material_id"],
            })
    words.sort(key=lambda w: (w["book"], w["lesson"], w["word_order"]))
    if len({w["word_id"] for w in words}) != len(words):
        raise HTTPException(503, "教材词条编号重复，请稍后重试。")
    return words


def public_word(word):
    return {key: value for key, value in word.items() if not key.startswith("_")}


class WaterSortCatalog:
    def __init__(self, db, user):
        self.db, self.user = db, user
        lesson, material = m.learning_material_lesson, m.learning_material
        rows = db.execute(
            select(lesson.c.id, lesson.c.material_id, lesson.c.content_json, material.c.material_code)
            .join(material, lesson.c.material_id == material.c.id)
            .where(material.c.material_code.in_(["wordlywise-3000"] + [f"wordlywise-3000-book-{n}" for n in range(2, 13)]),
                   material.c.is_published == 1, lesson.c.is_published == 1,
                   lesson.c.content_status == "published")
        ).mappings().all()
        self.words = extract_words(rows)
        self.by_id = {w["word_id"]: w for w in self.words}
        self.access = LearningUserCourseService(db)
        self._allowed = {}

    def allowed(self, word):
        material_id = word["_material_id"]
        if material_id not in self._allowed:
            # Reuse the same membership and topic-wide two-lesson preview as the main app.
            access = self.access.material_access(self.user, material_id)
            if access["access_state"] == "available":
                self._allowed[material_id] = None
            else:
                lessons = self.access.catalog.material_lessons.dao.list_lessons(material_id)
                self._allowed[material_id] = {
                    lessons[i]["id"] for i in (access.get("unlocked_lesson_indexes") or [])
                }
        allowed = self._allowed[material_id]
        return allowed is None or word["_lesson_id"] in allowed

    def require(self, ids):
        for word_id in ids:
            word = self.by_id.get(word_id)
            if word is None:
                raise HTTPException(503, "这关的教材词条暂不可用，请稍后重试。")
            if not self.allowed(word):
                raise HTTPException(403, "本关包含会员教材词汇，请使用已开通 Wordly Wise 权限的账号。")

    def level(self, number, version=7):
        board = json.loads(json.dumps(manifest(version)[number - 1]))
        assigned = []
        for bottle in board["bottles"]:
            # Versioned IDs are fixed at release time; editing another textbook
            # must not silently reassign every later bottle's learned word.
            assigned.append(bottle["word_id"])
        self.require(assigned)
        board.pop("solution_certificate", None)
        board["words"] = [public_word(self.by_id[key]) for key in dict.fromkeys(assigned)]
        board["vocabulary_source"] = "wordly-wise-3000"
        board["campaign_version"] = version
        return board
