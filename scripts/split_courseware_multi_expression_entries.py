#!/usr/bin/env python3
"""Rebuild generated courseware cards that contain safely splittable headwords.

Examples:

    .venv/bin/python scripts/split_courseware_multi_expression_entries.py \
      --note-item-id 334 --apply

Without ``--apply`` the command only shows the independent lessons that would
be produced.  A note is eligible only when its source explicitly maps every
slash-separated expression to a Chinese definition.
"""

import argparse
from pathlib import Path
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


def generated_targets(db, note_item_ids, material_id=None):
    conditions = [
        m.courseware_block_source.c.source_resource == "english_note_item",
        m.courseware_block_source.c.source_reference_id.in_(note_item_ids),
    ]
    if material_id is not None:
        conditions.append(m.learning_material.c.id == material_id)
    return db.execute(
        select(
            m.english_note_item.c.id.label("note_item_id"),
            m.english_note_item.c.created_by,
            m.english_note_item.c.updated_by,
            m.learning_material.c.id.label("material_id"),
            m.learning_material.c.topic_id,
            m.learning_material.c.title.label("material_title"),
        )
        .select_from(
            m.courseware_block_source
            .join(m.courseware_block)
            .join(
                m.learning_material_lesson,
                m.learning_material_lesson.c.id == m.courseware_block.c.material_lesson_id,
            )
            .join(
                m.learning_material,
                m.learning_material.c.id == m.learning_material_lesson.c.material_id,
            )
            .join(
                m.english_note_item,
                m.english_note_item.c.id == m.courseware_block_source.c.source_reference_id,
            )
        )
        .where(*conditions)
        .group_by(
            m.english_note_item.c.id,
            m.english_note_item.c.created_by,
            m.english_note_item.c.updated_by,
            m.learning_material.c.id,
            m.learning_material.c.topic_id,
            m.learning_material.c.title,
        )
        .order_by(m.learning_material.c.id, m.english_note_item.c.id)
    ).mappings().all()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--note-item-id",
        type=int,
        action="append",
        required=True,
        help="source english_note_item ID; repeat the option for more than one item",
    )
    parser.add_argument("--material-id", type=int, help="limit rebuilding to one target material")
    parser.add_argument("--apply", action="store_true", help="write rebuilt lessons to the database")
    args = parser.parse_args()

    engine = make_engine(Settings().database_url)
    with Session(engine) as db:
        service = NoteCoursewareService(db)
        targets = generated_targets(db, args.note_item_id, args.material_id)
        if not targets:
            print("No generated courseware lessons matched the requested source item IDs.")
            return
        changed = 0
        for target in targets:
            preview = service.preview(target["note_item_id"])
            phrases = [entry["phrase"] for entry in preview["entries"]]
            if not preview["split"]:
                print(
                    f"Skip note item #{target['note_item_id']} in {target['material_title']}: "
                    "the source does not have a safe per-expression definition map."
                )
                continue
            print(
                f"Note item #{target['note_item_id']} in {target['material_title']}: "
                + "、".join(phrases)
            )
            if args.apply:
                result = service.generate(
                    target["note_item_id"],
                    target["topic_id"],
                    {"id": target["updated_by"] or target["created_by"]},
                    target["material_id"],
                )
                print(
                    "  rebuilt lesson IDs: "
                    + ", ".join(str(lesson["lesson_id"]) for lesson in result["lessons"])
                )
                changed += 1
        if args.apply:
            print(f"Rebuilt {changed} courseware source item(s).")
        else:
            print("Dry run only. Re-run with --apply to write these lessons.")


if __name__ == "__main__":
    main()
