import json

from fastapi import HTTPException
from sqlalchemy import String, Text, func, or_, select

from app import models as m

RESOURCES = {
    "sentences": m.everyday_sentence,
    "notes": m.english_note,
    "note-items": m.english_note_item,
    "vocabulary": m.vocabulary_library,
    "interviews": m.interview_question,
    "interview-categories": m.interview_category,
    "kids-cards": m.kids_english_card,
    "math-cards": m.math_card,
    "textbook": m.english_textbook_lesson,
    "phonics": m.phonics_lesson,
    "dialogues": m.daily_spoken_dialogue_item,
}


def table_for(resource):
    if resource not in RESOURCES:
        raise HTTPException(404, "Unknown learning module.")
    return RESOURCES[resource]


def visible(table):
    for name in ("is_active", "is_published", "status"):
        if name in table.c:
            return [table.c[name] == 1]
    return []


def content_order(table):
    if table is m.english_note:
        return [table.c.note_date.desc(), table.c.id.desc()]
    return [
        table.c[name]
        for name in (
            "priority_order",
            "sort_order",
            "unit_order",
            "lesson_order",
            "section_order",
            "item_order",
        )
        if name in table.c
    ] + [table.c.id]


def serialise(row):
    result = dict(row)
    for key, value in list(result.items()):
        if key.endswith("_json"):
            try:
                result[key.removesuffix("_json")] = json.loads(value or "[]")
            except (ValueError, TypeError):
                result[key.removesuffix("_json")] = []
    return result


class ContentRepository:
    def __init__(self, db):
        self.db = db

    def list(self, resource, q="", category="", parent_id=None, page=1, page_size=20):
        table = table_for(resource)
        conditions = visible(table)
        if q:
            conditions.append(
                or_(*(c.ilike(f"%{q}%") for c in table.c if isinstance(c.type, (String, Text))))
            )
        if category:
            field = next(
                (
                    name
                    for name in ("category", "tag", "category_id", "unit_name", "lesson_code")
                    if name in table.c
                ),
                None,
            )
            if field:
                conditions.append(table.c[field] == category)
        if parent_id is not None and "note_id" in table.c:
            conditions.append(table.c.note_id == parent_id)
        total = self.db.scalar(select(func.count()).select_from(table).where(*conditions))
        rows = self.db.execute(
            select(table)
            .where(*conditions)
            .order_by(*content_order(table))
            .offset((page - 1) * page_size)
            .limit(page_size)
        ).mappings()
        return {
            "items": [serialise(row) for row in rows],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        }

    def get(self, resource, item_id):
        table = table_for(resource)
        row = self.db.execute(select(table).where(table.c.id == item_id, *visible(table))).mappings().first()
        if not row:
            raise HTTPException(404, "Content not found.")
        result = serialise(row)
        order = content_order(table)
        conditions = visible(table)
        if resource == "note-items":
            conditions.append(table.c.note_id == result["note_id"])
        navigation = (
            select(
                table.c.id,
                func.lag(table.c.id).over(order_by=order).label("previous_id"),
                func.lead(table.c.id).over(order_by=order).label("next_id"),
            )
            .where(*conditions)
            .subquery()
        )
        neighbors = self.db.execute(select(navigation).where(navigation.c.id == item_id)).mappings().one()
        result.update(previous_id=neighbors["previous_id"], next_id=neighbors["next_id"])
        children = {
            "kids-cards": [
                ("examples", m.kids_english_card_example, "card_id"),
                ("sound_parts", m.kids_english_card_sound_part, "card_id"),
                ("word_family", m.kids_english_card_word_family, "card_id"),
            ],
            "interviews": [("sections", m.interview_answer_section, "question_id")],
            "textbook": [("sentences", m.english_textbook_sentence, "lesson_id")],
            "notes": [("items", m.english_note_item, "note_id")],
        }
        for key, child, foreign_key in children.get(resource, []):
            order = [
                child.c[name]
                for name in ("sort_order", "priority_order", "part_order", "sentence_order", "item_order")
                if name in child.c
            ]
            rows = self.db.execute(
                select(child)
                .where(child.c[foreign_key] == item_id, *visible(child))
                .order_by(*order, child.c.id)
            ).mappings()
            result[key] = [serialise(row) for row in rows]
        return result
