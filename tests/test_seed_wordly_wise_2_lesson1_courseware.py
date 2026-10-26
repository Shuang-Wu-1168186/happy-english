from __future__ import annotations

import json

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.services.courseware import CoursewareBlockService
from app.services.learning_catalog import LearningCatalogService
from scripts.seed_wordly_wise_2_lesson1_courseware import (
    BLOCKS,
    COURSE_CODE,
    LESSON_CODE,
    MATERIAL_CODE,
    seed_wordly_wise_2_lesson1_courseware,
)
from tests.support import sample_engine


def _prepare_wordly_wise_2(engine):
    """Create the pre-existing Book 2 catalogue rows owned by its word-list seed."""

    with engine.begin() as connection:
        template_id = int(
            connection.execute(
                m.learning_template.insert().values(
                    template_code="put-aside",
                    template_version=1,
                    name="互动课件",
                    description="按区块组织的互动课件。",
                    content_kind="courseware",
                    supported_clients_json='["web","mini","android"]',
                    config_json="{}",
                    status="active",
                    sort_order=20,
                )
            ).inserted_primary_key[0]
        )
        topic_id = int(
            connection.execute(
                m.learning_topic.insert().values(
                    module_id=3,
                    topic_code="w",
                    title="Wordly Wise",
                    title_en="Wordly Wise",
                    description="分级词汇教材",
                    sort_order=16,
                    is_published=1,
                )
            ).inserted_primary_key[0]
        )
        material_id = int(
            connection.execute(
                m.learning_material.insert().values(
                    template_id=template_id,
                    material_code=MATERIAL_CODE,
                    title="Wordly Wise 2 · 单词教材",
                    title_en="Wordly Wise 3000 Book 2",
                    summary="15 节 Word List 单词课。",
                    material_type="textbook",
                    difficulty_code="elementary",
                    estimated_minutes=300,
                    sort_order=16,
                    is_published=1,
                    created_by=1,
                )
            ).inserted_primary_key[0]
        )
        course_id = int(
            connection.execute(
                m.learning_course.insert().values(
                    material_id=material_id,
                    course_code=COURSE_CODE,
                    title="Wordly Wise 2（单词教材）",
                    title_en="Wordly Wise 3000 Book 2",
                    summary="Book 2",
                    course_type="textbook",
                    estimated_minutes=300,
                    difficulty_code="elementary",
                    sort_order=16,
                    is_published=1,
                    access_policy="free",
                    created_by=1,
                )
            ).inserted_primary_key[0]
        )
        connection.execute(
            m.learning_course_material.insert().values(
                course_id=course_id,
                material_id=material_id,
                sort_order=10,
                created_by=1,
                updated_by=1,
            )
        )
        connection.execute(
            m.learning_topic_course.insert().values(
                topic_id=topic_id,
                course_id=course_id,
                sort_order=16,
                created_by=1,
                updated_by=1,
            )
        )


def test_seed_wordly_wise_2_lesson1_courseware_is_idempotent_and_public():
    engine = sample_engine()
    _prepare_wordly_wise_2(engine)

    for block in BLOCKS:
        input_payload = s.CoursewareBlockInput(
            block_code=block.block_code,
            block_type=block.block_type,
            title=block.title,
            payload=block.payload,
            sort_order=block.sort_order,
        )
        assert input_payload.block_type == block.block_type
        CoursewareBlockService.validate_payload(block.block_type, block.payload)

    first = seed_wordly_wise_2_lesson1_courseware(engine)
    second = seed_wordly_wise_2_lesson1_courseware(engine)

    assert first["lessons_created"] == 1
    assert first["blocks_created"] == len(BLOCKS)
    assert second["lessons_updated"] == 1
    assert second["blocks_updated"] == len(BLOCKS)
    assert first["lesson_id"] == second["lesson_id"]
    assert first["material_id"] == second["material_id"]
    assert first["course_id"] == second["course_id"]

    with engine.connect() as connection:
        material = connection.execute(
            select(m.learning_material).where(
                m.learning_material.c.id == first["material_id"]
            )
        ).mappings().one()
        course = connection.execute(
            select(m.learning_course).where(m.learning_course.c.id == first["course_id"])
        ).mappings().one()
        lesson = connection.execute(
            select(m.learning_material_lesson).where(
                m.learning_material_lesson.c.id == first["lesson_id"]
            )
        ).mappings().one()
        source_metadata = json.loads(lesson["content_json"])
        assert lesson["lesson_code"] == LESSON_CODE
        assert lesson["lesson_format"] == "courseware"
        assert lesson["content_status"] == "published"
        assert material["title"] == "Wordly Wise 2（单词与阅读）"
        assert "Lesson 1 的阅读与练习" in material["summary"]
        assert course["estimated_minutes"] == 335
        assert source_metadata["courseware_family"] == "wordly_wise"
        assert source_metadata["source"]["pdf_pages"] == list(range(10, 18))
        assert connection.scalar(
            select(func.count()).select_from(m.courseware_block).where(
                m.courseware_block.c.material_lesson_id == first["lesson_id"],
                m.courseware_block.c.status == "published",
            )
        ) == len(BLOCKS)
        # The scanned PDF has no normalized source-record table. Its document
        # and page provenance are stored in the lesson and each block payload,
        # rather than creating fake note/textbook source records.
        assert connection.scalar(
            select(func.count()).select_from(m.courseware_block_source).join(
                m.courseware_block,
                m.courseware_block.c.id
                == m.courseware_block_source.c.courseware_block_id,
            ).where(m.courseware_block.c.material_lesson_id == first["lesson_id"])
        ) == 0

    with Session(engine) as db:
        catalog = LearningCatalogService(db)
        material = catalog.get_material(first["material_id"])
        detail = catalog.get_material_lesson(first["material_id"], first["lesson_id"])

    assert material["template"]["renderer"] == "put-aside.v1"
    assert material["lessons"][0]["lesson_code"] == LESSON_CODE
    assert detail["render_payload"]["content_kind"] == "courseware"
    blocks = detail["courseware_blocks"]
    assert [block["block_code"] for block in blocks] == [
        block.block_code for block in BLOCKS
    ]
    reading = next(block for block in blocks if block["block_code"] == "wordly-wise-reading")
    comprehension = next(
        block for block in blocks if block["block_code"] == "wordly-wise-comprehension"
    )
    review = next(block for block in blocks if block["block_code"] == "wordly-wise-review")
    assert len(reading["payload"]["paragraphs"]) == 7
    assert len(comprehension["payload"]["items"]) == 10
    assert len(review["payload"]["items"]) == 12
    assert "sources" not in reading
