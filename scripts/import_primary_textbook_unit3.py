#!/usr/bin/env python3
"""Import Unit 3 of the primary English textbook into the active catalogue.

The four lessons were transcribed from the supplied textbook pages. The
importer writes both the original bilingual textbook source and the matching
"english-textbook-current" material entries, so learners see the lessons in
the existing textbook reader. It is safe to run again after a content edit.

Run locally or on the application server with:

    PYTHONPATH=. .venv/bin/python scripts/import_primary_textbook_unit3.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from sqlalchemy import delete, select, update
from sqlalchemy.engine import Connection, Engine

from app import models as m
from app.core.config import Settings
from app.core.database import make_engine


MATERIAL_CODE = "english-textbook-current"
SOURCE_RESOURCE = "textbook"
ESTIMATED_MINUTES_PER_LESSON = 15


@dataclass(frozen=True)
class Sentence:
    english_text: str
    chinese_text: str


@dataclass(frozen=True)
class TextbookLesson:
    lesson_name: str
    title: str
    title_cn: str
    summary: str
    lesson_order: int
    sentences: tuple[Sentence, ...]
    unit_name: str = "Unit 3"
    unit_order: int = 3


UNIT3_LESSONS = (
    TextbookLesson(
        lesson_name="Lesson 9",
        lesson_order=9,
        title="Technology Is Changing Our Communication",
        title_cn="科技正在改变我们的沟通方式",
        summary="通信方式对话：书信、电话和电子邮件如何改变人与人之间的联系。",
        sentences=(
            Sentence("Mike: Hi, Baobao!", "迈克：嗨，宝宝！"),
            Sentence("Mike: What are you doing?", "迈克：你在做什么？"),
            Sentence("Baobao: Hi, Mike!", "宝宝：嗨，迈克！"),
            Sentence("Baobao: I’m writing a letter to my grandparents.", "宝宝：我正在给祖父母写信。"),
            Sentence("Mike: Oh, why don’t you call them?", "迈克：哦，你为什么不给他们打电话呢？"),
            Sentence("Mike: It’s easier and faster.", "迈克：那样更容易也更快。"),
            Sentence("Baobao: Writing letters is a tradition in my family.", "宝宝：写信是我家的传统。"),
            Sentence("Baobao: It’s also a good way to collect stamps.", "宝宝：这也是收集邮票的好方法。"),
            Sentence("Mike: I see.", "迈克：我明白了。"),
            Sentence(
                "Mike: In the past, people usually wrote letters to keep in touch with each other.",
                "迈克：过去，人们通常写信来保持联系。",
            ),
            Sentence(
                "Mike: Sometimes they waited for days or weeks to hear from others.",
                "迈克：有时他们要等上几天甚至几周，才能收到别人的消息。",
            ),
            Sentence("Baobao: Yes, you are right.", "宝宝：是的，你说得对。"),
            Sentence(
                "Baobao: But technology is changing our communication now.",
                "宝宝：但科技正在改变我们现在的沟通方式。",
            ),
            Sentence(
                "Baobao: We can use phones to communicate anytime and anywhere.",
                "宝宝：我们可以随时随地用电话交流。",
            ),
            Sentence(
                "Mike: We can also write emails to keep in touch with others.",
                "迈克：我们也可以写电子邮件和别人保持联系。",
            ),
            Sentence("Mike: Emails are fast, too.", "迈克：电子邮件也很快。"),
            Sentence("Mike: They can reach people in seconds.", "迈克：它们几秒钟就能送达。"),
            Sentence("Baobao: That’s true.", "宝宝：确实如此。"),
            Sentence(
                "Baobao: Technology is making our communication easier and faster.",
                "宝宝：科技正在让我们的沟通更容易、更快捷。",
            ),
        ),
    ),
    TextbookLesson(
        lesson_name="Lesson 10",
        lesson_order=10,
        title="Technology Is Changing Our Learning",
        title_cn="科技正在改变我们的学习",
        summary="学习方式对话：国家智慧教育平台、VR 和机器人教师带来的学习变化。",
        sentences=(
            Sentence(
                "Yangyang: Can you help me with this science problem, Lingling?",
                "阳阳：玲玲，你能帮我解答这道科学题吗？",
            ),
            Sentence("Lingling: Sorry, I’m not sure about it.", "玲玲：抱歉，我不太确定。"),
            Sentence(
                "Lingling: We can study this part again on Smart Education of China.",
                "玲玲：我们可以在国家智慧教育平台上再学习这一部分。",
            ),
            Sentence("Yangyang: What’s Smart Education of China?", "阳阳：什么是国家智慧教育平台？"),
            Sentence("Lingling: It’s an online learning platform.", "玲玲：它是一个在线学习平台。"),
            Sentence("Lingling: We can take online lessons on it.", "玲玲：我们可以在上面学习在线课程。"),
            Sentence("Yangyang: That’s cool!", "阳阳：太酷了！"),
            Sentence("Yangyang: Online learning is making learning easier.", "阳阳：在线学习让学习变得更容易。"),
            Sentence("Lingling: Some schools are also using VR technology.", "玲玲：一些学校也在使用 VR 技术。"),
            Sentence("Lingling: It makes learning more interesting.", "玲玲：它让学习更有趣。"),
            Sentence(
                "Lingling: For example, if you want to learn about space, you can put on special "
                "glasses to feel what space is like.",
                "玲玲：例如，如果你想了解太空，你可以戴上特殊的眼镜，感受太空是什么样子。",
            ),
            Sentence("Yangyang: That’s amazing.", "阳阳：太神奇了。"),
            Sentence(
                "Yangyang: Kids in England can ask robot teachers to help them with lessons.",
                "阳阳：英国的孩子可以请机器人老师帮助他们学习课程。",
            ),
            Sentence(
                "Yangyang: These robots can quickly solve students’ problems.",
                "阳阳：这些机器人能很快解决学生的问题。",
            ),
            Sentence("Lingling: Technology is really changing our learning.", "玲玲：科技真的在改变我们的学习。"),
            Sentence("Lingling: I like these new and fun ways.", "玲玲：我喜欢这些新颖又有趣的方式。"),
        ),
    ),
    TextbookLesson(
        lesson_name="Lesson 11",
        lesson_order=11,
        title="The Qinghai-Xizang Railway Connects Xizang to the World",
        title_cn="青藏铁路连接西藏与世界",
        summary="青藏铁路说明文：科技如何让西藏交通更便利，并改善当地人的生活。",
        sentences=(
            Sentence("In the past, there was no railway in Xizang.", "过去，西藏没有铁路。"),
            Sentence(
                "Most people travelled by bus, on foot or on horseback.",
                "大多数人乘公共汽车、步行或骑马出行。",
            ),
            Sentence("It was hard to get into and out of Xizang.", "进出西藏很困难。"),
            Sentence(
                "With the help of technology, the Qinghai-Xizang Railway went into service in 2006.",
                "在科技的帮助下，青藏铁路于 2006 年投入运营。",
            ),
            Sentence("It is the highest railway in the world.", "它是世界上最高的铁路。"),
            Sentence("It starts in Xining and ends in Lhasa.", "它起于西宁，止于拉萨。"),
            Sentence(
                "This is the first railway connecting Xizang to other parts of China.",
                "这是连接西藏与中国其他地区的第一条铁路。",
            ),
            Sentence(
                "The railway crosses no-man’s land and climbs up snowy mountains.",
                "铁路穿越无人区，翻越雪山。",
            ),
            Sentence(
                "People all think it is amazing to build a railway like that.",
                "人们都认为修建这样一条铁路十分了不起。",
            ),
            Sentence(
                "The Qinghai-Xizang Railway makes travel to Xizang easier.",
                "青藏铁路让前往西藏的旅行更方便。",
            ),
            Sentence(
                "More and more people come to Xizang, because they are interested in the culture "
                "and life here.",
                "越来越多的人来到西藏，因为他们对这里的文化和生活感兴趣。",
            ),
            Sentence(
                "People in Xizang enjoy a better life too, and they feel it is easier to see the "
                "outside world.",
                "西藏人民也享受着更好的生活，他们觉得了解外面世界变得更容易了。",
            ),
        ),
    ),
    TextbookLesson(
        lesson_name="Lesson 12",
        lesson_order=12,
        title="China’s BDS Makes People’s Lives Better",
        title_cn="中国北斗系统让人们的生活更美好",
        summary="北斗系统说明文：导航、智慧农业和天气预警如何让生活更美好。",
        sentences=(
            Sentence(
                "BDS, China’s BeiDou Navigation Satellite System, went into service all over the "
                "world on the 31st of July 2020.",
                "北斗系统，即中国北斗卫星导航系统，于 2020 年 7 月 31 日在全球投入服务。",
            ),
            Sentence("BDS helps us know more about the Earth and space.", "北斗系统帮助我们更多地了解地球和太空。"),
            Sentence("It also makes people’s lives better.", "它也让人们的生活更美好。"),
            Sentence("First, BDS helps people find the way.", "首先，北斗系统帮助人们找到路。"),
            Sentence(
                "All the satellites of it move around the Earth with “good eyes”.",
                "它的所有卫星带着“好眼睛”围绕地球运行。",
            ),
            Sentence(
                "These eyes can see rivers, trees, mountains, houses and animals.",
                "这些眼睛能看见河流、树木、山脉、房屋和动物。",
            ),
            Sentence(
                "When people get lost and need help, BDS can show them the way.",
                "当人们迷路需要帮助时，北斗系统能为他们指路。",
            ),
            Sentence(
                "Second, BDS makes farming smarter, easier and safer.",
                "第二，北斗系统让耕作更智能、更轻松、更安全。",
            ),
            Sentence(
                "With the help of BDS, machines can do farm work on their own.",
                "借助北斗系统，机器可以自行完成农活。",
            ),
            Sentence(
                "Farmers are not so busy with farm work as before.",
                "农民不再像过去那样忙于农活。",
            ),
            Sentence(
                "BDS is changing farmers’ ways of living and working.",
                "北斗系统正在改变农民的生活和工作方式。",
            ),
            Sentence("Third, BDS helps keep people safe.", "第三，北斗系统帮助保障人们的安全。"),
            Sentence(
                "For example, BDS can protect people from bad weather.",
                "例如，北斗系统可以保护人们免受恶劣天气的影响。",
            ),
            Sentence(
                "It can tell us a heavy rain is coming before the rain comes.",
                "在大雨来临前，它能告诉我们大雨将要来临。",
            ),
            Sentence(
                "It can also tell us how the weather will change.",
                "它还能告诉我们天气将如何变化。",
            ),
            Sentence(
                "In the future, BDS will work better for people both in China and other countries.",
                "将来，北斗系统会更好地服务中国和其他国家的人们。",
            ),
        ),
    ),
)


def _inserted_id(connection: Connection, result, table, where_clause) -> int:
    inserted_id = result.inserted_primary_key[0]
    if inserted_id is not None:
        return int(inserted_id)
    return int(connection.execute(select(table.c.id).where(where_clause)).scalar_one())


def _upsert_source_lesson(
    connection: Connection,
    lesson: TextbookLesson,
    report: dict[str, int],
) -> int:
    existing = connection.execute(
        select(m.english_textbook_lesson.c.id).where(
            m.english_textbook_lesson.c.unit_name == lesson.unit_name,
            m.english_textbook_lesson.c.lesson_name == lesson.lesson_name,
        )
    ).mappings().one_or_none()
    source_values = {
        "unit_name": lesson.unit_name,
        "lesson_name": lesson.lesson_name,
        "title": lesson.title,
        "title_cn": lesson.title_cn,
        "summary": lesson.summary,
        "unit_order": lesson.unit_order,
        "lesson_order": lesson.lesson_order,
        "is_published": 1,
    }
    if existing is None:
        result = connection.execute(m.english_textbook_lesson.insert().values(**source_values))
        source_id = _inserted_id(
            connection,
            result,
            m.english_textbook_lesson,
            (
                (m.english_textbook_lesson.c.unit_name == lesson.unit_name)
                & (m.english_textbook_lesson.c.lesson_name == lesson.lesson_name)
            ),
        )
        report["source_lessons_created"] += 1
    else:
        source_id = int(existing["id"])
        connection.execute(
            update(m.english_textbook_lesson)
            .where(m.english_textbook_lesson.c.id == source_id)
            .values(**source_values)
        )
        report["source_lessons_updated"] += 1

    existing_sentences = {
        int(row["sentence_order"]): row["id"]
        for row in connection.execute(
            select(
                m.english_textbook_sentence.c.id,
                m.english_textbook_sentence.c.sentence_order,
            ).where(m.english_textbook_sentence.c.lesson_id == source_id)
        ).mappings()
    }
    expected_orders = set()
    for sentence_order, sentence in enumerate(lesson.sentences, start=1):
        expected_orders.add(sentence_order)
        sentence_values = {
            "sentence_order": sentence_order,
            "english_text": sentence.english_text,
            "chinese_text": sentence.chinese_text,
            "is_published": 1,
        }
        sentence_id = existing_sentences.get(sentence_order)
        if sentence_id is None:
            connection.execute(
                m.english_textbook_sentence.insert().values(
                    lesson_id=source_id,
                    **sentence_values,
                )
            )
            report["sentences_created"] += 1
        else:
            connection.execute(
                update(m.english_textbook_sentence)
                .where(m.english_textbook_sentence.c.id == sentence_id)
                .values(**sentence_values)
            )
            report["sentences_updated"] += 1

    stale_result = connection.execute(
        delete(m.english_textbook_sentence).where(
            m.english_textbook_sentence.c.lesson_id == source_id,
            m.english_textbook_sentence.c.sentence_order.not_in(expected_orders),
        )
    )
    report["sentences_deleted"] += max(stale_result.rowcount or 0, 0)
    return source_id


def _one_catalogue_lesson(
    connection: Connection,
    where_clause,
    lookup_description: str,
) -> dict | None:
    rows = connection.execute(select(m.learning_material_lesson).where(where_clause)).mappings().all()
    if len(rows) > 1:
        raise RuntimeError(f"Duplicate textbook catalogue entries found for {lookup_description}.")
    return dict(rows[0]) if rows else None


def _catalogue_lesson_code(source: dict) -> str:
    return (
        f"textbook-unit-{int(source['unit_order']):02d}-"
        f"lesson-{int(source['lesson_order']):02d}"
    )


def _upsert_catalogue_lesson(
    connection: Connection,
    material_id: int,
    source: dict,
    report: dict[str, int],
) -> None:
    lesson_code = _catalogue_lesson_code(source)
    source_id = int(source["id"])
    source_match = _one_catalogue_lesson(
        connection,
        (
            (m.learning_material_lesson.c.material_id == material_id)
            & (m.learning_material_lesson.c.source_resource == SOURCE_RESOURCE)
            & (m.learning_material_lesson.c.source_reference_id == source_id)
        ),
        f"{source['unit_name']} / {source['lesson_name']} source",
    )
    code_match = _one_catalogue_lesson(
        connection,
        (
            (m.learning_material_lesson.c.material_id == material_id)
            & (m.learning_material_lesson.c.lesson_code == lesson_code)
        ),
        f"{lesson_code} code",
    )
    if source_match is not None and code_match is not None and source_match["id"] != code_match["id"]:
        raise RuntimeError(
            "Conflicting textbook catalogue entries found for "
            f"{source['unit_name']} / {source['lesson_name']}."
        )

    existing = source_match or code_match
    source_title = str(source["title"] or "")
    source_title_cn = str(
        source["title_cn"]
        or source_title
        or f"{source['unit_name']} · {source['lesson_name']}"
    )
    catalogue_values = {
        "lesson_code": lesson_code,
        "title": source_title_cn,
        "title_en": source_title or None,
        "summary": source["summary"],
        "illustration_url": None,
        "source_resource": SOURCE_RESOURCE,
        "source_reference_id": source_id,
        "content_json": None,
        "lesson_format": "source",
        "lesson_schema_version": 1,
        "content_status": "published",
        "estimated_minutes": ESTIMATED_MINUTES_PER_LESSON,
        "sort_order": int(source["unit_order"]) * 100 + int(source["lesson_order"]),
        "is_published": 1,
    }
    if existing is None:
        connection.execute(
            m.learning_material_lesson.insert().values(
                material_id=material_id,
                **catalogue_values,
            )
        )
        report["catalogue_lessons_created"] += 1
        return

    connection.execute(
        update(m.learning_material_lesson)
        .where(m.learning_material_lesson.c.id == existing["id"])
        .values(**catalogue_values)
    )
    report["catalogue_lessons_updated"] += 1


def _sync_primary_textbook_catalogue(
    connection: Connection,
    material_id: int,
    report: dict[str, int],
) -> int:
    """Keep every catalogue row ordered from its authoritative source lesson."""

    sources = [
        dict(row)
        for row in connection.execute(
            select(m.english_textbook_lesson)
            .where(m.english_textbook_lesson.c.is_published == 1)
            .order_by(
                m.english_textbook_lesson.c.unit_order,
                m.english_textbook_lesson.c.lesson_order,
                m.english_textbook_lesson.c.id,
            )
        ).mappings()
    ]
    for source in sources:
        _upsert_catalogue_lesson(connection, material_id, source, report)
    return len(sources)


def import_unit3(engine: Engine) -> dict[str, int]:
    """Upsert all four Unit 3 lessons and synchronise the textbook catalogue."""

    report = {
        "source_lessons_created": 0,
        "source_lessons_updated": 0,
        "sentences_created": 0,
        "sentences_updated": 0,
        "sentences_deleted": 0,
        "catalogue_lessons_created": 0,
        "catalogue_lessons_updated": 0,
        "material_estimated_minutes": 0,
    }
    with engine.begin() as connection:
        material_id = connection.execute(
            select(m.learning_material.c.id).where(m.learning_material.c.material_code == MATERIAL_CODE)
        ).scalar_one_or_none()
        if material_id is None:
            raise RuntimeError(f"Learning material {MATERIAL_CODE!r} does not exist.")

        for lesson in UNIT3_LESSONS:
            _upsert_source_lesson(connection, lesson, report)

        textbook_lesson_count = _sync_primary_textbook_catalogue(
            connection,
            int(material_id),
            report,
        )
        material_minutes = textbook_lesson_count * ESTIMATED_MINUTES_PER_LESSON
        connection.execute(
            update(m.learning_material)
            .where(m.learning_material.c.id == material_id)
            .values(estimated_minutes=material_minutes, is_published=1)
        )
        report["material_estimated_minutes"] = material_minutes
    return report


def main() -> None:
    engine = make_engine(Settings().database_url)
    print(json.dumps(import_unit3(engine), ensure_ascii=False))


if __name__ == "__main__":
    main()
