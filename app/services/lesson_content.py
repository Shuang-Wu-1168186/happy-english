"""Generic lesson content sections and publication validation."""

import json

from fastapi import HTTPException
from sqlalchemy import func, select

from app import models as m
from app import schemas as s
from app.dao.lesson_content import (
    LearningLessonItemDAO,
    LearningLessonSectionDAO,
)


SECTION_RULES = {
    "core_vocabulary": {"min": 4, "max": 6},
    "situational_dialogues": {"min": 6, "max": 8},
    "key_sentence_patterns": {"min": 3, "max": 5},
    "speaking_practice": {"min": 1, "max": None},
    "mini_exercises": {"min": 1, "max": None},
    "useful_tips": {"min": 1, "max": None},
    "extended_reading": {"min": 1, "max": None},
}

SECTION_DEFAULTS = {
    "core_vocabulary": ("核心词汇", "Core Vocabulary", 10),
    "situational_dialogues": ("情景对话", "Situational Dialogues", 20),
    "key_sentence_patterns": ("核心句型", "Key Sentence Patterns", 30),
    "speaking_practice": ("口语练习", "Speaking Practice", 40),
    "mini_exercises": ("小练习", "Mini Exercises", 50),
    "useful_tips": ("实用表达提示", "Useful Tips", 60),
    "extended_reading": ("扩展阅读", "Extended Reading", 70),
}


def _decode(value, fallback):
    if value is None:
        return fallback
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError) as error:
        raise HTTPException(500, "Stored lesson content is invalid.") from error


def serialise_item(row):
    result = dict(row)
    result["payload"] = _decode(result.pop("payload_json"), {})
    return result


class GenericLessonContentService:
    """Own the reusable seven-section lesson format."""

    required_sections = frozenset(SECTION_RULES)

    def __init__(self, db):
        self.db = db
        self.sections = LearningLessonSectionDAO(db)
        self.items = LearningLessonItemDAO(db)

    def require_lesson(self, lesson_id):
        lesson = self.db.execute(
            select(m.learning_material_lesson).where(m.learning_material_lesson.c.id == lesson_id)
        ).mappings().first()
        if not lesson:
            raise HTTPException(404, "Learning material lesson not found.")
        return lesson

    def list_for_lesson(self, lesson_id, published_only=False, include_items=True):
        self.require_lesson(lesson_id)
        result = []
        for section in self.sections.list_for_lesson(lesson_id, published_only):
            items = self.items.list_for_section(section["id"], published_only)
            entry = {**dict(section), "item_count": len(items)}
            if include_items:
                entry["items"] = [serialise_item(item) for item in items]
            result.append(entry)
        return result

    @classmethod
    def validate_sections(cls, sections, require_complete=False):
        codes = [section.section_code for section in sections]
        if len(codes) != len(set(codes)):
            raise HTTPException(422, "Each lesson section can only be configured once.")
        if require_complete and set(codes) != cls.required_sections:
            missing = sorted(cls.required_sections - set(codes))
            raise HTTPException(422, f"The lesson is missing required sections: {', '.join(missing)}.")
        for section in sections:
            rule = SECTION_RULES[section.section_code]
            count = len(section.items)
            if section.status == "published" or require_complete:
                if count < rule["min"] or (rule["max"] is not None and count > rule["max"]):
                    maximum = rule["max"] if rule["max"] is not None else "以上"
                    raise HTTPException(
                        422,
                        f"{section.section_code} requires {rule['min']}-{maximum} items.",
                    )
            item_codes = [item.item_code for item in section.items]
            if len(item_codes) != len(set(item_codes)):
                raise HTTPException(422, f"{section.section_code} contains duplicate item codes.")

    def replace(self, lesson_id, payload: s.LearningLessonSectionsInput, actor, publish=False):
        lesson = self.require_lesson(lesson_id)
        self.validate_sections(payload.sections, require_complete=publish)
        if lesson["lesson_format"] == "courseware":
            raise HTTPException(409, "Courseware lessons must use the courseware block editor.")

        self.sections.delete_where(self.sections.table.c.lesson_id == lesson_id)
        for section in payload.sections:
            defaults = SECTION_DEFAULTS[section.section_code]
            section_id = self.sections.insert(
                {
                    "lesson_id": lesson_id,
                    "section_code": section.section_code,
                    "title": section.title or defaults[0],
                    "title_en": section.title_en or defaults[1],
                    "sort_order": section.sort_order or defaults[2],
                    "status": "published" if publish else section.status,
                    "created_by": actor["id"],
                    "updated_by": actor["id"],
                }
            )
            for item in section.items:
                self.items.insert(
                    {
                        "section_id": section_id,
                        "item_code": item.item_code,
                        "item_order": item.item_order,
                        "title": item.title or None,
                        "payload_json": json.dumps(
                            item.payload, ensure_ascii=False, separators=(",", ":")
                        ),
                        "status": "published" if publish else item.status,
                        "created_by": actor["id"],
                        "updated_by": actor["id"],
                    }
                )
        updates = {
            "lesson_schema_version": 2,
            "content_status": "published" if publish else "draft",
            "is_published": 1 if publish else 0,
            "updated_by": actor["id"],
        }
        if publish:
            updates["published_at"] = func.now()
            self.db.execute(
                m.learning_material_lesson.update()
                .where(m.learning_material_lesson.c.id == lesson_id)
                .values(**updates)
            )
        else:
            self.db.execute(
                m.learning_material_lesson.update()
                .where(m.learning_material_lesson.c.id == lesson_id)
                .values(**updates)
            )
        self.db.commit()
        return {"lesson_id": lesson_id, "sections": self.list_for_lesson(lesson_id)}

    def publish(self, lesson_id, actor):
        lesson = self.require_lesson(lesson_id)
        if lesson["lesson_format"] == "courseware":
            raise HTTPException(409, "Courseware lessons must use the courseware block editor.")
        sections = self.sections.list_for_lesson(lesson_id, published_only=False)
        codes = {section["section_code"] for section in sections}
        if codes != self.required_sections:
            missing = sorted(self.required_sections - codes)
            raise HTTPException(422, f"The lesson is missing required sections: {', '.join(missing)}.")
        for section in sections:
            rule = SECTION_RULES[section["section_code"]]
            items = self.items.list_for_section(section["id"], published_only=False)
            count = len(items)
            if count < rule["min"] or (rule["max"] is not None and count > rule["max"]):
                maximum = rule["max"] if rule["max"] is not None else "以上"
                raise HTTPException(
                    422,
                    f"{section['section_code']} requires {rule['min']}-{maximum} items.",
                )
            self.db.execute(
                self.items.table.update()
                .where(self.items.table.c.section_id == section["id"])
                .values(status="published", updated_by=actor["id"])
            )
            self.db.execute(
                self.sections.table.update()
                .where(self.sections.table.c.id == section["id"])
                .values(status="published", updated_by=actor["id"])
            )
        self.db.execute(
            m.learning_material_lesson.update()
            .where(m.learning_material_lesson.c.id == lesson_id)
            .values(
                lesson_schema_version=2,
                content_status="published",
                is_published=1,
                published_at=func.now(),
                updated_by=actor["id"],
            )
        )
        self.db.commit()
        return {"lesson_id": lesson_id, "sections": self.list_for_lesson(lesson_id)}


LESSON_CONTENT_TABLE_SERVICE_TYPES = {
    "learning_lesson_section": GenericLessonContentService,
    "learning_lesson_item": GenericLessonContentService,
}
