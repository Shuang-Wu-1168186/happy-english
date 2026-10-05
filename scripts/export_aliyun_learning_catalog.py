#!/usr/bin/env python3
"""Export the current learning catalogue as a portable MySQL content sync.

The generated SQL is deliberately keyed by stable business codes instead of
local numeric IDs.  It can therefore be applied to an existing Aliyun MySQL
instance after the schema migration bundle has completed.

It exports platform catalogue/configuration data only.  It does not export
users, passwords, sessions, progress, login audits, or user memberships.

Usage:
    PYTHONPATH=. .venv/bin/python scripts/export_aliyun_learning_catalog.py
    PYTHONPATH=. .venv/bin/python scripts/export_aliyun_learning_catalog.py \
        --output sql/deploy/20261005_learning_catalog_data.sql
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import numbers
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.engine import Connection

from app import models as m
from app.core.config import Settings
from app.core.database import make_engine


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "sql" / "deploy" / "20261005_learning_catalog_data.sql"
DEFAULT_MANIFEST = ROOT / "sql" / "deploy" / "20261005_learning_catalog_manifest.json"


@dataclass(frozen=True)
class TemporaryTable:
    name: str
    columns: tuple[tuple[str, str], ...]
    rows: list[dict[str, Any]]

    @property
    def column_names(self) -> tuple[str, ...]:
        return tuple(name for name, _ in self.columns if name != "PRIMARY KEY")


def select_rows(connection: Connection, statement) -> list[dict[str, Any]]:
    return [dict(row) for row in connection.execute(statement).mappings().all()]


def as_mysql_literal(value: Any) -> str:
    """Return a UTF-8-safe literal without relying on SQL string escaping."""

    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, Decimal)):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        value = value.isoformat(sep=" ") if isinstance(value, dt.datetime) else value.isoformat()
    if isinstance(value, bytes):
        return "0x" + value.hex()
    if not isinstance(value, str):
        if isinstance(value, numbers.Number):
            return str(value)
        value = str(value)
    if not value:
        return "''"
    return "CONVERT(0x{} USING utf8mb4)".format(value.encode("utf-8").hex())


def chunks(values: list[dict[str, Any]], size: int = 100):
    for index in range(0, len(values), size):
        yield values[index : index + size]


def emit_temporary_table(lines: list[str], table: TemporaryTable) -> None:
    lines.extend(
        [
            f"DROP TEMPORARY TABLE IF EXISTS `{table.name}`;",
            f"CREATE TEMPORARY TABLE `{table.name}` (",
            ",\n".join(
                (
                    f"    PRIMARY KEY {definition}"
                    if name == "PRIMARY KEY"
                    else f"    `{name}` {definition}"
                )
                for name, definition in table.columns
            ),
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
            "",
        ]
    )
    if not table.rows:
        return
    names = table.column_names
    name_sql = ", ".join(f"`{name}`" for name in names)
    for row_group in chunks(table.rows):
        values = []
        for row in row_group:
            values.append(
                "(" + ", ".join(as_mysql_literal(row.get(name)) for name in names) + ")"
            )
        lines.extend(
            [
                f"INSERT INTO `{table.name}` ({name_sql}) VALUES",
                ",\n".join(values) + ";",
                "",
            ]
        )


def clean(row: dict[str, Any], names: tuple[str, ...]) -> dict[str, Any]:
    return {name: row.get(name) for name in names}


def catalogue_tables(connection: Connection) -> list[TemporaryTable]:
    module_fields = (
        "module_code",
        "name",
        "name_en",
        "description",
        "icon",
        "color",
        "route_key",
        "sort_order",
        "is_published",
        "created_at",
        "updated_at",
    )
    modules = [
        clean(row, module_fields)
        for row in select_rows(
            connection,
            select(m.learning_module).order_by(m.learning_module.c.module_code),
        )
    ]

    template_fields = (
        "template_code",
        "template_version",
        "name",
        "description",
        "content_kind",
        "supported_clients_json",
        "config_json",
        "status",
        "sort_order",
        "created_at",
        "updated_at",
    )
    templates = [
        clean(row, template_fields)
        for row in select_rows(
            connection,
            select(m.learning_template).order_by(
                m.learning_template.c.template_code, m.learning_template.c.template_version
            ),
        )
    ]

    topic_fields = (
        "module_code",
        "topic_code",
        "title",
        "title_en",
        "description",
        "cover_url",
        "sort_order",
        "is_published",
        "created_at",
        "updated_at",
    )
    topics = [
        clean(row, topic_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_module.c.module_code,
                m.learning_topic.c.topic_code,
                m.learning_topic.c.title,
                m.learning_topic.c.title_en,
                m.learning_topic.c.description,
                m.learning_topic.c.cover_url,
                m.learning_topic.c.sort_order,
                m.learning_topic.c.is_published,
                m.learning_topic.c.created_at,
                m.learning_topic.c.updated_at,
            )
            .join(m.learning_module, m.learning_module.c.id == m.learning_topic.c.module_id)
            .order_by(m.learning_module.c.module_code, m.learning_topic.c.topic_code),
        )
    ]

    material_fields = (
        "template_code",
        "template_version",
        "material_code",
        "title",
        "title_en",
        "summary",
        "material_type",
        "publisher",
        "version_name",
        "cover_url",
        "difficulty_code",
        "estimated_minutes",
        "sort_order",
        "is_published",
        "created_at",
        "updated_at",
    )
    materials = [
        clean(row, material_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_template.c.template_code,
                m.learning_template.c.template_version,
                m.learning_material.c.material_code,
                m.learning_material.c.title,
                m.learning_material.c.title_en,
                m.learning_material.c.summary,
                m.learning_material.c.material_type,
                m.learning_material.c.publisher,
                m.learning_material.c.version_name,
                m.learning_material.c.cover_url,
                m.learning_material.c.difficulty_code,
                m.learning_material.c.estimated_minutes,
                m.learning_material.c.sort_order,
                m.learning_material.c.is_published,
                m.learning_material.c.created_at,
                m.learning_material.c.updated_at,
            )
            .outerjoin(
                m.learning_template,
                m.learning_template.c.id == m.learning_material.c.template_id,
            )
            .order_by(m.learning_material.c.material_code),
        )
    ]

    course_fields = (
        "primary_material_code",
        "course_code",
        "title",
        "title_en",
        "summary",
        "course_type",
        "content_resource",
        "content_reference_id",
        "content_json",
        "cover_url",
        "estimated_minutes",
        "difficulty_code",
        "sort_order",
        "is_published",
        "access_policy",
        "created_at",
        "updated_at",
    )
    courses = [
        clean(row, course_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_material.c.material_code.label("primary_material_code"),
                m.learning_course.c.course_code,
                m.learning_course.c.title,
                m.learning_course.c.title_en,
                m.learning_course.c.summary,
                m.learning_course.c.course_type,
                m.learning_course.c.content_resource,
                m.learning_course.c.content_reference_id,
                m.learning_course.c.content_json,
                m.learning_course.c.cover_url,
                m.learning_course.c.estimated_minutes,
                m.learning_course.c.difficulty_code,
                m.learning_course.c.sort_order,
                m.learning_course.c.is_published,
                m.learning_course.c.access_policy,
                m.learning_course.c.created_at,
                m.learning_course.c.updated_at,
            )
            .outerjoin(
                m.learning_material,
                m.learning_material.c.id == m.learning_course.c.material_id,
            )
            .order_by(m.learning_course.c.course_code),
        )
    ]

    course_material_fields = (
        "course_code",
        "material_code",
        "sort_order",
        "created_at",
        "updated_at",
    )
    course_materials = [
        clean(row, course_material_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_course.c.course_code,
                m.learning_material.c.material_code,
                m.learning_course_material.c.sort_order,
                m.learning_course_material.c.created_at,
                m.learning_course_material.c.updated_at,
            )
            .join(
                m.learning_course,
                m.learning_course.c.id == m.learning_course_material.c.course_id,
            )
            .join(
                m.learning_material,
                m.learning_material.c.id == m.learning_course_material.c.material_id,
            )
            .order_by(m.learning_course.c.course_code, m.learning_course_material.c.sort_order),
        )
    ]

    topic_course_fields = (
        "module_code",
        "topic_code",
        "course_code",
        "sort_order",
        "created_at",
        "updated_at",
    )
    topic_courses = [
        clean(row, topic_course_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_module.c.module_code,
                m.learning_topic.c.topic_code,
                m.learning_course.c.course_code,
                m.learning_topic_course.c.sort_order,
                m.learning_topic_course.c.created_at,
                m.learning_topic_course.c.updated_at,
            )
            .join(
                m.learning_topic,
                m.learning_topic.c.id == m.learning_topic_course.c.topic_id,
            )
            .join(m.learning_module, m.learning_module.c.id == m.learning_topic.c.module_id)
            .join(
                m.learning_course,
                m.learning_course.c.id == m.learning_topic_course.c.course_id,
            )
            .order_by(
                m.learning_module.c.module_code,
                m.learning_topic.c.topic_code,
                m.learning_topic_course.c.sort_order,
            ),
        )
    ]

    lesson_fields = (
        "material_code",
        "lesson_code",
        "title",
        "title_en",
        "summary",
        "illustration_url",
        "source_resource",
        "source_reference_id",
        "content_json",
        "lesson_format",
        "lesson_schema_version",
        "content_status",
        "published_at",
        "estimated_minutes",
        "sort_order",
        "is_published",
        "created_at",
        "updated_at",
    )
    lessons = [
        clean(row, lesson_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_material.c.material_code,
                m.learning_material_lesson.c.lesson_code,
                m.learning_material_lesson.c.title,
                m.learning_material_lesson.c.title_en,
                m.learning_material_lesson.c.summary,
                m.learning_material_lesson.c.illustration_url,
                m.learning_material_lesson.c.source_resource,
                m.learning_material_lesson.c.source_reference_id,
                m.learning_material_lesson.c.content_json,
                m.learning_material_lesson.c.lesson_format,
                m.learning_material_lesson.c.lesson_schema_version,
                m.learning_material_lesson.c.content_status,
                m.learning_material_lesson.c.published_at,
                m.learning_material_lesson.c.estimated_minutes,
                m.learning_material_lesson.c.sort_order,
                m.learning_material_lesson.c.is_published,
                m.learning_material_lesson.c.created_at,
                m.learning_material_lesson.c.updated_at,
            )
            .join(
                m.learning_material,
                m.learning_material.c.id == m.learning_material_lesson.c.material_id,
            )
            .order_by(m.learning_material.c.material_code, m.learning_material_lesson.c.sort_order),
        )
    ]

    section_fields = (
        "material_code",
        "lesson_code",
        "section_code",
        "title",
        "title_en",
        "sort_order",
        "status",
        "created_at",
        "updated_at",
    )
    sections = [
        clean(row, section_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_material.c.material_code,
                m.learning_material_lesson.c.lesson_code,
                m.learning_lesson_section.c.section_code,
                m.learning_lesson_section.c.title,
                m.learning_lesson_section.c.title_en,
                m.learning_lesson_section.c.sort_order,
                m.learning_lesson_section.c.status,
                m.learning_lesson_section.c.created_at,
                m.learning_lesson_section.c.updated_at,
            )
            .join(
                m.learning_material_lesson,
                m.learning_material_lesson.c.id == m.learning_lesson_section.c.lesson_id,
            )
            .join(
                m.learning_material,
                m.learning_material.c.id == m.learning_material_lesson.c.material_id,
            )
            .order_by(
                m.learning_material.c.material_code,
                m.learning_material_lesson.c.lesson_code,
                m.learning_lesson_section.c.sort_order,
            ),
        )
    ]

    item_fields = (
        "material_code",
        "lesson_code",
        "section_code",
        "item_code",
        "item_order",
        "title",
        "payload_json",
        "status",
        "created_at",
        "updated_at",
    )
    items = [
        clean(row, item_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_material.c.material_code,
                m.learning_material_lesson.c.lesson_code,
                m.learning_lesson_section.c.section_code,
                m.learning_lesson_item.c.item_code,
                m.learning_lesson_item.c.item_order,
                m.learning_lesson_item.c.title,
                m.learning_lesson_item.c.payload_json,
                m.learning_lesson_item.c.status,
                m.learning_lesson_item.c.created_at,
                m.learning_lesson_item.c.updated_at,
            )
            .join(
                m.learning_lesson_section,
                m.learning_lesson_section.c.id == m.learning_lesson_item.c.section_id,
            )
            .join(
                m.learning_material_lesson,
                m.learning_material_lesson.c.id == m.learning_lesson_section.c.lesson_id,
            )
            .join(
                m.learning_material,
                m.learning_material.c.id == m.learning_material_lesson.c.material_id,
            )
            .order_by(
                m.learning_material.c.material_code,
                m.learning_material_lesson.c.lesson_code,
                m.learning_lesson_section.c.section_code,
                m.learning_lesson_item.c.item_order,
            ),
        )
    ]

    block_fields = (
        "material_code",
        "lesson_code",
        "block_code",
        "block_type",
        "title",
        "payload_json",
        "sort_order",
        "status",
        "created_at",
        "updated_at",
    )
    blocks = [
        clean(row, block_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_material.c.material_code,
                m.learning_material_lesson.c.lesson_code,
                m.courseware_block.c.block_code,
                m.courseware_block.c.block_type,
                m.courseware_block.c.title,
                m.courseware_block.c.payload_json,
                m.courseware_block.c.sort_order,
                m.courseware_block.c.status,
                m.courseware_block.c.created_at,
                m.courseware_block.c.updated_at,
            )
            .join(
                m.learning_material_lesson,
                m.learning_material_lesson.c.id == m.courseware_block.c.material_lesson_id,
            )
            .join(
                m.learning_material,
                m.learning_material.c.id == m.learning_material_lesson.c.material_id,
            )
            .order_by(
                m.learning_material.c.material_code,
                m.learning_material_lesson.c.lesson_code,
                m.courseware_block.c.sort_order,
            ),
        )
    ]

    block_source_fields = (
        "material_code",
        "lesson_code",
        "block_code",
        "source_resource",
        "source_reference_id",
        "source_field",
        "source_locator_json",
        "source_snapshot_text",
        "source_hash",
        "sort_order",
        "created_at",
    )
    block_sources = [
        clean(row, block_source_fields)
        for row in select_rows(
            connection,
            select(
                m.learning_material.c.material_code,
                m.learning_material_lesson.c.lesson_code,
                m.courseware_block.c.block_code,
                m.courseware_block_source.c.source_resource,
                m.courseware_block_source.c.source_reference_id,
                m.courseware_block_source.c.source_field,
                m.courseware_block_source.c.source_locator_json,
                m.courseware_block_source.c.source_snapshot_text,
                m.courseware_block_source.c.source_hash,
                m.courseware_block_source.c.sort_order,
                m.courseware_block_source.c.created_at,
            )
            .join(
                m.courseware_block,
                m.courseware_block.c.id == m.courseware_block_source.c.courseware_block_id,
            )
            .join(
                m.learning_material_lesson,
                m.learning_material_lesson.c.id == m.courseware_block.c.material_lesson_id,
            )
            .join(
                m.learning_material,
                m.learning_material.c.id == m.learning_material_lesson.c.material_id,
            )
            .order_by(
                m.learning_material.c.material_code,
                m.learning_material_lesson.c.lesson_code,
                m.courseware_block.c.block_code,
                m.courseware_block_source.c.sort_order,
            ),
        )
    ]

    plan_fields = (
        "plan_code",
        "name",
        "name_en",
        "description",
        "tier_rank",
        "billing_cycle",
        "duration_days",
        "price",
        "currency",
        "icon",
        "badge_text",
        "sort_order",
        "status",
        "is_default",
        "created_at",
        "updated_at",
    )
    plans = [
        clean(row, plan_fields)
        for row in select_rows(
            connection,
            select(m.membership_plan).order_by(m.membership_plan.c.plan_code),
        )
    ]

    benefit_fields = (
        "benefit_code",
        "name",
        "name_en",
        "description",
        "benefit_type",
        "value_type",
        "unit",
        "scope_json",
        "default_value_json",
        "icon",
        "sort_order",
        "status",
        "created_at",
        "updated_at",
    )
    benefits = [
        clean(row, benefit_fields)
        for row in select_rows(
            connection,
            select(m.membership_benefit).order_by(m.membership_benefit.c.benefit_code),
        )
    ]

    plan_benefit_fields = (
        "plan_code",
        "benefit_code",
        "grant_value_json",
        "is_enabled",
        "sort_order",
        "created_at",
        "updated_at",
    )
    plan_benefits = [
        clean(row, plan_benefit_fields)
        for row in select_rows(
            connection,
            select(
                m.membership_plan.c.plan_code,
                m.membership_benefit.c.benefit_code,
                m.membership_plan_benefit.c.grant_value_json,
                m.membership_plan_benefit.c.is_enabled,
                m.membership_plan_benefit.c.sort_order,
                m.membership_plan_benefit.c.created_at,
                m.membership_plan_benefit.c.updated_at,
            )
            .join(
                m.membership_plan,
                m.membership_plan.c.id == m.membership_plan_benefit.c.membership_plan_id,
            )
            .join(
                m.membership_benefit,
                m.membership_benefit.c.id == m.membership_plan_benefit.c.benefit_id,
            )
            .order_by(m.membership_plan.c.plan_code, m.membership_benefit.c.benefit_code),
        )
    ]

    benefit_course_fields = (
        "benefit_code",
        "course_code",
        "access_action",
        "is_enabled",
        "sort_order",
        "created_at",
        "updated_at",
    )
    benefit_courses = [
        clean(row, benefit_course_fields)
        for row in select_rows(
            connection,
            select(
                m.membership_benefit.c.benefit_code,
                m.learning_course.c.course_code,
                m.membership_benefit_course.c.access_action,
                m.membership_benefit_course.c.is_enabled,
                m.membership_benefit_course.c.sort_order,
                m.membership_benefit_course.c.created_at,
                m.membership_benefit_course.c.updated_at,
            )
            .join(
                m.membership_benefit,
                m.membership_benefit.c.id == m.membership_benefit_course.c.benefit_id,
            )
            .join(
                m.learning_course,
                m.learning_course.c.id == m.membership_benefit_course.c.course_id,
            )
            .order_by(m.membership_benefit.c.benefit_code, m.learning_course.c.course_code),
        )
    ]

    return [
        TemporaryTable(
            "tmp_release_modules",
            (
                ("module_code", "VARCHAR(80) NOT NULL PRIMARY KEY"),
                ("name", "VARCHAR(100) NOT NULL"),
                ("name_en", "VARCHAR(100) NULL"),
                ("description", "VARCHAR(500) NULL"),
                ("icon", "VARCHAR(32) NULL"),
                ("color", "VARCHAR(32) NULL"),
                ("route_key", "VARCHAR(100) NULL"),
                ("sort_order", "INT NOT NULL"),
                ("is_published", "TINYINT(1) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
            ),
            modules,
        ),
        TemporaryTable(
            "tmp_release_templates",
            (
                ("template_code", "VARCHAR(80) NOT NULL"),
                ("template_version", "INT NOT NULL"),
                ("name", "VARCHAR(120) NOT NULL"),
                ("description", "LONGTEXT NULL"),
                ("content_kind", "VARCHAR(50) NOT NULL"),
                ("supported_clients_json", "LONGTEXT NOT NULL"),
                ("config_json", "LONGTEXT NULL"),
                ("status", "VARCHAR(20) NOT NULL"),
                ("sort_order", "INT NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`template_code`, `template_version`)"),
            ),
            templates,
        ),
        TemporaryTable(
            "tmp_release_topics",
            (
                ("module_code", "VARCHAR(80) NOT NULL"),
                ("topic_code", "VARCHAR(100) NOT NULL"),
                ("title", "VARCHAR(200) NOT NULL"),
                ("title_en", "VARCHAR(200) NULL"),
                ("description", "LONGTEXT NULL"),
                ("cover_url", "VARCHAR(500) NULL"),
                ("sort_order", "INT NOT NULL"),
                ("is_published", "TINYINT(1) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`module_code`, `topic_code`)"),
            ),
            topics,
        ),
        TemporaryTable(
            "tmp_release_materials",
            (
                ("template_code", "VARCHAR(80) NULL"),
                ("template_version", "INT NULL"),
                ("material_code", "VARCHAR(120) NOT NULL PRIMARY KEY"),
                ("title", "VARCHAR(255) NOT NULL"),
                ("title_en", "VARCHAR(255) NULL"),
                ("summary", "LONGTEXT NULL"),
                ("material_type", "VARCHAR(50) NOT NULL"),
                ("publisher", "VARCHAR(200) NULL"),
                ("version_name", "VARCHAR(100) NULL"),
                ("cover_url", "VARCHAR(500) NULL"),
                ("difficulty_code", "VARCHAR(50) NULL"),
                ("estimated_minutes", "INT NULL"),
                ("sort_order", "INT NOT NULL"),
                ("is_published", "TINYINT(1) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
            ),
            materials,
        ),
        TemporaryTable(
            "tmp_release_courses",
            (
                ("primary_material_code", "VARCHAR(120) NULL"),
                ("course_code", "VARCHAR(120) NOT NULL PRIMARY KEY"),
                ("title", "VARCHAR(255) NOT NULL"),
                ("title_en", "VARCHAR(255) NULL"),
                ("summary", "LONGTEXT NULL"),
                ("course_type", "VARCHAR(50) NOT NULL"),
                ("content_resource", "VARCHAR(80) NULL"),
                ("content_reference_id", "BIGINT UNSIGNED NULL"),
                ("content_json", "LONGTEXT NULL"),
                ("cover_url", "VARCHAR(500) NULL"),
                ("estimated_minutes", "INT NULL"),
                ("difficulty_code", "VARCHAR(50) NULL"),
                ("sort_order", "INT NOT NULL"),
                ("is_published", "TINYINT(1) NOT NULL"),
                ("access_policy", "VARCHAR(20) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
            ),
            courses,
        ),
        TemporaryTable(
            "tmp_release_course_materials",
            (
                ("course_code", "VARCHAR(120) NOT NULL"),
                ("material_code", "VARCHAR(120) NOT NULL"),
                ("sort_order", "INT NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`course_code`, `material_code`)"),
            ),
            course_materials,
        ),
        TemporaryTable(
            "tmp_release_topic_courses",
            (
                ("module_code", "VARCHAR(80) NOT NULL"),
                ("topic_code", "VARCHAR(100) NOT NULL"),
                ("course_code", "VARCHAR(120) NOT NULL"),
                ("sort_order", "INT NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`module_code`, `topic_code`, `course_code`)"),
            ),
            topic_courses,
        ),
        TemporaryTable(
            "tmp_release_lessons",
            (
                ("material_code", "VARCHAR(120) NOT NULL"),
                ("lesson_code", "VARCHAR(120) NOT NULL"),
                ("title", "VARCHAR(255) NOT NULL"),
                ("title_en", "VARCHAR(255) NULL"),
                ("summary", "LONGTEXT NULL"),
                ("illustration_url", "VARCHAR(500) NULL"),
                ("source_resource", "VARCHAR(80) NULL"),
                ("source_reference_id", "BIGINT UNSIGNED NULL"),
                ("content_json", "LONGTEXT NULL"),
                ("lesson_format", "VARCHAR(50) NOT NULL"),
                ("lesson_schema_version", "INT NOT NULL"),
                ("content_status", "VARCHAR(20) NOT NULL"),
                ("published_at", "DATETIME NULL"),
                ("estimated_minutes", "INT NULL"),
                ("sort_order", "INT NOT NULL"),
                ("is_published", "TINYINT(1) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`material_code`, `lesson_code`)"),
            ),
            lessons,
        ),
        TemporaryTable(
            "tmp_release_sections",
            (
                ("material_code", "VARCHAR(120) NOT NULL"),
                ("lesson_code", "VARCHAR(120) NOT NULL"),
                ("section_code", "VARCHAR(50) NOT NULL"),
                ("title", "VARCHAR(150) NOT NULL"),
                ("title_en", "VARCHAR(150) NOT NULL"),
                ("sort_order", "INT NOT NULL"),
                ("status", "VARCHAR(20) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`material_code`, `lesson_code`, `section_code`)"),
            ),
            sections,
        ),
        TemporaryTable(
            "tmp_release_items",
            (
                ("material_code", "VARCHAR(120) NOT NULL"),
                ("lesson_code", "VARCHAR(120) NOT NULL"),
                ("section_code", "VARCHAR(50) NOT NULL"),
                ("item_code", "VARCHAR(120) NOT NULL"),
                ("item_order", "INT NOT NULL"),
                ("title", "VARCHAR(255) NULL"),
                ("payload_json", "LONGTEXT NOT NULL"),
                ("status", "VARCHAR(20) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`material_code`, `lesson_code`, `section_code`, `item_code`)"),
            ),
            items,
        ),
        TemporaryTable(
            "tmp_release_blocks",
            (
                ("material_code", "VARCHAR(120) NOT NULL"),
                ("lesson_code", "VARCHAR(120) NOT NULL"),
                ("block_code", "VARCHAR(120) NOT NULL"),
                ("block_type", "VARCHAR(50) NOT NULL"),
                ("title", "VARCHAR(255) NULL"),
                ("payload_json", "LONGTEXT NOT NULL"),
                ("sort_order", "INT NOT NULL"),
                ("status", "VARCHAR(20) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`material_code`, `lesson_code`, `block_code`)"),
            ),
            blocks,
        ),
        TemporaryTable(
            "tmp_release_block_sources",
            (
                ("material_code", "VARCHAR(120) NOT NULL"),
                ("lesson_code", "VARCHAR(120) NOT NULL"),
                ("block_code", "VARCHAR(120) NOT NULL"),
                ("source_resource", "VARCHAR(80) NOT NULL"),
                ("source_reference_id", "BIGINT UNSIGNED NOT NULL"),
                ("source_field", "VARCHAR(80) NOT NULL"),
                ("source_locator_json", "LONGTEXT NULL"),
                ("source_snapshot_text", "MEDIUMTEXT NOT NULL"),
                ("source_hash", "CHAR(64) NULL"),
                ("sort_order", "INT NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
            ),
            block_sources,
        ),
        TemporaryTable(
            "tmp_release_membership_plans",
            (
                ("plan_code", "VARCHAR(64) NOT NULL PRIMARY KEY"),
                ("name", "VARCHAR(100) NOT NULL"),
                ("name_en", "VARCHAR(100) NULL"),
                ("description", "VARCHAR(500) NULL"),
                ("tier_rank", "INT NOT NULL"),
                ("billing_cycle", "VARCHAR(20) NOT NULL"),
                ("duration_days", "INT NULL"),
                ("price", "DECIMAL(10,2) NOT NULL"),
                ("currency", "CHAR(3) NOT NULL"),
                ("icon", "VARCHAR(32) NULL"),
                ("badge_text", "VARCHAR(50) NULL"),
                ("sort_order", "INT NOT NULL"),
                ("status", "VARCHAR(20) NOT NULL"),
                ("is_default", "TINYINT(1) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
            ),
            plans,
        ),
        TemporaryTable(
            "tmp_release_membership_benefits",
            (
                ("benefit_code", "VARCHAR(80) NOT NULL PRIMARY KEY"),
                ("name", "VARCHAR(100) NOT NULL"),
                ("name_en", "VARCHAR(100) NULL"),
                ("description", "VARCHAR(500) NULL"),
                ("benefit_type", "VARCHAR(30) NOT NULL"),
                ("value_type", "VARCHAR(20) NOT NULL"),
                ("unit", "VARCHAR(50) NULL"),
                ("scope_json", "LONGTEXT NULL"),
                ("default_value_json", "LONGTEXT NULL"),
                ("icon", "VARCHAR(32) NULL"),
                ("sort_order", "INT NOT NULL"),
                ("status", "VARCHAR(20) NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
            ),
            benefits,
        ),
        TemporaryTable(
            "tmp_release_plan_benefits",
            (
                ("plan_code", "VARCHAR(64) NOT NULL"),
                ("benefit_code", "VARCHAR(80) NOT NULL"),
                ("grant_value_json", "LONGTEXT NULL"),
                ("is_enabled", "TINYINT(1) NOT NULL"),
                ("sort_order", "INT NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`plan_code`, `benefit_code`)"),
            ),
            plan_benefits,
        ),
        TemporaryTable(
            "tmp_release_benefit_courses",
            (
                ("benefit_code", "VARCHAR(80) NOT NULL"),
                ("course_code", "VARCHAR(120) NOT NULL"),
                ("access_action", "VARCHAR(20) NOT NULL"),
                ("is_enabled", "TINYINT(1) NOT NULL"),
                ("sort_order", "INT NOT NULL"),
                ("created_at", "DATETIME NOT NULL"),
                ("updated_at", "DATETIME NOT NULL"),
                ("PRIMARY KEY", "(`benefit_code`, `course_code`, `access_action`)"),
            ),
            benefit_courses,
        ),
    ]


def emit_target_upserts(lines: list[str]) -> None:
    """Emit schema-aware upserts after every temp table has been populated."""

    lines.extend(
        [
            "-- The target's local user IDs are intentionally not copied.  Content rows are",
            "-- attributed to its first administrator when one exists; otherwise the nullable",
            "-- audit fields stay NULL.",
            "SET @release_actor_id := (",
            "    SELECT `id` FROM `user` WHERE `role` = 'admin' ORDER BY `id` LIMIT 1",
            ");",
            "",
            "START TRANSACTION;",
            "",
            "INSERT INTO `learning_module`",
            "(`module_code`,`name`,`name_en`,`description`,`icon`,`color`,`route_key`,`sort_order`,`is_published`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `module_code`,`name`,`name_en`,`description`,`icon`,`color`,`route_key`,`sort_order`,`is_published`,@release_actor_id,`created_at`,@release_actor_id,`updated_at`",
            "FROM `tmp_release_modules`",
            "ON DUPLICATE KEY UPDATE",
            "  `name`=VALUES(`name`), `name_en`=VALUES(`name_en`), `description`=VALUES(`description`),",
            "  `icon`=VALUES(`icon`), `color`=VALUES(`color`), `route_key`=VALUES(`route_key`),",
            "  `sort_order`=VALUES(`sort_order`), `is_published`=VALUES(`is_published`),",
            "  `updated_by`=@release_actor_id, `updated_at`=VALUES(`updated_at`);",
            "",
            "INSERT INTO `learning_template`",
            "(`template_code`,`template_version`,`name`,`description`,`content_kind`,`supported_clients_json`,`config_json`,`status`,`sort_order`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `template_code`,`template_version`,`name`,`description`,`content_kind`,`supported_clients_json`,`config_json`,`status`,`sort_order`,@release_actor_id,`created_at`,@release_actor_id,`updated_at`",
            "FROM `tmp_release_templates`",
            "ON DUPLICATE KEY UPDATE",
            "  `name`=VALUES(`name`), `description`=VALUES(`description`), `content_kind`=VALUES(`content_kind`),",
            "  `supported_clients_json`=VALUES(`supported_clients_json`), `config_json`=VALUES(`config_json`),",
            "  `status`=VALUES(`status`), `sort_order`=VALUES(`sort_order`),",
            "  `updated_by`=@release_actor_id, `updated_at`=VALUES(`updated_at`);",
            "",
            "INSERT INTO `learning_topic`",
            "(`module_id`,`topic_code`,`title`,`title_en`,`description`,`cover_url`,`sort_order`,`is_published`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `module`.`id`, `source`.`topic_code`, `source`.`title`, `source`.`title_en`, `source`.`description`, `source`.`cover_url`,",
            "       `source`.`sort_order`, `source`.`is_published`, @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_topics` AS `source`",
            "JOIN `learning_module` AS `module` ON `module`.`module_code` = `source`.`module_code`",
            "ON DUPLICATE KEY UPDATE",
            "  `title`=VALUES(`title`), `title_en`=VALUES(`title_en`), `description`=VALUES(`description`),",
            "  `cover_url`=VALUES(`cover_url`), `sort_order`=VALUES(`sort_order`), `is_published`=VALUES(`is_published`),",
            "  `updated_by`=@release_actor_id, `updated_at`=VALUES(`updated_at`);",
            "",
            "INSERT INTO `learning_material`",
            "(`template_id`,`material_code`,`title`,`title_en`,`summary`,`material_type`,`publisher`,`version_name`,`cover_url`,`difficulty_code`,`estimated_minutes`,`sort_order`,`is_published`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `template`.`id`, `source`.`material_code`, `source`.`title`, `source`.`title_en`, `source`.`summary`, `source`.`material_type`,",
            "       `source`.`publisher`, `source`.`version_name`, `source`.`cover_url`, `source`.`difficulty_code`, `source`.`estimated_minutes`,",
            "       `source`.`sort_order`, `source`.`is_published`, @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_materials` AS `source`",
            "LEFT JOIN `learning_template` AS `template`",
            "  ON `template`.`template_code` = `source`.`template_code`",
            " AND `template`.`template_version` = `source`.`template_version`",
            "ON DUPLICATE KEY UPDATE",
            "  `template_id`=VALUES(`template_id`), `title`=VALUES(`title`), `title_en`=VALUES(`title_en`),",
            "  `summary`=VALUES(`summary`), `material_type`=VALUES(`material_type`), `publisher`=VALUES(`publisher`),",
            "  `version_name`=VALUES(`version_name`), `cover_url`=VALUES(`cover_url`),",
            "  `difficulty_code`=VALUES(`difficulty_code`), `estimated_minutes`=VALUES(`estimated_minutes`),",
            "  `sort_order`=VALUES(`sort_order`), `is_published`=VALUES(`is_published`),",
            "  `updated_by`=@release_actor_id, `updated_at`=VALUES(`updated_at`);",
            "",
            "INSERT INTO `learning_course`",
            "(`material_id`,`course_code`,`title`,`title_en`,`summary`,`course_type`,`content_resource`,`content_reference_id`,`content_json`,`cover_url`,`estimated_minutes`,`difficulty_code`,`sort_order`,`is_published`,`access_policy`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `material`.`id`, `source`.`course_code`, `source`.`title`, `source`.`title_en`, `source`.`summary`, `source`.`course_type`,",
            "       `source`.`content_resource`, `source`.`content_reference_id`, `source`.`content_json`, `source`.`cover_url`,",
            "       `source`.`estimated_minutes`, `source`.`difficulty_code`, `source`.`sort_order`, `source`.`is_published`,",
            "       `source`.`access_policy`, @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_courses` AS `source`",
            "LEFT JOIN `learning_material` AS `material` ON `material`.`material_code` = `source`.`primary_material_code`",
            "ON DUPLICATE KEY UPDATE",
            "  `material_id`=VALUES(`material_id`), `title`=VALUES(`title`), `title_en`=VALUES(`title_en`),",
            "  `summary`=VALUES(`summary`), `course_type`=VALUES(`course_type`),",
            "  `content_resource`=VALUES(`content_resource`), `content_reference_id`=VALUES(`content_reference_id`),",
            "  `content_json`=VALUES(`content_json`), `cover_url`=VALUES(`cover_url`),",
            "  `estimated_minutes`=VALUES(`estimated_minutes`), `difficulty_code`=VALUES(`difficulty_code`),",
            "  `sort_order`=VALUES(`sort_order`), `is_published`=VALUES(`is_published`),",
            "  `access_policy`=VALUES(`access_policy`), `updated_by`=@release_actor_id, `updated_at`=VALUES(`updated_at`);",
            "",
            "-- The sync is authoritative for relationships within the exported catalogue.",
            "DELETE `mapping` FROM `learning_course_material` AS `mapping`",
            "JOIN `learning_course` AS `course` ON `course`.`id` = `mapping`.`course_id`",
            "JOIN `tmp_release_courses` AS `source` ON `source`.`course_code` = `course`.`course_code`;",
            "",
            "INSERT INTO `learning_course_material`",
            "(`course_id`,`material_id`,`sort_order`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `course`.`id`, `material`.`id`, `source`.`sort_order`, @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_course_materials` AS `source`",
            "JOIN `learning_course` AS `course` ON `course`.`course_code` = `source`.`course_code`",
            "JOIN `learning_material` AS `material` ON `material`.`material_code` = `source`.`material_code`;",
            "",
            "DELETE `mapping` FROM `learning_topic_course` AS `mapping`",
            "JOIN `learning_topic` AS `topic` ON `topic`.`id` = `mapping`.`topic_id`",
            "JOIN `learning_module` AS `module` ON `module`.`id` = `topic`.`module_id`",
            "JOIN `tmp_release_topics` AS `source`",
            "  ON `source`.`module_code` = `module`.`module_code` AND `source`.`topic_code` = `topic`.`topic_code`;",
            "",
            "INSERT INTO `learning_topic_course`",
            "(`topic_id`,`course_id`,`sort_order`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `topic`.`id`, `course`.`id`, `source`.`sort_order`, @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_topic_courses` AS `source`",
            "JOIN `learning_module` AS `module` ON `module`.`module_code` = `source`.`module_code`",
            "JOIN `learning_topic` AS `topic` ON `topic`.`module_id` = `module`.`id` AND `topic`.`topic_code` = `source`.`topic_code`",
            "JOIN `learning_course` AS `course` ON `course`.`course_code` = `source`.`course_code`;",
            "",
            "INSERT INTO `learning_material_lesson`",
            "(`material_id`,`lesson_code`,`title`,`title_en`,`summary`,`illustration_url`,`source_resource`,`source_reference_id`,`content_json`,`lesson_format`,`lesson_schema_version`,`content_status`,`published_at`,`estimated_minutes`,`sort_order`,`is_published`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `material`.`id`, `source`.`lesson_code`, `source`.`title`, `source`.`title_en`, `source`.`summary`, `source`.`illustration_url`,",
            "       `source`.`source_resource`, `source`.`source_reference_id`, `source`.`content_json`, `source`.`lesson_format`,",
            "       `source`.`lesson_schema_version`, `source`.`content_status`, `source`.`published_at`, `source`.`estimated_minutes`,",
            "       `source`.`sort_order`, `source`.`is_published`, @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_lessons` AS `source`",
            "JOIN `learning_material` AS `material` ON `material`.`material_code` = `source`.`material_code`",
            "ON DUPLICATE KEY UPDATE",
            "  `title`=VALUES(`title`), `title_en`=VALUES(`title_en`), `summary`=VALUES(`summary`),",
            "  `illustration_url`=VALUES(`illustration_url`), `source_resource`=VALUES(`source_resource`),",
            "  `source_reference_id`=VALUES(`source_reference_id`), `content_json`=VALUES(`content_json`),",
            "  `lesson_format`=VALUES(`lesson_format`), `lesson_schema_version`=VALUES(`lesson_schema_version`),",
            "  `content_status`=VALUES(`content_status`), `published_at`=VALUES(`published_at`),",
            "  `estimated_minutes`=VALUES(`estimated_minutes`), `sort_order`=VALUES(`sort_order`),",
            "  `is_published`=VALUES(`is_published`), `updated_by`=@release_actor_id, `updated_at`=VALUES(`updated_at`);",
            "",
            "-- Rebuild child content only for lessons carried by this release.  Foreign-key",
            "-- cascades remove old items and source snapshots before the current versions enter.",
            "DELETE `section` FROM `learning_lesson_section` AS `section`",
            "JOIN `learning_material_lesson` AS `lesson` ON `lesson`.`id` = `section`.`lesson_id`",
            "JOIN `learning_material` AS `material` ON `material`.`id` = `lesson`.`material_id`",
            "JOIN `tmp_release_lessons` AS `source`",
            "  ON `source`.`material_code` = `material`.`material_code` AND `source`.`lesson_code` = `lesson`.`lesson_code`;",
            "",
            "DELETE `block` FROM `courseware_block` AS `block`",
            "JOIN `learning_material_lesson` AS `lesson` ON `lesson`.`id` = `block`.`material_lesson_id`",
            "JOIN `learning_material` AS `material` ON `material`.`id` = `lesson`.`material_id`",
            "JOIN `tmp_release_lessons` AS `source`",
            "  ON `source`.`material_code` = `material`.`material_code` AND `source`.`lesson_code` = `lesson`.`lesson_code`;",
            "",
            "INSERT INTO `learning_lesson_section`",
            "(`lesson_id`,`section_code`,`title`,`title_en`,`sort_order`,`status`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `lesson`.`id`, `source`.`section_code`, `source`.`title`, `source`.`title_en`, `source`.`sort_order`, `source`.`status`,",
            "       @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_sections` AS `source`",
            "JOIN `learning_material` AS `material` ON `material`.`material_code` = `source`.`material_code`",
            "JOIN `learning_material_lesson` AS `lesson` ON `lesson`.`material_id` = `material`.`id` AND `lesson`.`lesson_code` = `source`.`lesson_code`;",
            "",
            "INSERT INTO `learning_lesson_item`",
            "(`section_id`,`item_code`,`item_order`,`title`,`payload_json`,`status`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `section`.`id`, `source`.`item_code`, `source`.`item_order`, `source`.`title`, `source`.`payload_json`, `source`.`status`,",
            "       @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_items` AS `source`",
            "JOIN `learning_material` AS `material` ON `material`.`material_code` = `source`.`material_code`",
            "JOIN `learning_material_lesson` AS `lesson` ON `lesson`.`material_id` = `material`.`id` AND `lesson`.`lesson_code` = `source`.`lesson_code`",
            "JOIN `learning_lesson_section` AS `section` ON `section`.`lesson_id` = `lesson`.`id` AND `section`.`section_code` = `source`.`section_code`;",
            "",
            "INSERT INTO `courseware_block`",
            "(`material_lesson_id`,`block_code`,`block_type`,`title`,`payload_json`,`sort_order`,`status`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `lesson`.`id`, `source`.`block_code`, `source`.`block_type`, `source`.`title`, `source`.`payload_json`,",
            "       `source`.`sort_order`, `source`.`status`, @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_blocks` AS `source`",
            "JOIN `learning_material` AS `material` ON `material`.`material_code` = `source`.`material_code`",
            "JOIN `learning_material_lesson` AS `lesson` ON `lesson`.`material_id` = `material`.`id` AND `lesson`.`lesson_code` = `source`.`lesson_code`;",
            "",
            "INSERT INTO `courseware_block_source`",
            "(`courseware_block_id`,`source_resource`,`source_reference_id`,`source_field`,`source_locator_json`,`source_snapshot_text`,`source_hash`,`sort_order`,`created_at`)",
            "SELECT `block`.`id`, `source`.`source_resource`, `source`.`source_reference_id`, `source`.`source_field`,",
            "       `source`.`source_locator_json`, `source`.`source_snapshot_text`, `source`.`source_hash`, `source`.`sort_order`, `source`.`created_at`",
            "FROM `tmp_release_block_sources` AS `source`",
            "JOIN `learning_material` AS `material` ON `material`.`material_code` = `source`.`material_code`",
            "JOIN `learning_material_lesson` AS `lesson` ON `lesson`.`material_id` = `material`.`id` AND `lesson`.`lesson_code` = `source`.`lesson_code`",
            "JOIN `courseware_block` AS `block` ON `block`.`material_lesson_id` = `lesson`.`id` AND `block`.`block_code` = `source`.`block_code`;",
            "",
            "INSERT INTO `membership_plan`",
            "(`plan_code`,`name`,`name_en`,`description`,`tier_rank`,`billing_cycle`,`duration_days`,`price`,`currency`,`icon`,`badge_text`,`sort_order`,`status`,`is_default`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `plan_code`,`name`,`name_en`,`description`,`tier_rank`,`billing_cycle`,`duration_days`,`price`,`currency`,`icon`,`badge_text`,`sort_order`,`status`,`is_default`,@release_actor_id,`created_at`,@release_actor_id,`updated_at`",
            "FROM `tmp_release_membership_plans`",
            "ON DUPLICATE KEY UPDATE",
            "  `name`=VALUES(`name`), `name_en`=VALUES(`name_en`), `description`=VALUES(`description`),",
            "  `tier_rank`=VALUES(`tier_rank`), `billing_cycle`=VALUES(`billing_cycle`), `duration_days`=VALUES(`duration_days`),",
            "  `price`=VALUES(`price`), `currency`=VALUES(`currency`), `icon`=VALUES(`icon`), `badge_text`=VALUES(`badge_text`),",
            "  `sort_order`=VALUES(`sort_order`), `status`=VALUES(`status`), `is_default`=VALUES(`is_default`),",
            "  `updated_by`=@release_actor_id, `updated_at`=VALUES(`updated_at`);",
            "",
            "INSERT INTO `membership_benefit`",
            "(`benefit_code`,`name`,`name_en`,`description`,`benefit_type`,`value_type`,`unit`,`scope_json`,`default_value_json`,`icon`,`sort_order`,`status`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `benefit_code`,`name`,`name_en`,`description`,`benefit_type`,`value_type`,`unit`,`scope_json`,`default_value_json`,`icon`,`sort_order`,`status`,@release_actor_id,`created_at`,@release_actor_id,`updated_at`",
            "FROM `tmp_release_membership_benefits`",
            "ON DUPLICATE KEY UPDATE",
            "  `name`=VALUES(`name`), `name_en`=VALUES(`name_en`), `description`=VALUES(`description`),",
            "  `benefit_type`=VALUES(`benefit_type`), `value_type`=VALUES(`value_type`), `unit`=VALUES(`unit`),",
            "  `scope_json`=VALUES(`scope_json`), `default_value_json`=VALUES(`default_value_json`),",
            "  `icon`=VALUES(`icon`), `sort_order`=VALUES(`sort_order`), `status`=VALUES(`status`),",
            "  `updated_by`=@release_actor_id, `updated_at`=VALUES(`updated_at`);",
            "",
            "DELETE `mapping` FROM `membership_plan_benefit` AS `mapping`",
            "JOIN `membership_plan` AS `plan` ON `plan`.`id` = `mapping`.`membership_plan_id`",
            "JOIN `tmp_release_membership_plans` AS `source` ON `source`.`plan_code` = `plan`.`plan_code`;",
            "",
            "INSERT INTO `membership_plan_benefit`",
            "(`membership_plan_id`,`benefit_id`,`grant_value_json`,`is_enabled`,`sort_order`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `plan`.`id`, `benefit`.`id`, `source`.`grant_value_json`, `source`.`is_enabled`, `source`.`sort_order`,",
            "       @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_plan_benefits` AS `source`",
            "JOIN `membership_plan` AS `plan` ON `plan`.`plan_code` = `source`.`plan_code`",
            "JOIN `membership_benefit` AS `benefit` ON `benefit`.`benefit_code` = `source`.`benefit_code`;",
            "",
            "DELETE `mapping` FROM `membership_benefit_course` AS `mapping`",
            "JOIN `membership_benefit` AS `benefit` ON `benefit`.`id` = `mapping`.`benefit_id`",
            "JOIN `tmp_release_membership_benefits` AS `source` ON `source`.`benefit_code` = `benefit`.`benefit_code`;",
            "",
            "INSERT INTO `membership_benefit_course`",
            "(`benefit_id`,`course_id`,`access_action`,`is_enabled`,`sort_order`,`created_by`,`created_at`,`updated_by`,`updated_at`)",
            "SELECT `benefit`.`id`, `course`.`id`, `source`.`access_action`, `source`.`is_enabled`, `source`.`sort_order`,",
            "       @release_actor_id, `source`.`created_at`, @release_actor_id, `source`.`updated_at`",
            "FROM `tmp_release_benefit_courses` AS `source`",
            "JOIN `membership_benefit` AS `benefit` ON `benefit`.`benefit_code` = `source`.`benefit_code`",
            "JOIN `learning_course` AS `course` ON `course`.`course_code` = `source`.`course_code`;",
            "",
            "COMMIT;",
            "",
            "-- The temporary tables disappear at the end of the mysql/DMS session.",
        ]
    )


def table_counts(tables: list[TemporaryTable]) -> dict[str, int]:
    return {table.name.removeprefix("tmp_release_"): len(table.rows) for table in tables}


def generate(output: Path, manifest_path: Path) -> dict[str, int]:
    settings = Settings()
    engine = make_engine(settings.database_url)
    if engine.dialect.name != "mysql":
        raise RuntimeError("The Aliyun export must be generated from a MySQL database.")
    with engine.connect() as connection:
        tables = catalogue_tables(connection)

    counts = table_counts(tables)
    if not counts["modules"] or not counts["materials"] or not counts["lessons"]:
        raise RuntimeError("The source database does not contain a complete learning catalogue.")
    if counts["items"] < counts["sections"]:
        raise RuntimeError("Generic lesson item count is unexpectedly lower than section count.")

    lines = [
        "-- Happy English learning catalogue content sync for Aliyun MySQL.",
        "-- Generated from the current local MySQL catalogue; numeric IDs are never reused.",
        "-- Prerequisite: run sql/deploy/20261005_aliyun_schema_release.sh first.",
        "-- This script intentionally excludes user accounts, login audit, learning progress,",
        "-- study sessions, and user membership records.",
        "SET NAMES utf8mb4;",
        "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;",
        "",
    ]
    for table in tables:
        emit_temporary_table(lines, table)
    emit_target_upserts(lines)
    payload = "\n".join(lines) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload, encoding="utf-8")

    manifest = {
        "generated_from": "local MySQL learning catalogue",
        "output": str(output.relative_to(ROOT)),
        "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "counts": counts,
        "excluded": [
            "user",
            "login_audit",
            "learning_progress",
            "learning_progress_item",
            "learning_study_session",
            "user_membership",
            "learning_user_course",
        ],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    counts = generate(args.output.resolve(), args.manifest.resolve())
    print(json.dumps({"output": str(args.output), "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
