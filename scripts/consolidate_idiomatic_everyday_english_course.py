#!/usr/bin/env python3
"""Consolidate the monthly idiomatic-English courses into one course.

The series keeps its individual monthly materials and lessons.  This command
creates one ordered course-to-material mapping for all of them, keeps the
lowest existing course ID, and safely folds course references into that row.

Without ``--apply`` it only reports the planned result.  With ``--apply`` it
updates the configured database in one transaction.

Examples:

    .venv/bin/python scripts/consolidate_idiomatic_everyday_english_course.py
    .venv/bin/python scripts/consolidate_idiomatic_everyday_english_course.py --apply
"""

import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Any

from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import models as m  # noqa: E402
from app.core.config import Settings  # noqa: E402
from app.core.database import make_engine  # noqa: E402


SERIES_TITLE = "地道英语日积月累"
SERIES_TOPIC_CODE = "phrase-courseware"
SERIES_COURSE_CODE = "idiomatic-everyday-english-course"
MONTH_TITLE = re.compile(r"【\s*(\d{4})年\s*(\d{1,2})月\s*】")


@dataclass
class ConsolidationPlan:
    topic: dict[str, Any]
    courses: list[dict[str, Any]]
    canonical: dict[str, Any]
    materials: list[dict[str, Any]]
    reference_counts: dict[str, int]

    @property
    def course_ids(self):
        return [course["id"] for course in self.courses]

    @property
    def obsolete_course_ids(self):
        return [course_id for course_id in self.course_ids if course_id != self.canonical["id"]]


def rows(db, statement):
    return [dict(row) for row in db.execute(statement).mappings().all()]


def first_nonempty(rows_, field, fallback=None):
    for row in rows_:
        value = row.get(field)
        if value is not None:
            return value
    return fallback


def earliest(rows_, field):
    values = [row[field] for row in rows_ if row.get(field) is not None]
    return min(values) if values else None


def latest(rows_, field):
    values = [row[field] for row in rows_ if row.get(field) is not None]
    return max(values) if values else None


def material_order(material):
    match = MONTH_TITLE.search(material["title"] or "")
    if match:
        return (0, int(match.group(1)), int(match.group(2)), material["id"])
    return (1, int(material["sort_order"] or 0), material["id"], material["id"])


def locked_rows(db, table, course_ids):
    return rows(
        db,
        select(table)
        .where(table.c.course_id.in_(course_ids))
        .with_for_update(),
    )


def build_plan(db):
    topic = db.execute(
        select(m.learning_topic)
        .where(m.learning_topic.c.topic_code == SERIES_TOPIC_CODE)
        .with_for_update()
    ).mappings().one_or_none()
    if not topic:
        raise RuntimeError(f"Learning topic '{SERIES_TOPIC_CODE}' does not exist.")
    topic = dict(topic)

    materials = rows(
        db,
        select(m.learning_material)
        .where(
            m.learning_material.c.topic_id == topic["id"],
            m.learning_material.c.title.like(f"{SERIES_TITLE}%"),
        )
        .order_by(m.learning_material.c.id)
        .with_for_update(),
    )
    if not materials:
        raise RuntimeError(f"No '{SERIES_TITLE}' materials exist in topic #{topic['id']}.")
    materials.sort(key=material_order)
    material_ids = [material["id"] for material in materials]

    mapping_rows = rows(
        db,
        select(m.learning_course_material)
        .where(m.learning_course_material.c.material_id.in_(material_ids))
        .with_for_update(),
    )
    mapped_course_ids = {row["course_id"] for row in mapping_rows}
    legacy_course_ids = set(
        db.scalars(
            select(m.learning_course.c.id)
            .where(
                m.learning_course.c.material_id.in_(material_ids),
            )
            .with_for_update()
        ).all()
    )
    course_ids = mapped_course_ids | legacy_course_ids
    if not course_ids:
        raise RuntimeError("The series materials are not attached to any course.")

    courses = rows(
        db,
        select(m.learning_course)
        .where(m.learning_course.c.id.in_(course_ids))
        .order_by(m.learning_course.c.id)
        .with_for_update(),
    )
    topic_course_ids = set(
        db.scalars(
            select(m.learning_topic_course.c.course_id).where(
                m.learning_topic_course.c.topic_id == topic["id"],
                m.learning_topic_course.c.course_id.in_(course_ids),
            )
        ).all()
    )
    missing_topic_associations = set(course_ids) - topic_course_ids
    if missing_topic_associations:
        raise RuntimeError(
            "A series material is linked to a course not associated with this topic: "
            + ", ".join(map(str, sorted(missing_topic_associations)))
        )
    unrelated_courses = [
        course["id"]
        for course in courses
        if not str(course["title"] or "").startswith(SERIES_TITLE)
    ]
    if unrelated_courses:
        raise RuntimeError(
            "A series material is also linked to a non-series course: "
            + ", ".join(map(str, unrelated_courses))
        )
    direct_content_courses = [
        course["id"]
        for course in courses
        if course["content_resource"]
        or course["content_reference_id"] is not None
        or course["content_json"]
    ]
    if direct_content_courses:
        raise RuntimeError(
            "A series course has direct content and cannot safely be consolidated: "
            + ", ".join(map(str, direct_content_courses))
        )

    all_mappings = locked_rows(db, m.learning_course_material, list(course_ids))
    unexpected_mappings = [
        row for row in all_mappings if row["material_id"] not in set(material_ids)
    ]
    if unexpected_mappings:
        raise RuntimeError(
            "A series course also has a material outside this series: "
            + ", ".join(str(row["material_id"]) for row in unexpected_mappings)
        )
    unexpected_legacy_materials = [
        course["id"]
        for course in courses
        if course["material_id"] is not None and course["material_id"] not in set(material_ids)
    ]
    if unexpected_legacy_materials:
        raise RuntimeError(
            "A series course has a legacy material outside this series: "
            + ", ".join(map(str, unexpected_legacy_materials))
        )

    canonical = courses[0]
    code_conflicts = list(
        db.scalars(
            select(m.learning_course.c.id).where(
                m.learning_course.c.course_code == SERIES_COURSE_CODE,
                m.learning_course.c.id != canonical["id"],
            )
        ).all()
    )
    if code_conflicts:
        raise RuntimeError(
            f"Course code '{SERIES_COURSE_CODE}' is already used by course(s): "
            + ", ".join(map(str, code_conflicts))
        )

    reference_counts = {
        "membership_benefit_course": len(
            locked_rows(db, m.membership_benefit_course, list(course_ids))
        ),
        "learning_user_course": len(locked_rows(db, m.learning_user_course, list(course_ids))),
        "learning_progress": len(locked_rows(db, m.learning_progress, list(course_ids))),
        "learning_study_session": len(
            locked_rows(db, m.learning_study_session, list(course_ids))
        ),
    }
    return ConsolidationPlan(
        topic=topic,
        courses=courses,
        canonical=canonical,
        materials=materials,
        reference_counts=reference_counts,
    )


def merge_membership_bindings(db, course_ids, canonical_id, actor_id):
    rows_ = locked_rows(db, m.membership_benefit_course, course_ids)
    groups = defaultdict(list)
    for row in rows_:
        groups[(row["benefit_id"], row["access_action"])].append(row)

    removed = 0
    for grouped_rows in groups.values():
        keeper = next(
            (row for row in grouped_rows if row["course_id"] == canonical_id),
            min(grouped_rows, key=lambda row: row["id"]),
        )
        duplicate_ids = [row["id"] for row in grouped_rows if row["id"] != keeper["id"]]
        if duplicate_ids:
            db.execute(
                delete(m.membership_benefit_course).where(
                    m.membership_benefit_course.c.id.in_(duplicate_ids)
                )
            )
            removed += len(duplicate_ids)
        values = {
            "course_id": canonical_id,
            "is_enabled": int(any(row["is_enabled"] for row in grouped_rows)),
            "sort_order": min(int(row["sort_order"] or 0) for row in grouped_rows),
            "updated_at": func.now(),
        }
        if actor_id is not None:
            values["updated_by"] = actor_id
        db.execute(
            update(m.membership_benefit_course)
            .where(m.membership_benefit_course.c.id == keeper["id"])
            .values(**values)
        )
    return {"rows": len(rows_), "removed_duplicates": removed}


def merge_user_courses(db, course_ids, canonical_id):
    rows_ = locked_rows(db, m.learning_user_course, course_ids)
    groups = defaultdict(list)
    for row in rows_:
        groups[row["user_id"]].append(row)

    removed = 0
    for grouped_rows in groups.values():
        keeper = next(
            (row for row in grouped_rows if row["course_id"] == canonical_id),
            min(grouped_rows, key=lambda row: row["id"]),
        )
        source_row = next(
            (row for row in grouped_rows if row["source_membership_id"] is not None),
            keeper,
        )
        is_active = any(row["status"] == "active" for row in grouped_rows)
        duplicate_ids = [row["id"] for row in grouped_rows if row["id"] != keeper["id"]]
        if duplicate_ids:
            db.execute(
                delete(m.learning_user_course).where(m.learning_user_course.c.id.in_(duplicate_ids))
            )
            removed += len(duplicate_ids)
        db.execute(
            update(m.learning_user_course)
            .where(m.learning_user_course.c.id == keeper["id"])
            .values(
                course_id=canonical_id,
                source=source_row["source"],
                source_membership_id=source_row["source_membership_id"],
                status="active" if is_active else keeper["status"],
                enrolled_at=earliest(grouped_rows, "enrolled_at"),
                last_opened_at=latest(grouped_rows, "last_opened_at"),
                archived_at=None if is_active else latest(grouped_rows, "archived_at"),
                updated_at=func.now(),
            )
        )
    return {"rows": len(rows_), "removed_duplicates": removed}


def merge_progress_items(db, source_progress_id, target_progress_id):
    target_items = {
        row["item_key"]: row
        for row in rows(
            db,
            select(m.learning_progress_item)
            .where(m.learning_progress_item.c.progress_id == target_progress_id)
            .with_for_update(),
        )
    }
    source_items = rows(
        db,
        select(m.learning_progress_item)
        .where(m.learning_progress_item.c.progress_id == source_progress_id)
        .with_for_update(),
    )
    for source in source_items:
        target = target_items.get(source["item_key"])
        if target is None:
            db.execute(
                update(m.learning_progress_item)
                .where(m.learning_progress_item.c.id == source["id"])
                .values(progress_id=target_progress_id, updated_at=func.now())
            )
            target_items[source["item_key"]] = source
            continue
        freshest = max(
            (source, target),
            key=lambda row: row["last_studied_at"] or row["created_at"],
        )
        db.execute(
            update(m.learning_progress_item)
            .where(m.learning_progress_item.c.id == target["id"])
            .values(
                item_type=freshest["item_type"],
                item_reference_id=freshest["item_reference_id"],
                is_completed=int(bool(source["is_completed"]) or bool(target["is_completed"])),
                last_position_seconds=max(
                    int(source["last_position_seconds"] or 0),
                    int(target["last_position_seconds"] or 0),
                ),
                attempt_count=int(source["attempt_count"] or 0)
                + int(target["attempt_count"] or 0),
                score=freshest["score"]
                if freshest["score"] is not None
                else target["score"],
                last_studied_at=latest((source, target), "last_studied_at"),
                completed_at=earliest((source, target), "completed_at"),
                updated_at=func.now(),
            )
        )
        db.execute(
            delete(m.learning_progress_item).where(m.learning_progress_item.c.id == source["id"])
        )


def merge_progress(db, course_ids, canonical_id):
    rows_ = locked_rows(db, m.learning_progress, course_ids)
    groups = defaultdict(list)
    for row in rows_:
        groups[row["user_id"]].append(row)

    removed = 0
    for grouped_rows in groups.values():
        keeper = next(
            (row for row in grouped_rows if row["course_id"] == canonical_id),
            min(grouped_rows, key=lambda row: row["id"]),
        )
        for source in grouped_rows:
            if source["id"] == keeper["id"]:
                continue
            merge_progress_items(db, source["id"], keeper["id"])
            db.execute(
                update(m.learning_study_session)
                .where(m.learning_study_session.c.progress_id == source["id"])
                .values(progress_id=keeper["id"], course_id=canonical_id, updated_at=func.now())
            )

        if len(grouped_rows) == 1 and keeper["course_id"] == canonical_id:
            continue
        completed_item_count = db.scalar(
            select(func.count())
            .select_from(m.learning_progress_item)
            .where(
                m.learning_progress_item.c.progress_id == keeper["id"],
                m.learning_progress_item.c.is_completed == 1,
            )
        ) or 0
        total_item_count = max(
            sum(int(row["total_item_count"] or 0) for row in grouped_rows),
            completed_item_count,
        )
        freshest = max(
            grouped_rows,
            key=lambda row: row["last_studied_at"] or row["created_at"],
        )
        db.execute(
            update(m.learning_progress)
            .where(m.learning_progress.c.id == keeper["id"])
            .values(
                course_id=canonical_id,
                status=(
                    "completed"
                    if total_item_count and completed_item_count >= total_item_count
                    else "in_progress"
                ),
                total_item_count=total_item_count,
                completed_item_count=completed_item_count,
                last_item_key=freshest["last_item_key"],
                last_item_id=freshest["last_item_id"],
                last_position_seconds=freshest["last_position_seconds"],
                started_at=earliest(grouped_rows, "started_at"),
                last_studied_at=latest(grouped_rows, "last_studied_at"),
                completed_at=(
                    latest(grouped_rows, "completed_at")
                    if total_item_count and completed_item_count >= total_item_count
                    else None
                ),
                accumulated_seconds=sum(
                    int(row["accumulated_seconds"] or 0) for row in grouped_rows
                ),
                updated_at=func.now(),
            )
        )
        duplicate_ids = [row["id"] for row in grouped_rows if row["id"] != keeper["id"]]
        if duplicate_ids:
            db.execute(delete(m.learning_progress).where(m.learning_progress.c.id.in_(duplicate_ids)))
            removed += len(duplicate_ids)
    return {"rows": len(rows_), "removed_duplicates": removed}


def apply_plan(db, plan, actor_id):
    canonical_id = plan.canonical["id"]
    course_ids = plan.course_ids
    material_ids = [material["id"] for material in plan.materials]
    actor_id = actor_id if actor_id is not None else (
        plan.canonical["updated_by"] or plan.canonical["created_by"]
    )

    memberships = merge_membership_bindings(db, course_ids, canonical_id, actor_id)
    user_courses = merge_user_courses(db, course_ids, canonical_id)
    progress = merge_progress(db, course_ids, canonical_id)
    sessions = db.execute(
        update(m.learning_study_session)
        .where(m.learning_study_session.c.course_id.in_(course_ids))
        .values(course_id=canonical_id, updated_at=func.now())
    ).rowcount

    db.execute(
        delete(m.learning_course_material).where(
            m.learning_course_material.c.course_id.in_(course_ids)
        )
    )
    mapping_values = [
        {
            "course_id": canonical_id,
            "material_id": material_id,
            "sort_order": position * 10,
            "created_by": actor_id,
            "updated_by": actor_id,
        }
        for position, material_id in enumerate(material_ids, start=1)
    ]
    db.execute(m.learning_course_material.insert(), mapping_values)

    course_values = {
        "material_id": material_ids[0],
        "course_code": SERIES_COURSE_CODE,
        "title": SERIES_TITLE,
        "sort_order": min(int(course["sort_order"] or 0) for course in plan.courses),
        "updated_at": func.now(),
    }
    if actor_id is not None:
        course_values["updated_by"] = actor_id
    db.execute(
        update(m.learning_course)
        .where(m.learning_course.c.id == canonical_id)
        .values(**course_values)
    )

    if plan.obsolete_course_ids:
        db.execute(
            delete(m.learning_course).where(m.learning_course.c.id.in_(plan.obsolete_course_ids))
        )
    return {
        "canonical_course_id": canonical_id,
        "removed_courses": len(plan.obsolete_course_ids),
        "materials": len(material_ids),
        "membership_bindings": memberships,
        "user_courses": user_courses,
        "progress": progress,
        "study_sessions_repointed": sessions,
    }


def print_plan(plan):
    canonical = plan.canonical
    print(f"Topic #{plan.topic['id']}: {plan.topic['title']}")
    print(
        f"Keep course #{canonical['id']}: {canonical['title']} "
        f"-> {SERIES_TITLE} ({SERIES_COURSE_CODE})"
    )
    print(
        f"Merge {len(plan.courses)} course record(s) into one and keep "
        f"{len(plan.materials)} ordered material(s):"
    )
    for position, material in enumerate(plan.materials, start=1):
        print(f"  {position:>2}. #{material['id']} {material['title']}")
    print(
        "References to rewrite: "
        + ", ".join(
            f"{table}={count}" for table, count in plan.reference_counts.items()
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write the consolidated course")
    parser.add_argument(
        "--actor-id",
        type=int,
        help="administrator ID for updated_by fields; defaults to the kept course's editor",
    )
    args = parser.parse_args()

    engine = make_engine(Settings().database_url)
    with Session(engine) as db:
        plan = build_plan(db)
        print_plan(plan)
        if not args.apply:
            db.rollback()
            print("Dry run only. Re-run with --apply to write the consolidated course.")
            return
        result = apply_plan(db, plan, args.actor_id)
        db.commit()
        print(
            f"Applied: kept course #{result['canonical_course_id']}, removed "
            f"{result['removed_courses']} duplicate course(s), and linked "
            f"{result['materials']} material(s)."
        )
        print(
            "Reference merge: "
            f"membership bindings={result['membership_bindings']['rows']} "
            f"({result['membership_bindings']['removed_duplicates']} duplicate(s) removed), "
            f"user courses={result['user_courses']['rows']} "
            f"({result['user_courses']['removed_duplicates']} duplicate(s) removed), "
            f"progress={result['progress']['rows']} "
            f"({result['progress']['removed_duplicates']} duplicate(s) removed), "
            f"study sessions repointed={result['study_sessions_repointed']}."
        )


if __name__ == "__main__":
    main()
