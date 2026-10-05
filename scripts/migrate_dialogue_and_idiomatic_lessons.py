"""Backfill generic sections for idiomatic-English courseware.

Daily spoken dialogue migration is complete and its legacy source table has
been retired.  The idiomatic-English series keeps its courseware rendering;
its generic section copy deliberately has no item-source records.  Re-run with
``--apply`` to insert rows; existing generic content is skipped unless
``--replace`` is explicitly used.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path
import sys

from sqlalchemy import select

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import models as m  # noqa: E402
from app.core.config import Settings  # noqa: E402
from app.core.database import make_engine  # noqa: E402


SECTION_META = {
    "core_vocabulary": ("核心词汇", "Core Vocabulary", 10),
    "situational_dialogues": ("情景对话", "Situational Dialogues", 20),
    "key_sentence_patterns": ("核心句型", "Key Sentence Patterns", 30),
    "speaking_practice": ("口语练习", "Speaking Practice", 40),
    "mini_exercises": ("小练习", "Mini Exercises", 50),
    "useful_tips": ("实用表达提示", "Useful Tips", 60),
    "extended_reading": ("扩展阅读", "Extended Reading", 70),
}


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def decode(value, fallback):
    if value is None:
        return fallback
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return fallback


def item(code, payload, title=None, order=10):
    return {
        "item_code": code,
        "item_order": order,
        "title": title,
        "payload": payload,
    }


def idiomatic_sections(blocks):
    by_type = {block["block_type"]: block for block in blocks}

    def block_payload(block_type):
        block = by_type.get(block_type)
        return decode(block["payload_json"], {}) if block else {}

    hero = block_payload("hero")
    usage = block_payload("usage_group")
    dialogue = block_payload("dialogue")
    comparison = block_payload("comparison")
    output = block_payload("output")
    recap = block_payload("recap")
    uses = usage.get("uses") if isinstance(usage.get("uses"), list) else []

    return {
        "core_vocabulary": [
            item(
                "target-expression",
                {
                    "term": hero.get("phrase", ""),
                    "meaning": hero.get("meaning", ""),
                    "memory": hero.get("memory", ""),
                    "example": hero.get("key_sentence"),
                },
            )
        ]
        if hero
        else [],
        "situational_dialogues": [
            item(
                "real-life-dialogue",
                {
                    "scenario": dialogue.get("scene", "真实场景"),
                    "turns": dialogue.get("lines", []),
                    "collocations": dialogue.get("collocations", []),
                },
            )
        ]
        if dialogue
        else [],
        "key_sentence_patterns": [
            item(
                f"usage-{index:02d}",
                {
                    "pattern": use.get("description") or use.get("title") or "",
                    "meaning": use.get("title") or "",
                    "examples": use.get("examples", []),
                },
                use.get("title"),
                index * 10,
            )
            for index, use in enumerate(uses, start=1)
            if isinstance(use, dict)
        ],
        "speaking_practice": [
            item(
                "guided-output",
                {
                    "instruction": output.get("instruction", ""),
                    "patterns": output.get("patterns", []),
                },
            )
        ]
        if output
        else [],
        "mini_exercises": [
            item(
                "expression-comparison",
                {
                    "exercise_type": "comparison",
                    "intro": comparison.get("intro", ""),
                    "items": comparison.get("items", []),
                },
            )
        ]
        if comparison
        else [
            item(
                "complete-the-pattern",
                {
                    "exercise_type": "sentence_completion",
                    "instruction": output.get("instruction", ""),
                    "patterns": output.get("patterns", []),
                },
            )
        ]
        if output
        else [],
        "useful_tips": [
            item(
                "recap",
                {"summary": recap.get("summary", ""), "key_sentence": recap.get("key_sentence")},
            )
        ]
        if recap
        else [],
        "extended_reading": [
            item(
                "usage-notes",
                {"intro": usage.get("intro", ""), "uses": uses},
            )
        ]
        if usage
        else [],
    }


def insert_lesson_content(connection, lesson, sections, replace=False):
    existing = connection.execute(
        select(m.learning_lesson_section.c.id).where(
            m.learning_lesson_section.c.lesson_id == lesson["id"]
        )
    ).first()
    if existing:
        if not replace:
            return False
        connection.execute(
            m.learning_lesson_section.delete().where(
                m.learning_lesson_section.c.lesson_id == lesson["id"]
            )
        )

    for section_code, (title, title_en, sort_order) in SECTION_META.items():
        section_id = connection.execute(
            m.learning_lesson_section.insert().values(
                lesson_id=lesson["id"],
                section_code=section_code,
                title=title,
                title_en=title_en,
                sort_order=sort_order,
                status="published",
                created_by=lesson["created_by"],
                updated_by=lesson["updated_by"] or lesson["created_by"],
            )
        ).inserted_primary_key[0]
        for row in sections.get(section_code, []):
            connection.execute(
                m.learning_lesson_item.insert().values(
                    section_id=section_id,
                    item_code=row["item_code"],
                    item_order=row["item_order"],
                    title=row["title"],
                    payload_json=encode(row["payload"]),
                    status="published",
                    created_by=lesson["created_by"],
                    updated_by=lesson["updated_by"] or lesson["created_by"],
                )
            ).inserted_primary_key[0]
    connection.execute(
        m.learning_material_lesson.update()
        .where(m.learning_material_lesson.c.id == lesson["id"])
        .values(lesson_schema_version=2, content_status="published")
    )
    return True


def load_idiomatic_lessons(connection):
    lessons = connection.execute(
        select(m.learning_material_lesson)
        .join(m.learning_material, m.learning_material.c.id == m.learning_material_lesson.c.material_id)
        .where(m.learning_material.c.material_code.like("idiomatic-everyday-english%"))
    ).mappings().all()
    lesson_ids = [lesson["id"] for lesson in lessons]
    blocks_by_lesson = defaultdict(list)
    for block in connection.execute(
        select(m.courseware_block)
        .where(m.courseware_block.c.material_lesson_id.in_(lesson_ids))
        .order_by(m.courseware_block.c.sort_order, m.courseware_block.c.id)
    ).mappings():
        blocks_by_lesson[block["material_lesson_id"]].append(block)
    return [
        (lesson, idiomatic_sections(blocks_by_lesson[lesson["id"]]))
        for lesson in lessons
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write migrated generic lesson content.")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing generic sections for the selected lessons.",
    )
    args = parser.parse_args()
    if args.replace and not args.apply:
        parser.error("--replace requires --apply")

    engine = make_engine(Settings().database_url)
    with engine.begin() as connection:
        idiomatic = load_idiomatic_lessons(connection)
        candidates = [("idiomatic English", *row) for row in idiomatic]
        existing = sum(
            connection.execute(
                select(m.learning_lesson_section.c.id).where(
                    m.learning_lesson_section.c.lesson_id == lesson["id"]
                )
            ).first()
            is not None
            for _, lesson, _ in candidates
        )
        print(f"idiomatic_english_lessons={len(idiomatic)}")
        print(f"already_migrated={existing}")
        if not args.apply:
            print("Dry run only. Re-run with --apply to write generic lesson content.")
            return

        migrated = 0
        skipped = 0
        for _, lesson, sections in candidates:
            if insert_lesson_content(connection, lesson, sections, replace=args.replace):
                migrated += 1
            else:
                skipped += 1
        print(f"migrated={migrated}")
        print(f"skipped={skipped}")


if __name__ == "__main__":
    main()
