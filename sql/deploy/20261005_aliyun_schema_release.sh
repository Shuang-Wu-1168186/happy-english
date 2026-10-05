#!/usr/bin/env bash
# Apply the Happy English database release to an existing Aliyun MySQL/RDS DB.
#
# Required environment variables:
#   MYSQL_HOST, MYSQL_USER, MYSQL_DATABASE, MYSQL_PWD
# Optional:
#   MYSQL_PORT=3306, MYSQL_BIN=mysql, MYSQL_SSL_CA=/path/to/ca.pem
#
# Default mode upgrades schema and imports the current learning catalogue.  It
# keeps the two legacy source tables for rollback.  Run this script again with
# --finalize only after the deployed API and learner pages are verified.

set -euo pipefail
export LC_ALL=C

release_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
mysql_bin="${MYSQL_BIN:-mysql}"
mysql_host="${MYSQL_HOST:?Set MYSQL_HOST}"
mysql_user="${MYSQL_USER:?Set MYSQL_USER}"
mysql_database="${MYSQL_DATABASE:?Set MYSQL_DATABASE}"
: "${MYSQL_PWD:?Set MYSQL_PWD}"
mysql_port="${MYSQL_PORT:-3306}"
finalize=false
force_content=false

for argument in "$@"; do
  case "$argument" in
    --finalize) finalize=true ;;
    --force-content) force_content=true ;;
    *)
      echo "Unknown option: $argument" >&2
      exit 2
      ;;
  esac
done

mysql_args=(
  --protocol=TCP
  --host="$mysql_host"
  --port="$mysql_port"
  --user="$mysql_user"
  --default-character-set=utf8mb4
)
if [[ -n "${MYSQL_SSL_CA:-}" ]]; then
  mysql_args+=(--ssl-ca="$MYSQL_SSL_CA")
fi

mysql_exec() {
  "$mysql_bin" "${mysql_args[@]}" "$mysql_database" "$@"
}

mysql_query() {
  mysql_exec --skip-column-names --batch --raw -e "$1"
}

has_table() {
  [[ "$(mysql_query "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = '$1'")" == "1" ]]
}

has_column() {
  [[ "$(mysql_query "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = '$1' AND column_name = '$2'")" == "1" ]]
}

has_index() {
  [[ "$(mysql_query "SELECT COUNT(*) FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = '$1' AND index_name = '$2'")" == "1" ]]
}

has_all_tables() {
  local table_name
  for table_name in "$@"; do
    has_table "$table_name" || return 1
  done
}

has_all_columns() {
  if (( $# % 2 != 0 )); then
    echo "has_all_columns expects table/column pairs" >&2
    exit 2
  fi

  while (( $# > 0 )); do
    has_column "$1" "$2" || return 1
    shift 2
  done
}

migration_applied() {
  [[ "$(mysql_query "SELECT COUNT(*) FROM app_schema_migration WHERE migration_name = '$1'")" == "1" ]]
}

mark_applied() {
  local migration_name="$1"
  local file_path="$2"
  local checksum
  if command -v sha256sum >/dev/null 2>&1; then
    checksum="$(sha256sum "$file_path" | awk '{print $1}')"
  else
    checksum="$(shasum -a 256 "$file_path" | awk '{print $1}')"
  fi
  mysql_exec -e "INSERT INTO app_schema_migration (migration_name, checksum) VALUES ('$migration_name', '$checksum') ON DUPLICATE KEY UPDATE checksum=VALUES(checksum), applied_at=CURRENT_TIMESTAMP"
}

run_once() {
  local migration_name="$1"
  local relative_file="$2"
  local file_path="$release_root/$relative_file"
  if migration_applied "$migration_name"; then
    echo "[skip] $migration_name"
    return
  fi
  echo "[run ] $migration_name"
  mysql_exec < "$file_path"
  mark_applied "$migration_name" "$file_path"
}

mark_existing() {
  local migration_name="$1"
  local marker_file="$release_root/sql/deploy/20261005_aliyun_preflight.sql"
  if migration_applied "$migration_name"; then
    echo "[skip] $migration_name"
    return
  fi
  echo "[mark] $migration_name (already present on target)"
  mark_applied "$migration_name" "$marker_file"
}

# Read-only state report first; it is intentionally not used as an automatic
# gate because this runner supports both legacy and partially upgraded RDS DBs.
mysql_exec < "$release_root/sql/deploy/20261005_aliyun_preflight.sql"

mysql_exec <<'SQL'
CREATE TABLE IF NOT EXISTS `app_schema_migration` (
  `migration_name` VARCHAR(160) NOT NULL,
  `checksum` CHAR(64) NOT NULL,
  `applied_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`migration_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Happy English release migration ledger';
SQL

if has_table "login_audit" && has_column "login_audit" "logged_in_at"; then
  mark_existing "20260920-login-audit"
else
  run_once "20260920-login-audit" "sql/20260920_add_login_audit.sql"
fi

if has_column "user" "contact_number" && has_index "user" "uk_user_contact_number"; then
  mark_existing "20260925-miniprogram-phone-login"
else
  run_once "20260925-miniprogram-phone-login" "sql/20260925_add_miniprogram_phone_login.sql"
fi

if has_all_tables "learning_module" "learning_topic" "learning_course"; then
  mark_existing "20260925-learning-catalog"
else
  run_once "20260925-learning-catalog" "sql/20260925_add_learning_catalog.sql"
fi

if has_all_tables "learning_progress" "learning_progress_item" "learning_study_session"; then
  mark_existing "20260925-learning-progress"
else
  run_once "20260925-learning-progress" "sql/20260925_redesign_learning_progress.sql"
fi

if has_all_tables \
    "learning_material" "learning_material_lesson" "learning_course_material" \
    "membership_plan" "membership_benefit" "membership_plan_benefit" \
    "membership_benefit_course" "user_membership" \
  && has_all_columns "learning_course" "material_id" "learning_course" "access_policy"; then
  mark_existing "20260926-membership-material-management"
else
  # This historical migration adds material_id immediately after topic_id.  A
  # target without both columns is a mixed, manually edited schema and must be
  # reviewed instead of risking an invalid ALTER TABLE statement.
  if ! has_column "learning_course" "topic_id" && ! has_column "learning_course" "material_id"; then
    echo "learning_course has neither topic_id nor material_id; target is partially migrated." >&2
    exit 1
  fi
  run_once "20260926-membership-material-management" "sql/20260926_add_membership_material_management.sql"
fi

if has_all_columns \
    "english_note_item" "language_register" \
    "english_note_item" "usage_scenarios_json" \
    "english_note_item" "register_reason" \
    "english_note_item" "classification_confidence" \
    "english_note_item" "classification_source"; then
  mark_existing "20260926-note-language-columns"
  # The label seed is deliberately not replayed on an already classified
  # database: it can update automatic labels on a user's existing notes.
  mark_existing "20260926-note-language-labels"
else
  run_once "20260926-note-language-columns" "sql/20260926_classify_english_note_items.sql"
  run_once "20260926-note-language-labels" "sql/20260926_seed_english_note_item_language_labels.sql"
fi

if has_all_tables "courseware_block" "courseware_block_source" \
  && has_column "learning_material_lesson" "lesson_format"; then
  mark_existing "20260926-courseware-blocks"
else
  run_once "20260926-courseware-blocks" "sql/20260926_add_courseware_blocks.sql"
fi

# These four migrations are only the bridge from the original direct
# topic→course/material design.  Current databases no longer have either
# topic_id column, and replaying the bridge there would fail or create stale
# legacy content.  A database with exactly one of the two columns needs human
# review before deployment.
if has_column "learning_course" "topic_id" && has_column "learning_material" "topic_id"; then
  run_once "20260926-import-existing-materials" "sql/20260926_import_existing_learning_materials.sql"
  run_once "20260926-restructure-learning-modules" "sql/20260926_restructure_learning_modules.sql"
  run_once "20260926-move-my-notes" "sql/20260926_move_my_notes_to_private_zone.sql"
  run_once "20260926-seed-put-aside-courseware" "sql/20260926_seed_put_aside_courseware.sql"
elif has_column "learning_course" "topic_id" || has_column "learning_material" "topic_id"; then
  echo "Only one legacy topic_id column remains; target is partially migrated." >&2
  exit 1
else
  mark_existing "20260926-import-existing-materials"
  mark_existing "20260926-restructure-learning-modules"
  mark_existing "20260926-move-my-notes"
  mark_existing "20260926-seed-put-aside-courseware"
fi

if has_table "learning_course_material"; then
  mark_existing "20260927-course-material-mapping"
else
  run_once "20260927-course-material-mapping" "sql/20260927_add_learning_course_material_mapping.sql"
fi

if has_column "learning_course" "topic_id"; then
  run_once "20260927-topic-course-mapping" "sql/20260927_add_learning_topic_course_mapping.sql"
elif has_table "learning_topic_course"; then
  mark_existing "20260927-topic-course-mapping"
else
  echo "learning_course.topic_id is absent but learning_topic_course is missing; target is partially migrated." >&2
  exit 1
fi

if has_all_tables "learning_lesson_section" "learning_lesson_item" \
  && has_all_columns \
    "learning_material_lesson" "lesson_schema_version" \
    "learning_material_lesson" "content_status" \
    "learning_material_lesson" "published_at"; then
  mark_existing "20260928-generic-lesson-content"
else
  run_once "20260928-generic-lesson-content" "sql/20260928_add_generic_lesson_content.sql"
fi

if has_column "learning_material" "topic_id"; then
  run_once "20260928-decouple-learning-material-topic" "sql/20260928_decouple_learning_material_topic.sql"
elif has_table "learning_course_material"; then
  mark_existing "20260928-decouple-learning-material-topic"
else
  echo "learning_material.topic_id is absent but learning_course_material is missing; target is partially migrated." >&2
  exit 1
fi

if has_table "learning_template" && has_column "learning_material" "template_id"; then
  mark_existing "20260928-learning-material-templates"
else
  run_once "20260928-learning-material-templates" "sql/20260928_add_learning_material_templates.sql"
fi

if has_column "learning_material_lesson" "illustration_url"; then
  mark_existing "20261004-lesson-illustration"
else
  run_once "20261004-lesson-illustration" "sql/20261004_add_learning_lesson_illustration.sql"
fi

run_once "20261005-cleanup-empty-duplicate-topics" "sql/deploy/20261005_cleanup_empty_duplicate_topics.sql"

if [[ "$force_content" == true ]]; then
  echo "[run ] 20261005-learning-catalogue-data (forced)"
  mysql_exec < "$release_root/sql/deploy/20261005_learning_catalog_data.sql"
  mark_applied "20261005-learning-catalogue-data" "$release_root/sql/deploy/20261005_learning_catalog_data.sql"
else
  run_once "20261005-learning-catalogue-data" "sql/deploy/20261005_learning_catalog_data.sql"
fi

if [[ "$finalize" == true ]]; then
  if has_table "daily_spoken_dialogue_item"; then
    run_once "20260928-drop-daily-spoken-dialogue-item" "sql/20260928_drop_daily_spoken_dialogue_item.sql"
  else
    mark_existing "20260928-drop-daily-spoken-dialogue-item"
  fi
  if has_table "learning_lesson_item_source"; then
    run_once "20260928-drop-learning-lesson-item-source" "sql/20260928_drop_learning_lesson_item_source.sql"
  else
    mark_existing "20260928-drop-learning-lesson-item-source"
  fi
else
  echo "[info] Legacy dialogue/source tables are retained. Re-run with --finalize after API validation."
fi

mysql_exec < "$release_root/sql/deploy/20261005_aliyun_postflight.sql"
echo "Database release completed."
