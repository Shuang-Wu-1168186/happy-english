#!/usr/bin/env python3
"""Generate and publish one textbook package to the Aliyun MySQL database.

The package is selected by stable business codes and is written to
``sql/deploy/generated`` by default.  The generated SQL is then applied over a
single MySQL session, recorded in ``app_schema_migration``, and verified with
the normal postflight checks.

Examples:
    PYTHONPATH=. .venv/bin/python scripts/publish_aliyun_textbook.py \
        --material-code commute-micro-english
    PYTHONPATH=. .venv/bin/python scripts/publish_aliyun_textbook.py \
        --course-code a-new-course --dry-run

Remote credentials are read from MYSQL_* environment variables.  MYSQL_PWD is
required for a real publish and is never written to the generated package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

from scripts.export_aliyun_learning_catalog import (
    ExportScope,
    default_output_path,
    generate,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REMOTE_HOST = "147.139.172.68"
DEFAULT_REMOTE_PORT = "3306"
DEFAULT_REMOTE_USER = "root"
DEFAULT_REMOTE_DATABASE = "happy_english"


def resolve_mysql_bin() -> str:
    configured = os.environ.get("MYSQL_BIN")
    if configured:
        return configured
    for candidate in ("/usr/local/mysql/bin/mysql", shutil.which("mysql")):
        if candidate and Path(candidate).exists():
            return candidate
    raise RuntimeError("mysql client not found; set MYSQL_BIN to the MySQL 8.x client path")


def remote_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment.setdefault("MYSQL_HOST", DEFAULT_REMOTE_HOST)
    environment.setdefault("MYSQL_PORT", DEFAULT_REMOTE_PORT)
    environment.setdefault("MYSQL_USER", DEFAULT_REMOTE_USER)
    environment.setdefault("MYSQL_DATABASE", DEFAULT_REMOTE_DATABASE)
    environment["MYSQL_BIN"] = resolve_mysql_bin()
    if not environment.get("MYSQL_PWD"):
        raise RuntimeError("MYSQL_PWD is required for a real Aliyun publish")
    return environment


def mysql_args(environment: dict[str, str]) -> list[str]:
    args = [
        environment["MYSQL_BIN"],
        "--protocol=TCP",
        "--host=" + environment["MYSQL_HOST"],
        "--port=" + environment["MYSQL_PORT"],
        "--user=" + environment["MYSQL_USER"],
        "--default-character-set=utf8mb4",
    ]
    if environment.get("MYSQL_SSL_CA"):
        args.append("--ssl-ca=" + environment["MYSQL_SSL_CA"])
    if environment.get("MYSQL_SSL_MODE"):
        args.append("--ssl-mode=" + environment["MYSQL_SSL_MODE"])
    if environment.get("MYSQL_COMPRESS", "").lower() in {"1", "true", "yes"}:
        args.append("--compress")
    args.append(environment["MYSQL_DATABASE"])
    return args


def run_mysql_file(path: Path, environment: dict[str, str]) -> None:
    with path.open("rb") as handle:
        subprocess.run(mysql_args(environment), stdin=handle, cwd=ROOT, env=environment, check=True)


def run_mysql_query(sql: str, environment: dict[str, str]) -> str:
    result = subprocess.run(
        mysql_args(environment)
        + ["--skip-column-names", "--batch", "--raw", "--execute=" + sql],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def content_migration_name(scope: ExportScope, checksum: str) -> str:
    return f"catalog:{scope.slug}:{checksum[:16]}"[:160]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--material-code", action="append", dest="material_codes", metavar="CODE")
    parser.add_argument("--course-code", action="append", dest="course_codes", metavar="CODE")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument(
        "--skip-schema",
        action="store_true",
        help="Skip the idempotent schema release; use only when the target schema is known current.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate and inspect the package without connecting to Aliyun.",
    )
    args = parser.parse_args()

    material_codes = frozenset(args.material_codes or ())
    course_codes = frozenset(args.course_codes or ())
    if not material_codes and not course_codes:
        parser.error("provide at least one --material-code or --course-code")

    scope = ExportScope(material_codes=material_codes, course_codes=course_codes)
    output = (args.output or default_output_path(scope)).resolve()
    manifest_path = (args.manifest or output.with_suffix(".manifest.json")).resolve()
    counts = generate(output, manifest_path, scope)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checksum = manifest["sha256"]
    expected_checksum = hashlib.sha256(output.read_bytes()).hexdigest()
    if checksum != expected_checksum:
        raise RuntimeError("Generated package checksum does not match its manifest")

    result = {
        "output": str(output),
        "manifest": str(manifest_path),
        "checksum": checksum,
        "scope": scope.as_manifest(),
        "counts": counts,
    }
    if args.dry_run:
        print(json.dumps({**result, "published": False}, ensure_ascii=False))
        return

    environment = remote_environment()
    if not args.skip_schema:
        schema_release = ROOT / "sql" / "deploy" / "20261005_aliyun_schema_release.sh"
        subprocess.run(
            [str(schema_release), "--skip-postflight"],
            cwd=ROOT,
            env=environment,
            check=True,
        )

    print(f"[publish] {output}")
    run_mysql_file(output, environment)

    migration_name = content_migration_name(scope, checksum)
    migration_name_sql = migration_name.replace("'", "''")
    checksum_sql = checksum.replace("'", "''")
    run_mysql_query(
        "INSERT INTO `app_schema_migration` (`migration_name`, `checksum`) "
        f"VALUES ('{migration_name_sql}', '{checksum_sql}') "
        "ON DUPLICATE KEY UPDATE `checksum`=VALUES(`checksum`), `applied_at`=CURRENT_TIMESTAMP",
        environment,
    )

    postflight = ROOT / "sql" / "deploy" / "20261005_aliyun_postflight.sql"
    run_mysql_file(postflight, environment)
    print(json.dumps({**result, "published": True, "migration_name": migration_name}, ensure_ascii=False))


if __name__ == "__main__":
    main()
