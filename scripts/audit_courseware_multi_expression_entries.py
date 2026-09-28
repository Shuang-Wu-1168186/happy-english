#!/usr/bin/env python3
"""Remove generated collection cards or rebuild them as individual lessons.

The audit only touches courseware generated from ``english_note_item``:

* source notes with an explicit per-expression Chinese meaning are rebuilt as
  one lesson per expression;
* a trailing IPA transcription is removed from an otherwise single headword;
* an unresolved collection is removed from the generated material, while its
  original note remains untouched for later editorial splitting.

Examples:

    .venv/bin/python scripts/audit_courseware_multi_expression_entries.py
    .venv/bin/python scripts/audit_courseware_multi_expression_entries.py --apply
    .venv/bin/python scripts/audit_courseware_multi_expression_entries.py --lesson-id 1156 --apply
"""

import argparse
import json
from collections import Counter
from pathlib import Path
import re
import sys

from sqlalchemy import select
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import models as m  # noqa: E402
from app.core.config import Settings  # noqa: E402
from app.core.database import make_engine  # noqa: E402
from app.services.courseware import NoteCoursewareService  # noqa: E402


def loads(value, fallback):
    try:
        return json.loads(value) if value else fallback
    except (TypeError, ValueError):
        return fallback


def generated_hero_targets(db, lesson_ids):
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
            m.learning_material_lesson.c.created_by.label("lesson_created_by"),
            m.learning_material_lesson.c.updated_by.label("lesson_updated_by"),
            m.learning_material.c.id.label("material_id"),
            m.learning_material.c.topic_id.label("topic_id"),
            m.courseware_block.c.payload_json.label("hero_payload_json"),
            m.courseware_block_source.c.source_locator_json.label("source_locator_json"),
            m.english_note_item.c.id.label("note_item_id"),
        )
        .select_from(
            m.learning_material_lesson
            .join(m.learning_material)
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
            m.learning_material.c.id,
            m.learning_material.c.topic_id,
            m.courseware_block.c.payload_json,
            m.courseware_block_source.c.source_locator_json,
            m.english_note_item.c.id,
        )
        .order_by(m.learning_material_lesson.c.id)
    ).mappings().all()


def has_separator(value):
    return bool(re.search(r"[|/]", value or ""))


def classify_target(service, target, source_item):
    """Return ``(action, entries)`` for one generated lesson, or ``None``."""
    locator = loads(target["source_locator_json"], None)
    if isinstance(locator, dict) and locator.get("kind") == "split_expression":
        return None

    hero = loads(target["hero_payload_json"], {})
    stored_phrase = str(hero.get("phrase") or "")
    title = str(target["lesson_title"] or "")
    split_entries = service._split_expression_entries(source_item)
    is_collection = service.has_unresolved_expression_collection(source_item)
    is_phrase_collection = stored_phrase == "Phrase collection"
    display_has_separator = has_separator(stored_phrase) or has_separator(title)

    if split_entries and (display_has_separator or is_phrase_collection or service._collection_expression_terms(source_item)):
        return "split", service._preview_entries(source_item)
    if is_collection or is_phrase_collection:
        return "remove", []

    # An IPA transcription is not a second expression.  Rebuild only this
    # safely normalisable case so its title, hero and recap use the headword.
    source_phrase = service._source_phrase(source_item)
    normalised_source = service._strip_pronunciation_notation(source_phrase)
    normalised_phrase = service._card_phrase(source_item)
    if (
        display_has_separator
        and normalised_source != service._single_line(source_phrase)
        and normalised_phrase
        and normalised_phrase != stored_phrase
    ):
        return "normalise", service._preview_entries(source_item)
    if display_has_separator:
        return "remove", []
    return None


def rebuild_target(db, service, target, source_item, entries):
    material = db.execute(
        select(m.learning_material).where(m.learning_material.c.id == target["material_id"])
    ).mappings().one()
    actor = {"id": target["lesson_updated_by"] or target["lesson_created_by"]}
    rebuilt = [
        service._save_generated_entry(target["material_id"], source_item, entry, actor)
        for entry in entries
    ]
    service._ensure_generated_course(
        target["material_id"], material, target["topic_id"], actor
    )
    return rebuilt


def remove_target(db, lesson_id):
    block_ids = select(m.courseware_block.c.id).where(
        m.courseware_block.c.material_lesson_id == lesson_id
    )
    db.execute(m.courseware_block_source.delete().where(
        m.courseware_block_source.c.courseware_block_id.in_(block_ids)
    ))
    db.execute(m.courseware_block.delete().where(
        m.courseware_block.c.material_lesson_id == lesson_id
    ))
    db.execute(m.learning_material_lesson.delete().where(
        m.learning_material_lesson.c.id == lesson_id
    ))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lesson-id", type=int, action="append",
        help="limit the audit to a generated lesson; repeat for more than one",
    )
    parser.add_argument("--apply", action="store_true", help="write the audited changes")
    parser.add_argument("--verbose", action="store_true", help="show every affected lesson")
    args = parser.parse_args()

    engine = make_engine(Settings().database_url)
    with Session(engine) as db:
        service = NoteCoursewareService(db)
        targets = generated_hero_targets(db, args.lesson_id or [])
        actions = []
        for target in targets:
            source_item = dict(service._item(target["note_item_id"]))
            result = classify_target(service, target, source_item)
            if result is not None:
                action, entries = result
                actions.append((action, target, source_item, entries))

        counts = Counter(action for action, *_ in actions)
        projected_lessons = sum(
            len(entries) for action, _, _, entries in actions
            if action in {"split", "normalise"}
        )
        print(
            f"Reviewed {len(targets)} generated lesson(s): "
            f"{counts['split']} source group(s) will become {sum(len(entries) for action, _, _, entries in actions if action == 'split')} lesson(s), "
            f"{counts['normalise']} pronunciation label(s) will be normalised, "
            f"{counts['remove']} unresolved collection card(s) will be removed."
        )
        if args.verbose:
            for action, target, _, entries in actions:
                suffix = "、".join(entry["phrase"] for entry in entries)
                print(
                    f"{action.upper()} #{target['lesson_id']} "
                    f"(note #{target['note_item_id']}): {target['lesson_title']}"
                    + (f" -> {suffix}" if suffix else "")
                )
        if not args.apply:
            print("Dry run only. Re-run with --apply to write the audited changes.")
            return

        obsolete_combined_cards = 0
        for action, target, source_item, entries in actions:
            if action == "remove":
                remove_target(db, target["lesson_id"])
            else:
                rebuilt = rebuild_target(db, service, target, source_item, entries)
                # Most first split entries reuse the old lesson ID.  Older
                # cards sometimes used a legacy slug that cannot be matched
                # after source corrections, in which case a new first lesson
                # is created.  Delete that obsolete combined card explicitly.
                if target["lesson_id"] not in {lesson["lesson_id"] for lesson in rebuilt}:
                    remove_target(db, target["lesson_id"])
                    obsolete_combined_cards += 1
        db.commit()
        print(
            f"Applied {counts['split']} split rebuild(s), "
            f"{counts['normalise']} label normalisation(s), and "
            f"{counts['remove'] + obsolete_combined_cards} removal(s); "
            f"{projected_lessons} rebuilt learner-facing lesson(s)."
        )


if __name__ == "__main__":
    main()
