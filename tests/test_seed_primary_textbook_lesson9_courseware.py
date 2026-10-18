from __future__ import annotations

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app import models as m
from app.services.learning_catalog import LearningCatalogService
from scripts.import_primary_textbook_unit3 import UNIT3_LESSONS
from scripts.seed_primary_textbook_lesson9_courseware import (
    BLOCKS,
    COURSE_CODE,
    LESSON_CODE,
    MATERIAL_CODE,
    seed_lesson9_courseware,
)
from tests.support import sample_engine


def _prepare_lesson9_source(engine):
    source = UNIT3_LESSONS[0]
    with engine.begin() as connection:
        connection.execute(
            update(m.learning_topic)
            .where(m.learning_topic.c.topic_code == "english-textbook")
            .values(is_published=1)
        )
        connection.execute(
            m.learning_template.insert().values(
                template_code="put-aside",
                template_version=1,
                name="互动课件",
                description="按主题、阅读、情景和输出区块组织的互动课件。",
                content_kind="courseware",
                supported_clients_json='["web","mini"]',
                config_json="{}",
                status="active",
                sort_order=20,
            )
        )
        result = connection.execute(
            m.english_textbook_lesson.insert().values(
                unit_name=source.unit_name,
                lesson_name=source.lesson_name,
                title=source.title,
                title_cn=source.title_cn,
                summary=source.summary,
                unit_order=source.unit_order,
                lesson_order=source.lesson_order,
                is_published=1,
            )
        )
        source_lesson_id = int(result.inserted_primary_key[0])
        connection.execute(
            m.english_textbook_sentence.insert(),
            [
                {
                    "lesson_id": source_lesson_id,
                    "sentence_order": sentence_order,
                    "english_text": sentence.english_text,
                    "chinese_text": sentence.chinese_text,
                    "is_published": 1,
                }
                for sentence_order, sentence in enumerate(source.sentences, start=1)
            ],
        )


def test_seed_lesson9_courseware_is_public_traceable_and_idempotent():
    engine = sample_engine()
    _prepare_lesson9_source(engine)

    first = seed_lesson9_courseware(engine)
    second = seed_lesson9_courseware(engine)

    assert first["materials_created"] == 1
    assert first["lessons_created"] == 1
    assert first["blocks_created"] == len(BLOCKS)
    assert first["courses_created"] == 1
    assert second["materials_updated"] == 1
    assert second["lessons_updated"] == 1
    assert second["blocks_updated"] == len(BLOCKS)
    assert second["courses_updated"] == 1
    assert first["material_id"] == second["material_id"]
    assert first["lesson_id"] == second["lesson_id"]
    assert first["course_id"] == second["course_id"]

    with engine.connect() as connection:
        material = connection.execute(
            select(m.learning_material).where(
                m.learning_material.c.material_code == MATERIAL_CODE
            )
        ).mappings().one()
        lesson = connection.execute(
            select(m.learning_material_lesson).where(
                m.learning_material_lesson.c.id == first["lesson_id"]
            )
        ).mappings().one()
        assert material["is_published"] == 1
        assert lesson["lesson_code"] == LESSON_CODE
        assert lesson["lesson_format"] == "courseware"
        assert lesson["content_status"] == "published"
        assert connection.scalar(
            select(func.count()).select_from(m.courseware_block).where(
                m.courseware_block.c.material_lesson_id == first["lesson_id"],
                m.courseware_block.c.status == "published",
            )
        ) == len(BLOCKS)
        sources = connection.execute(
            select(m.courseware_block_source)
            .join(
                m.courseware_block,
                m.courseware_block.c.id
                == m.courseware_block_source.c.courseware_block_id,
            )
            .where(m.courseware_block.c.material_lesson_id == first["lesson_id"])
        ).mappings().all()
        assert len(sources) == sum(len(block.source_sentence_orders) for block in BLOCKS)
        assert {source["source_resource"] for source in sources} == {
            "english_textbook_sentence"
        }
        assert all(len(source["source_hash"]) == 64 for source in sources)
        assert connection.scalar(
            select(func.count()).select_from(m.learning_course_material).where(
                m.learning_course_material.c.course_id == first["course_id"],
                m.learning_course_material.c.material_id == first["material_id"],
            )
        ) == 1
        assert connection.scalar(
            select(func.count()).select_from(m.learning_topic_course).where(
                m.learning_topic_course.c.course_id == first["course_id"]
            )
        ) == 1
        assert connection.scalar(
            select(m.learning_course.c.course_code).where(
                m.learning_course.c.id == first["course_id"]
            )
        ) == COURSE_CODE

    with Session(engine) as db:
        material = LearningCatalogService(db).get_material(first["material_id"])
        detail = LearningCatalogService(db).get_material_lesson(
            first["material_id"], first["lesson_id"]
        )
    assert material["template"]["renderer"] == "put-aside.v1"
    assert material["lessons"][0]["lesson_code"] == LESSON_CODE
    assert detail["render_payload"]["content_kind"] == "courseware"
    blocks = detail["courseware_blocks"]
    assert [block["block_code"] for block in blocks] == [
        block.block_code for block in BLOCKS
    ]
    assert blocks[0]["payload"]["eyebrow"] == "UNIT 3 · LESSON 9 · READING & SPEAKING"
    assert "sources" not in blocks[0]
