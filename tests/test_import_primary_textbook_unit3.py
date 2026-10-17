from sqlalchemy import func, select, update

from app import models as m
from scripts import import_primary_textbook_unit3 as importer
from tests.support import sample_engine


def _engine_with_textbook_material():
    engine = sample_engine()
    with engine.begin() as connection:
        connection.execute(
            m.learning_material.insert().values(
                id=101,
                material_code=importer.MATERIAL_CODE,
                title="小学英语教材",
                title_en="Primary English Textbook",
                material_type="textbook",
                is_published=1,
            )
        )
    return engine


def test_import_unit3_creates_bilingual_source_and_catalogue_entries():
    engine = _engine_with_textbook_material()

    report = importer.import_unit3(engine)

    assert report == {
        "source_lessons_created": 4,
        "source_lessons_updated": 0,
        "sentences_created": 63,
        "sentences_updated": 0,
        "sentences_deleted": 0,
        "catalogue_lessons_created": 4,
        "catalogue_lessons_updated": 0,
        "material_estimated_minutes": 60,
    }
    with engine.connect() as connection:
        lessons = connection.execute(
            select(m.english_textbook_lesson)
            .where(m.english_textbook_lesson.c.unit_name == "Unit 3")
            .order_by(m.english_textbook_lesson.c.lesson_order)
        ).mappings().all()
        assert [(row["lesson_name"], row["title_cn"]) for row in lessons] == [
            ("Lesson 9", "科技正在改变我们的沟通方式"),
            ("Lesson 10", "科技正在改变我们的学习"),
            ("Lesson 11", "青藏铁路连接西藏与世界"),
            ("Lesson 12", "中国北斗系统让人们的生活更美好"),
        ]
        assert connection.execute(
            select(func.count())
            .select_from(m.english_textbook_sentence)
            .join(
                m.english_textbook_lesson,
                m.english_textbook_lesson.c.id == m.english_textbook_sentence.c.lesson_id,
            )
            .where(m.english_textbook_lesson.c.unit_name == "Unit 3")
        ).scalar_one() == 63

        lesson_12 = lessons[-1]
        lesson_12_sentences = connection.execute(
            select(
                m.english_textbook_sentence.c.english_text,
                m.english_textbook_sentence.c.chinese_text,
            )
            .where(m.english_textbook_sentence.c.lesson_id == lesson_12["id"])
            .order_by(m.english_textbook_sentence.c.sentence_order)
        ).all()
        assert lesson_12_sentences[0] == (
            "BDS, China’s BeiDou Navigation Satellite System, went into service all over the world "
            "on the 31st of July 2020.",
            "北斗系统，即中国北斗卫星导航系统，于 2020 年 7 月 31 日在全球投入服务。",
        )
        assert lesson_12_sentences[-1] == (
            "In the future, BDS will work better for people both in China and other countries.",
            "将来，北斗系统会更好地服务中国和其他国家的人们。",
        )

        catalogue_rows = connection.execute(
            select(m.learning_material_lesson)
            .where(m.learning_material_lesson.c.material_id == 101)
            .order_by(m.learning_material_lesson.c.sort_order)
        ).mappings().all()
        assert [
            (
                row["lesson_code"],
                row["title"],
                row["title_en"],
                row["source_resource"],
                row["sort_order"],
                row["content_status"],
            )
            for row in catalogue_rows
        ] == [
            (
                "textbook-unit-03-lesson-09",
                "科技正在改变我们的沟通方式",
                "Technology Is Changing Our Communication",
                "textbook",
                309,
                "published",
            ),
            (
                "textbook-unit-03-lesson-10",
                "科技正在改变我们的学习",
                "Technology Is Changing Our Learning",
                "textbook",
                310,
                "published",
            ),
            (
                "textbook-unit-03-lesson-11",
                "青藏铁路连接西藏与世界",
                "The Qinghai-Xizang Railway Connects Xizang to the World",
                "textbook",
                311,
                "published",
            ),
            (
                "textbook-unit-03-lesson-12",
                "中国北斗系统让人们的生活更美好",
                "China’s BDS Makes People’s Lives Better",
                "textbook",
                312,
                "published",
            ),
        ]


def test_import_unit3_reuses_source_linked_catalogue_lesson_and_removes_stale_sentence():
    engine = _engine_with_textbook_material()
    importer.import_unit3(engine)

    with engine.begin() as connection:
        lesson_9_id = connection.execute(
            select(m.english_textbook_lesson.c.id).where(
                m.english_textbook_lesson.c.unit_name == "Unit 3",
                m.english_textbook_lesson.c.lesson_name == "Lesson 9",
            )
        ).scalar_one()
        connection.execute(
            m.english_textbook_sentence.insert().values(
                lesson_id=lesson_9_id,
                sentence_order=99,
                english_text="stale",
                chinese_text="过期内容",
            )
        )
        connection.execute(
            update(m.learning_material_lesson)
            .where(
                m.learning_material_lesson.c.material_id == 101,
                m.learning_material_lesson.c.source_reference_id == lesson_9_id,
            )
            .values(lesson_code="legacy-unit-3-lesson-9")
        )

    report = importer.import_unit3(engine)

    assert report["source_lessons_created"] == 0
    assert report["catalogue_lessons_created"] == 0
    assert report["sentences_deleted"] == 1
    with engine.connect() as connection:
        assert connection.execute(
            select(m.english_textbook_sentence.c.id).where(
                m.english_textbook_sentence.c.lesson_id == lesson_9_id,
                m.english_textbook_sentence.c.sentence_order == 99,
            )
        ).scalar_one_or_none() is None
        assert connection.execute(
            select(m.learning_material_lesson.c.lesson_code).where(
                m.learning_material_lesson.c.material_id == 101,
                m.learning_material_lesson.c.source_reference_id == lesson_9_id,
            )
        ).scalar_one() == "textbook-unit-03-lesson-09"
        assert connection.execute(
            select(func.count())
            .select_from(m.learning_material_lesson)
            .where(m.learning_material_lesson.c.material_id == 101)
        ).scalar_one() == 4
