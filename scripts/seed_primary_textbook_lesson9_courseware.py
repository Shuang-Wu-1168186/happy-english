#!/usr/bin/env python3
"""Publish one reviewable interactive courseware lesson for primary textbook Lesson 9.

The source lesson remains in the original textbook reader.  This script creates
a separate, free preview material in the same textbook topic so the new
courseware experience can be reviewed without changing the reader learners
already use.

Run locally or on the application server with:

    PYTHONPATH=. .venv/bin/python scripts/seed_primary_textbook_lesson9_courseware.py
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from sqlalchemy import delete, func, select, update
from sqlalchemy.engine import Connection, Engine

from app import models as m
from app.core.config import Settings
from app.core.database import make_engine


TOPIC_CODE = "english-textbook"
TEMPLATE_CODE = "put-aside"
TEMPLATE_VERSION = 1
MATERIAL_CODE = "primary-textbook-courseware-preview"
COURSE_CODE = "primary-textbook-courseware-preview-course"
LESSON_CODE = "unit-03-lesson-09-technology-communication"
SOURCE_UNIT_NAME = "Unit 3"
SOURCE_LESSON_NAME = "Lesson 9"


@dataclass(frozen=True)
class CoursewareBlock:
    block_code: str
    block_type: str
    title: str | None
    payload: dict
    sort_order: int
    source_sentence_orders: tuple[int, ...]


BLOCKS = (
    CoursewareBlock(
        block_code="hero",
        block_type="hero",
        title=None,
        sort_order=10,
        source_sentence_orders=(19,),
        payload={
            "eyebrow": "UNIT 3 · LESSON 9 · READING & SPEAKING",
            "phrase": "Technology Is Changing Our Communication",
            "meaning": "科技正在改变我们的沟通方式",
            "memory": "过去写信常要等很久；现在电话和电子邮件让联系变得更容易、更快捷。",
            "memory_visual": "✉️ 过去 → 📞 / 📧 现在 → ⚡ 随时联系",
            "key_sentence_label": "本课核心句",
            "key_sentence": {
                "english": "Technology is making our communication easier and faster.",
                "chinese": "科技正在让我们的沟通更容易、更快捷。",
            },
            "learning_path": ["读前思考", "抓住变化", "进入课文", "开口表达"],
        },
    ),
    CoursewareBlock(
        block_code="reading-ideas",
        block_type="usage_group",
        title="从“过去”到“现在”，看懂沟通方式的变化",
        sort_order=20,
        source_sentence_orders=(10, 11, 14, 15, 16, 17),
        payload={
            "eyebrow": "READ FOR IDEAS",
            "intro": "先找出课文中的过去、现在和结果，再把“科技改变生活”说清楚。",
            "uses": [
                {
                    "title": "过去：写信等回音",
                    "description": "过去人们常用写信保持联系，有时要等几天甚至几周才收到消息。",
                    "examples": [
                        {
                            "english": "In the past, people usually wrote letters to keep in touch with each other.",
                            "chinese": "过去，人们通常写信来保持联系。",
                        },
                        {
                            "english": "Sometimes they waited for days or weeks to hear from others.",
                            "chinese": "有时他们要等上几天甚至几周，才能收到别人的消息。",
                        },
                    ],
                },
                {
                    "title": "现在：随时随地沟通",
                    "description": "电话和电子邮件让我们不受时间、地点的限制，随时保持联系。",
                    "examples": [
                        {
                            "english": "We can use phones to communicate anytime and anywhere.",
                            "chinese": "我们可以随时随地用电话交流。",
                        },
                        {
                            "english": "We can also write emails to keep in touch with others.",
                            "chinese": "我们也可以写电子邮件和别人保持联系。",
                        },
                    ],
                },
                {
                    "title": "结果：联系更快",
                    "description": "电子邮件可以在几秒钟内送达，科技让沟通更加快捷。",
                    "examples": [
                        {
                            "english": "Emails are fast, too.",
                            "chinese": "电子邮件也很快。",
                        },
                        {
                            "english": "They can reach people in seconds.",
                            "chinese": "它们几秒钟就能送达。",
                        },
                    ],
                },
            ],
        },
    ),
    CoursewareBlock(
        block_code="textbook-dialogue",
        block_type="dialogue",
        title="课文情景：给爷爷奶奶的信",
        sort_order=30,
        source_sentence_orders=(4, 5, 6, 7, 10, 13, 15, 19),
        payload={
            "eyebrow": "TEXTBOOK DIALOGUE",
            "scene": "Mike 和 Baobao 聊起给爷爷奶奶写信。",
            "intro": "先听他们的不同选择，再找出科技带来的沟通变化。",
            "collocations": [
                "write a letter",
                "call someone",
                "keep in touch",
                "anytime and anywhere",
            ],
            "lines": [
                {
                    "speaker": "Baobao",
                    "english": "I’m writing a letter to my grandparents.",
                    "chinese": "我正在给祖父母写信。",
                },
                {
                    "speaker": "Mike",
                    "english": "Why don’t you call them? It’s easier and faster.",
                    "chinese": "你为什么不给他们打电话呢？那样更容易也更快。",
                },
                {
                    "speaker": "Baobao",
                    "english": "Writing letters is a tradition in my family.",
                    "chinese": "写信是我家的传统。",
                },
                {
                    "speaker": "Mike",
                    "english": "In the past, people usually wrote letters to keep in touch with each other.",
                    "chinese": "过去，人们通常写信来保持联系。",
                },
                {
                    "speaker": "Baobao",
                    "english": "But technology is changing our communication now.",
                    "chinese": "但科技正在改变我们现在的沟通方式。",
                },
                {
                    "speaker": "Mike",
                    "english": "We can also write emails to keep in touch with others.",
                    "chinese": "我们也可以写电子邮件和别人保持联系。",
                },
                {
                    "speaker": "Baobao",
                    "english": "Technology is making our communication easier and faster.",
                    "chinese": "科技正在让我们的沟通更容易、更快捷。",
                },
            ],
        },
    ),
    CoursewareBlock(
        block_code="language-focus",
        block_type="comparison",
        title="过去时和现在进行时：课文怎样讲“变化”？",
        sort_order=40,
        source_sentence_orders=(10, 13),
        payload={
            "eyebrow": "LANGUAGE FOCUS",
            "intro": "用过去时说从前的习惯，用现在进行时说正在发生的改变。",
            "items": [
                {
                    "expression": "In the past, people usually wrote…",
                    "label": "一般过去时",
                    "meaning": "说过去的习惯或状态",
                    "english": "In the past, people usually wrote letters to keep in touch with each other.",
                    "chinese": "过去，人们通常写信来保持联系。",
                },
                {
                    "expression": "Technology is changing…",
                    "label": "现在进行时",
                    "meaning": "说正在发生的改变",
                    "english": "Technology is changing our communication now.",
                    "chinese": "但科技正在改变我们现在的沟通方式。",
                },
            ],
        },
    ),
    CoursewareBlock(
        block_code="speaking-output",
        block_type="output",
        title="用自己的话说一说",
        sort_order=50,
        source_sentence_orders=(10, 14, 19),
        payload={
            "eyebrow": "SPEAK IT",
            "instruction": "先用第一句说过去，再选一句说现在，最后用第三句说结果。",
            "patterns": [
                "In the past, people usually ________ to keep in touch with each other.",
                "Now we can use ________ to communicate anytime and anywhere.",
                "Technology is making our communication ________ and ________.",
            ],
        },
    ),
    CoursewareBlock(
        block_code="recap",
        block_type="recap",
        title=None,
        sort_order=60,
        source_sentence_orders=(19,),
        payload={
            "eyebrow": "TAKE AWAY",
            "summary": "写信保留传统与情感；电话和邮件让联系随时发生；科技让沟通更容易、更快捷。",
            "key_sentence": {
                "english": "Technology is making our communication easier and faster.",
                "chinese": "科技正在让我们的沟通更容易、更快捷。",
            },
        },
    ),
)


def _inserted_id(connection: Connection, result, table, where_clause) -> int:
    inserted_id = result.inserted_primary_key[0]
    if inserted_id is not None:
        return int(inserted_id)
    return int(connection.execute(select(table.c.id).where(where_clause)).scalar_one())


def _required_scalar(connection: Connection, statement, description: str) -> int:
    rows = [int(value) for value in connection.execute(statement).scalars()]
    if len(rows) != 1:
        raise RuntimeError(f"Expected exactly one {description}; found {len(rows)}.")
    return rows[0]


def _upsert_material(connection: Connection, template_id: int, actor_id: int, report: dict[str, int]) -> int:
    values = {
        "template_id": template_id,
        "material_code": MATERIAL_CODE,
        "title": "课文互动课件 · Lesson 9（样例）",
        "title_en": "Technology Is Changing Our Communication",
        "summary": "把一篇课文转成读前思考、理解、对话、语法聚焦和开口练习。",
        "material_type": "courseware",
        "publisher": "Happy Lingo",
        "version_name": "Unit 3 · Lesson 9 Preview",
        "difficulty_code": "elementary",
        "estimated_minutes": 15,
        "sort_order": 5,
        "is_published": 1,
    }
    material_id = connection.execute(
        select(m.learning_material.c.id).where(
            m.learning_material.c.material_code == MATERIAL_CODE
        )
    ).scalar_one_or_none()
    if material_id is None:
        result = connection.execute(
            m.learning_material.insert().values(created_by=actor_id, **values)
        )
        material_id = _inserted_id(
            connection,
            result,
            m.learning_material,
            m.learning_material.c.material_code == MATERIAL_CODE,
        )
        report["materials_created"] += 1
    else:
        connection.execute(
            update(m.learning_material)
            .where(m.learning_material.c.id == material_id)
            .values(updated_by=actor_id, **values)
        )
        report["materials_updated"] += 1
    return int(material_id)


def _upsert_lesson(connection: Connection, material_id: int, actor_id: int, report: dict[str, int]) -> int:
    values = {
        "lesson_code": LESSON_CODE,
        "title": "Unit 3 · Lesson 9",
        "title_en": "Technology Is Changing Our Communication",
        "summary": "从书信、电话和电子邮件读懂科技如何改变人与人之间的联系。",
        "illustration_url": None,
        "source_resource": None,
        "source_reference_id": None,
        "content_json": None,
        "lesson_format": "courseware",
        "lesson_schema_version": 1,
        "content_status": "published",
        "published_at": func.now(),
        "estimated_minutes": 15,
        "sort_order": 309,
        "is_published": 1,
    }
    lesson_id = connection.execute(
        select(m.learning_material_lesson.c.id).where(
            m.learning_material_lesson.c.material_id == material_id,
            m.learning_material_lesson.c.lesson_code == LESSON_CODE,
        )
    ).scalar_one_or_none()
    if lesson_id is None:
        result = connection.execute(
            m.learning_material_lesson.insert().values(
                material_id=material_id, created_by=actor_id, **values
            )
        )
        lesson_id = _inserted_id(
            connection,
            result,
            m.learning_material_lesson,
            (
                (m.learning_material_lesson.c.material_id == material_id)
                & (m.learning_material_lesson.c.lesson_code == LESSON_CODE)
            ),
        )
        report["lessons_created"] += 1
    else:
        connection.execute(
            update(m.learning_material_lesson)
            .where(m.learning_material_lesson.c.id == lesson_id)
            .values(updated_by=actor_id, **values)
        )
        report["lessons_updated"] += 1
    return int(lesson_id)


def _replace_blocks(
    connection: Connection,
    lesson_id: int,
    actor_id: int,
    sentences: dict[int, dict],
    report: dict[str, int],
) -> None:
    expected_codes = {block.block_code for block in BLOCKS}
    existing = {
        str(row["block_code"]): int(row["id"])
        for row in connection.execute(
            select(m.courseware_block.c.id, m.courseware_block.c.block_code).where(
                m.courseware_block.c.material_lesson_id == lesson_id
            )
        ).mappings()
    }
    stale_ids = [block_id for code, block_id in existing.items() if code not in expected_codes]
    if stale_ids:
        connection.execute(
            delete(m.courseware_block_source).where(
                m.courseware_block_source.c.courseware_block_id.in_(stale_ids)
            )
        )
        connection.execute(delete(m.courseware_block).where(m.courseware_block.c.id.in_(stale_ids)))
        report["blocks_removed"] += len(stale_ids)

    for block in BLOCKS:
        payload_json = json.dumps(block.payload, ensure_ascii=False, separators=(",", ":"))
        values = {
            "block_type": block.block_type,
            "title": block.title,
            "payload_json": payload_json,
            "sort_order": block.sort_order,
            "status": "published",
        }
        block_id = existing.get(block.block_code)
        if block_id is None:
            result = connection.execute(
                m.courseware_block.insert().values(
                    material_lesson_id=lesson_id,
                    block_code=block.block_code,
                    created_by=actor_id,
                    updated_by=actor_id,
                    **values,
                )
            )
            block_id = _inserted_id(
                connection,
                result,
                m.courseware_block,
                (
                    (m.courseware_block.c.material_lesson_id == lesson_id)
                    & (m.courseware_block.c.block_code == block.block_code)
                ),
            )
            report["blocks_created"] += 1
        else:
            connection.execute(
                update(m.courseware_block)
                .where(m.courseware_block.c.id == block_id)
                .values(updated_by=actor_id, **values)
            )
            report["blocks_updated"] += 1

        connection.execute(
            delete(m.courseware_block_source).where(
                m.courseware_block_source.c.courseware_block_id == block_id
            )
        )
        sources = []
        for source_order, sentence_order in enumerate(block.source_sentence_orders, start=1):
            sentence = sentences.get(sentence_order)
            if sentence is None:
                raise RuntimeError(
                    f"Source Lesson 9 is missing sentence {sentence_order}, needed by {block.block_code}."
                )
            snapshot = str(sentence["english_text"])
            sources.append(
                {
                    "courseware_block_id": block_id,
                    "source_resource": "english_textbook_sentence",
                    "source_reference_id": int(sentence["id"]),
                    "source_field": "english_text",
                    "source_locator_json": json.dumps(
                        {"sentence_order": sentence_order},
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ),
                    "source_snapshot_text": snapshot,
                    "source_hash": hashlib.sha256(snapshot.encode("utf-8")).hexdigest(),
                    "sort_order": source_order,
                }
            )
        connection.execute(m.courseware_block_source.insert(), sources)
        report["source_links_replaced"] += len(sources)


def _upsert_course(
    connection: Connection,
    topic_id: int,
    material_id: int,
    actor_id: int,
    report: dict[str, int],
) -> int:
    values = {
        "material_id": material_id,
        "course_code": COURSE_CODE,
        "title": "课文互动课件 · Lesson 9（样例）",
        "title_en": "Technology Is Changing Our Communication",
        "summary": "一节可试听的课文互动课件：读懂变化，再用英语说出来。",
        "course_type": "textbook",
        "content_resource": None,
        "content_reference_id": None,
        "content_json": None,
        "estimated_minutes": 15,
        "difficulty_code": "elementary",
        "sort_order": 5,
        "is_published": 1,
        "access_policy": "free",
    }
    course_id = connection.execute(
        select(m.learning_course.c.id).where(m.learning_course.c.course_code == COURSE_CODE)
    ).scalar_one_or_none()
    if course_id is None:
        result = connection.execute(
            m.learning_course.insert().values(created_by=actor_id, **values)
        )
        course_id = _inserted_id(
            connection,
            result,
            m.learning_course,
            m.learning_course.c.course_code == COURSE_CODE,
        )
        report["courses_created"] += 1
    else:
        connection.execute(
            update(m.learning_course)
            .where(m.learning_course.c.id == course_id)
            .values(updated_by=actor_id, **values)
        )
        report["courses_updated"] += 1

    course_id = int(course_id)
    course_material = connection.execute(
        select(m.learning_course_material.c.id).where(
            m.learning_course_material.c.course_id == course_id,
            m.learning_course_material.c.material_id == material_id,
        )
    ).scalar_one_or_none()
    if course_material is None:
        connection.execute(
            m.learning_course_material.insert().values(
                course_id=course_id,
                material_id=material_id,
                sort_order=10,
                created_by=actor_id,
                updated_by=actor_id,
            )
        )
    else:
        connection.execute(
            update(m.learning_course_material)
            .where(m.learning_course_material.c.id == course_material)
            .values(sort_order=10, updated_by=actor_id)
        )

    topic_course = connection.execute(
        select(m.learning_topic_course.c.id).where(
            m.learning_topic_course.c.topic_id == topic_id,
            m.learning_topic_course.c.course_id == course_id,
        )
    ).scalar_one_or_none()
    if topic_course is None:
        connection.execute(
            m.learning_topic_course.insert().values(
                topic_id=topic_id,
                course_id=course_id,
                sort_order=5,
                created_by=actor_id,
                updated_by=actor_id,
            )
        )
    else:
        connection.execute(
            update(m.learning_topic_course)
            .where(m.learning_topic_course.c.id == topic_course)
            .values(sort_order=5, updated_by=actor_id)
        )
    return course_id


def seed_lesson9_courseware(engine: Engine) -> dict[str, int]:
    """Create or refresh the separate Lesson 9 courseware preview."""

    report = {
        "materials_created": 0,
        "materials_updated": 0,
        "lessons_created": 0,
        "lessons_updated": 0,
        "blocks_created": 0,
        "blocks_updated": 0,
        "blocks_removed": 0,
        "source_links_replaced": 0,
        "courses_created": 0,
        "courses_updated": 0,
    }
    with engine.begin() as connection:
        actor_id = _required_scalar(
            connection,
            select(m.user.c.id)
            .where(m.user.c.role == "admin")
            .order_by(m.user.c.id)
            .limit(1),
            "administrator account",
        )
        topic_id = _required_scalar(
            connection,
            select(m.learning_topic.c.id).where(m.learning_topic.c.topic_code == TOPIC_CODE),
            f"learning topic {TOPIC_CODE!r}",
        )
        template_id = _required_scalar(
            connection,
            select(m.learning_template.c.id).where(
                m.learning_template.c.template_code == TEMPLATE_CODE,
                m.learning_template.c.template_version == TEMPLATE_VERSION,
                m.learning_template.c.status == "active",
            ),
            f"active {TEMPLATE_CODE!r} template",
        )
        source_lesson_id = _required_scalar(
            connection,
            select(m.english_textbook_lesson.c.id).where(
                m.english_textbook_lesson.c.unit_name == SOURCE_UNIT_NAME,
                m.english_textbook_lesson.c.lesson_name == SOURCE_LESSON_NAME,
                m.english_textbook_lesson.c.is_published == 1,
            ),
            "published Unit 3 Lesson 9 source lesson",
        )
        sentences = {
            int(row["sentence_order"]): dict(row)
            for row in connection.execute(
                select(m.english_textbook_sentence)
                .where(
                    m.english_textbook_sentence.c.lesson_id == source_lesson_id,
                    m.english_textbook_sentence.c.is_published == 1,
                )
                .order_by(m.english_textbook_sentence.c.sentence_order)
            ).mappings()
        }
        material_id = _upsert_material(connection, template_id, actor_id, report)
        lesson_id = _upsert_lesson(connection, material_id, actor_id, report)
        _replace_blocks(connection, lesson_id, actor_id, sentences, report)
        course_id = _upsert_course(connection, topic_id, material_id, actor_id, report)

    return {
        **report,
        "topic_id": topic_id,
        "material_id": material_id,
        "lesson_id": lesson_id,
        "course_id": course_id,
        "source_lesson_id": source_lesson_id,
    }


def main() -> None:
    engine = make_engine(Settings().database_url)
    print(json.dumps(seed_lesson9_courseware(engine), ensure_ascii=False))


if __name__ == "__main__":
    main()
