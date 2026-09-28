#!/usr/bin/env python3
"""Refresh generated phrase lessons with validated real-life dialogue scenes.

The command is intentionally replayable. Without ``--apply`` it reports which
blocks would be refreshed. With ``--apply`` it updates dialogue/output blocks
that fail learner-facing quality rules, and replays the hand-curated situations
for expressions that have them.

Examples:

    .venv/bin/python scripts/repair_courseware_scene_quality.py
    .venv/bin/python scripts/repair_courseware_scene_quality.py --apply
    .venv/bin/python scripts/repair_courseware_scene_quality.py --lesson-id 1187 --apply
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path
import sys

from sqlalchemy import func, select
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import models as m  # noqa: E402
from app.core.config import Settings  # noqa: E402
from app.core.database import make_engine  # noqa: E402
from app.services.courseware import NoteCoursewareService  # noqa: E402
from app.services.courseware_scene_catalog import (  # noqa: E402
    CURATED_REAL_LIFE_EXPRESSION_SCENES,
    CURATED_REAL_LIFE_SCENES,
)


OUTPUT_INSTRUCTION = "先读完整句，再把横线处填成今天要练的关键词。"


def loads(value):
    return json.loads(value or "{}")


def dumps(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def generated_lessons(db, lesson_ids):
    conditions = [
        m.learning_material_lesson.c.lesson_format == "courseware",
        m.courseware_block.c.block_code == "hero",
        m.courseware_block_source.c.source_resource == "english_note_item",
    ]
    if lesson_ids:
        conditions.append(m.learning_material_lesson.c.id.in_(lesson_ids))
    return db.execute(
        select(
            m.learning_material_lesson.c.id.label("lesson_id"),
            m.learning_material_lesson.c.title.label("lesson_title"),
            m.learning_material_lesson.c.lesson_code.label("lesson_code"),
            m.learning_material_lesson.c.created_by.label("lesson_created_by"),
            m.learning_material_lesson.c.updated_by.label("lesson_updated_by"),
            m.english_note_item,
        )
        .select_from(
            m.learning_material_lesson
            .join(
                m.courseware_block,
                m.courseware_block.c.material_lesson_id == m.learning_material_lesson.c.id,
            )
            .join(
                m.courseware_block_source,
                m.courseware_block_source.c.courseware_block_id == m.courseware_block.c.id,
            )
            .join(
                m.english_note_item,
                m.english_note_item.c.id == m.courseware_block_source.c.source_reference_id,
            )
        )
        .where(*conditions)
        .group_by(
            m.learning_material_lesson.c.id,
            m.learning_material_lesson.c.title,
            m.learning_material_lesson.c.created_by,
            m.learning_material_lesson.c.updated_by,
            *m.english_note_item.c,
        )
        .order_by(m.learning_material_lesson.c.id)
    ).mappings().all()


def lesson_blocks(db, lesson_ids):
    result = defaultdict(dict)
    rows = db.execute(
        select(m.courseware_block)
        .where(m.courseware_block.c.material_lesson_id.in_(lesson_ids))
        .order_by(m.courseware_block.c.material_lesson_id, m.courseware_block.c.sort_order)
    ).mappings()
    for row in rows:
        result[row["material_lesson_id"]][row["block_code"]] = dict(row)
    return result


def has_target_expression(lines, phrase):
    for line in lines:
        english = str(line.get("english", ""))
        if NoteCoursewareService._blank_keyword(english, phrase):
            return True
        if NoteCoursewareService._blank_keyword_anchor(english, phrase):
            return True
    return False


def dialogue_needs_repair(payload, phrase):
    lines = payload.get("lines", []) if isinstance(payload, dict) else []
    return (
        NoteCoursewareService.is_low_quality_scene_dialogue(lines)
        or not has_target_expression(lines, phrase)
    )


def dialogue_lines(payload):
    return payload.get("lines", []) if isinstance(payload, dict) else []


def output_needs_repair(payload):
    patterns = payload.get("patterns", []) if isinstance(payload, dict) else []
    return not patterns or not all(
        NoteCoursewareService._is_meaningful_practice_sentence(pattern)
        for pattern in patterns
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lesson-id",
        type=int,
        action="append",
        help="limit review to a lesson ID; repeat for more than one lesson",
    )
    parser.add_argument("--apply", action="store_true", help="write the repaired payloads")
    parser.add_argument("--verbose", action="store_true", help="print every repaired lesson")
    args = parser.parse_args()

    engine = make_engine(Settings().database_url)
    with Session(engine) as db:
        lessons = generated_lessons(db, args.lesson_id or [])
        if not lessons:
            print("No generated courseware lessons matched the selected scope.")
            return
        blocks_by_lesson = lesson_blocks(db, [lesson["lesson_id"] for lesson in lessons])
        service = NoteCoursewareService(db)
        dialogue_changes = []
        output_changes = []
        hero_changes = []
        recap_changes = []
        lesson_changes = []
        quality_dialogue_repairs = 0
        curated_scene_refreshes = 0
        skipped = 0

        for lesson in lessons:
            blocks = blocks_by_lesson[lesson["lesson_id"]]
            hero_block = blocks.get("hero")
            dialogue_block = blocks.get("scene-practice")
            output_block = blocks.get("say-it")
            if not hero_block or not dialogue_block or not output_block:
                skipped += 1
                continue

            hero = loads(hero_block["payload_json"])
            usage = loads(blocks.get("usage", {}).get("payload_json"))
            recap_block = blocks.get("recap")
            recap = loads(recap_block["payload_json"]) if recap_block else {}
            old_dialogue = loads(dialogue_block["payload_json"])
            old_output = loads(output_block["payload_json"])
            stored_phrase = hero.get("phrase", "")
            phrase = service.normalise_courseware_phrase(stored_phrase)
            meaning = hero.get("meaning", "")
            source_item = service.item_for_existing_phrase(dict(lesson), phrase)
            practice_expression = service._practice_expression(source_item, phrase)
            force_curated_scene = (
                source_item.get("id") in CURATED_REAL_LIFE_SCENES
                or (
                    source_item.get("id"),
                    service._expression_key(phrase),
                ) in CURATED_REAL_LIFE_EXPRESSION_SCENES
            )
            needs_dialogue_repair = dialogue_needs_repair(old_dialogue, practice_expression)
            needs_output_repair = output_needs_repair(old_output)
            new_lines = dialogue_lines(old_dialogue)
            if needs_dialogue_repair or force_curated_scene:
                if needs_dialogue_repair:
                    quality_dialogue_repairs += 1
                else:
                    curated_scene_refreshes += 1
                new_lines = service._dialogue_lines(
                    source_item,
                    phrase,
                    meaning,
                    hero.get("key_sentence", {}),
                )
                if NoteCoursewareService.is_low_quality_scene_dialogue(new_lines):
                    raise RuntimeError(
                        f"Generated an invalid scene for lesson #{lesson['lesson_id']}: "
                        f"{lesson['lesson_title']}"
                    )
                if not has_target_expression(new_lines, practice_expression):
                    raise RuntimeError(
                        f"Generated scene does not use '{practice_expression}' for lesson "
                        f"#{lesson['lesson_id']}: {lesson['lesson_title']}"
                    )
                new_dialogue = {
                    **old_dialogue,
                    "scene": old_dialogue.get("scene") or "真实发生的日常场景",
                    "intro": "把表达放进一个前后连得上的真实场景里。",
                    "lines": new_lines,
                }
                dialogue_changes.append((lesson, dialogue_block, new_dialogue))
            if needs_output_repair:
                pairs = service._pairs(
                    f"{source_item.get('explanation') or ''}\n{source_item.get('examples') or ''}"
                )
                new_patterns = service._practice_patterns(
                    source_item,
                    phrase,
                    meaning,
                    new_lines,
                    usage.get("uses", []),
                    pairs,
                )
                new_output = {
                    **old_output,
                    "instruction": OUTPUT_INSTRUCTION,
                    "patterns": new_patterns,
                }
                output_changes.append((lesson, output_block, new_output))
            if phrase != stored_phrase:
                new_hero = {**hero, "phrase": phrase}
                hero_changes.append((lesson, hero_block, new_hero))
                if recap_block:
                    recap_changes.append((
                        lesson,
                        recap_block,
                        {
                            **recap,
                            "summary": service._recap_summary(phrase, meaning),
                        },
                    ))
                if lesson["lesson_title"] == stored_phrase:
                    new_code = (lesson.get("lesson_code") or "").replace(
                        stored_phrase.casefold(), phrase.casefold()
                    )
                    lesson_changes.append((lesson, phrase, new_code))

        print(
            f"Reviewed {len(lessons)} lesson(s): "
            f"{len(dialogue_changes)} dialogue scene(s) selected "
            f"({quality_dialogue_repairs} quality repair(s), "
            f"{curated_scene_refreshes} curated refresh(es)), "
            f"{len(output_changes)} output block(s), "
            f"{len(hero_changes)} corrected phrase card(s); "
            f"{skipped} incomplete lesson(s) skipped."
        )
        if args.verbose:
            for lesson, _, payload in dialogue_changes:
                print(
                    f"DIALOGUE #{lesson['lesson_id']} {lesson['lesson_title']}: "
                    f"{payload['lines'][0]['english']} / {payload['lines'][1]['english']}"
                )
            for lesson, _, payload in output_changes:
                print(
                    f"OUTPUT #{lesson['lesson_id']} {lesson['lesson_title']}: "
                    + " | ".join(payload["patterns"])
                )
        if not args.apply:
            print("Dry run only. Re-run with --apply to write the refreshed payloads.")
            return

        for lesson, block, payload in dialogue_changes + output_changes + hero_changes + recap_changes:
            actor_id = lesson["lesson_updated_by"] or lesson["lesson_created_by"] or lesson.get("updated_by")
            db.execute(
                m.courseware_block.update()
                .where(m.courseware_block.c.id == block["id"])
                .values(payload_json=dumps(payload), updated_by=actor_id, updated_at=func.now())
            )
        for lesson, title, lesson_code in lesson_changes:
            db.execute(
                m.learning_material_lesson.update()
                .where(m.learning_material_lesson.c.id == lesson["lesson_id"])
                .values(
                    title=title,
                    lesson_code=lesson_code,
                    updated_by=lesson["lesson_updated_by"] or lesson["lesson_created_by"],
                    updated_at=func.now(),
                )
            )
        db.commit()
        print(
            f"Wrote {len(dialogue_changes)} dialogue scene(s), "
            f"{len(output_changes)} output block(s), and "
            f"{len(hero_changes)} corrected phrase card(s)."
        )


if __name__ == "__main__":
    main()
