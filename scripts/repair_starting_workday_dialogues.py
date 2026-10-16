#!/usr/bin/env python3
"""Replace disconnected dialogue fragments in Starting the Workday.

The script is replayable.  It targets a material and lesson codes rather than
database IDs, so the same command can repair local and production content.

Examples:

    .venv/bin/python scripts/repair_starting_workday_dialogues.py
    .venv/bin/python scripts/repair_starting_workday_dialogues.py --apply
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from sqlalchemy import func, select

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import models as m  # noqa: E402
from app.core.config import Settings  # noqa: E402
from app.core.database import make_engine  # noqa: E402
from app.curriculum.starting_workday_dialogues import (  # noqa: E402
    LESSON_DIALOGUES,
    MATERIAL_CODE,
    validate_dialogues,
)


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def load_lessons(connection):
    material = connection.execute(
        select(m.learning_material).where(m.learning_material.c.material_code == MATERIAL_CODE)
    ).mappings().first()
    if not material:
        raise RuntimeError(f"Material '{MATERIAL_CODE}' was not found.")

    lessons = connection.execute(
        select(m.learning_material_lesson)
        .where(m.learning_material_lesson.c.material_id == material["id"])
        .order_by(m.learning_material_lesson.c.sort_order, m.learning_material_lesson.c.id)
    ).mappings().all()
    by_code = {lesson["lesson_code"]: dict(lesson) for lesson in lessons}
    unexpected = sorted(set(by_code) - set(LESSON_DIALOGUES))
    missing = sorted(set(LESSON_DIALOGUES) - set(by_code))
    if missing or unexpected:
        details = []
        if missing:
            details.append(f"missing lesson codes: {', '.join(missing)}")
        if unexpected:
            details.append(f"unexpected lesson codes: {', '.join(unexpected)}")
        raise RuntimeError("Target material does not match this repair: " + "; ".join(details))
    return by_code


def dialogue_section(connection, lesson):
    section = connection.execute(
        select(m.learning_lesson_section).where(
            m.learning_lesson_section.c.lesson_id == lesson["id"],
            m.learning_lesson_section.c.section_code == "situational_dialogues",
        )
    ).mappings().first()
    if not section:
        raise RuntimeError(f"Lesson '{lesson['lesson_code']}' has no situational_dialogues section.")
    return dict(section)


def item_rows(connection, section_id):
    return connection.execute(
        select(m.learning_lesson_item)
        .where(m.learning_lesson_item.c.section_id == section_id)
        .order_by(m.learning_lesson_item.c.item_order, m.learning_lesson_item.c.id)
    ).mappings().all()


def replace_dialogues(connection, lessons):
    changes = []
    for lesson_code, lesson in lessons.items():
        section = dialogue_section(connection, lesson)
        old_items = item_rows(connection, section["id"])
        new_dialogues = LESSON_DIALOGUES[lesson_code]
        actor_id = lesson["updated_by"] or lesson["created_by"]
        connection.execute(
            m.learning_lesson_item.delete().where(
                m.learning_lesson_item.c.section_id == section["id"]
            )
        )
        for index, payload in enumerate(new_dialogues, start=1):
            connection.execute(
                m.learning_lesson_item.insert().values(
                    section_id=section["id"],
                    item_code=f"dialogue-{index}",
                    item_order=index * 10,
                    title=payload["title"],
                    payload_json=encode(payload),
                    status="published",
                    created_by=actor_id,
                    updated_by=actor_id,
                )
            )
        connection.execute(
            m.learning_material_lesson.update()
            .where(m.learning_material_lesson.c.id == lesson["id"])
            .values(
                content_status="published",
                is_published=1,
                updated_by=actor_id,
                updated_at=func.now(),
            )
        )
        changes.append((lesson_code, len(old_items), len(new_dialogues)))
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write the hand-authored dialogue scenes")
    args = parser.parse_args()

    errors = validate_dialogues()
    if errors:
        raise RuntimeError("Invalid dialogue source:\n- " + "\n- ".join(errors))

    engine = make_engine(Settings().database_url)
    try:
        with engine.begin() as connection:
            lessons = load_lessons(connection)
            preview = []
            for lesson_code, lesson in lessons.items():
                section = dialogue_section(connection, lesson)
                preview.append(
                    (lesson_code, len(item_rows(connection, section["id"])), len(LESSON_DIALOGUES[lesson_code]))
                )

            print(
                f"Validated {len(LESSON_DIALOGUES)} lessons and "
                f"{sum(len(items) for items in LESSON_DIALOGUES.values())} dialogue scenes."
            )
            for lesson_code, old_count, new_count in preview:
                print(f"{lesson_code}: {old_count} existing scene(s) -> {new_count} hand-authored scene(s)")
            if not args.apply:
                print("Dry run only. Re-run with --apply to update the database.")
                return

            changes = replace_dialogues(connection, lessons)
            print(f"Updated {len(changes)} lessons and {sum(new for _, _, new in changes)} dialogue scenes.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
