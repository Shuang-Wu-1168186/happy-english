-- Happy English Aliyun release preflight (read-only).
-- Run this in the target RDS database before the schema release script.
-- It deliberately uses information_schema only, so it is safe against both
-- the legacy database and an already-upgraded database.

SET NAMES utf8mb4;

SELECT
    DATABASE() AS `database_name`,
    VERSION() AS `mysql_version`,
    @@character_set_database AS `database_charset`,
    @@collation_database AS `database_collation`,
    CURRENT_USER() AS `connected_as`;

SELECT
    required.`object_name`,
    required.`object_kind`,
    CASE WHEN existing.`object_name` IS NULL THEN 'missing' ELSE 'present' END AS `state`
FROM (
    SELECT 'learning_module' AS `object_name`, 'table' AS `object_kind`
    UNION ALL SELECT 'learning_topic', 'table'
    UNION ALL SELECT 'learning_template', 'table'
    UNION ALL SELECT 'learning_material', 'table'
    UNION ALL SELECT 'learning_material_lesson', 'table'
    UNION ALL SELECT 'learning_lesson_section', 'table'
    UNION ALL SELECT 'learning_lesson_item', 'table'
    UNION ALL SELECT 'learning_course', 'table'
    UNION ALL SELECT 'learning_course_material', 'table'
    UNION ALL SELECT 'learning_topic_course', 'table'
    UNION ALL SELECT 'courseware_block', 'table'
    UNION ALL SELECT 'courseware_block_source', 'table'
    UNION ALL SELECT 'membership_plan', 'table'
    UNION ALL SELECT 'membership_benefit', 'table'
    UNION ALL SELECT 'login_audit', 'table'
    UNION ALL SELECT 'app_schema_migration', 'release ledger'
) AS required
LEFT JOIN (
    SELECT `table_name` AS `object_name`, 'table' AS `object_kind`
    FROM information_schema.tables
    WHERE table_schema = DATABASE()
    UNION ALL
    SELECT `table_name` AS `object_name`, 'release ledger' AS `object_kind`
    FROM information_schema.tables
    WHERE table_schema = DATABASE() AND table_name = 'app_schema_migration'
) AS existing
    ON existing.`object_name` = required.`object_name`
   AND existing.`object_kind` = required.`object_kind`
ORDER BY required.`object_kind`, required.`object_name`;

SELECT
    required.`table_name`,
    required.`column_name`,
    CASE WHEN existing.`column_name` IS NULL THEN 'missing' ELSE 'present' END AS `state`
FROM (
    SELECT 'learning_material' AS `table_name`, 'template_id' AS `column_name`
    UNION ALL SELECT 'learning_material_lesson', 'lesson_format'
    UNION ALL SELECT 'learning_material_lesson', 'lesson_schema_version'
    UNION ALL SELECT 'learning_material_lesson', 'content_status'
    UNION ALL SELECT 'learning_material_lesson', 'published_at'
    UNION ALL SELECT 'learning_material_lesson', 'illustration_url'
    UNION ALL SELECT 'learning_course', 'access_policy'
    UNION ALL SELECT 'user', 'contact_number'
    UNION ALL SELECT 'english_note_item', 'language_register'
    UNION ALL SELECT 'english_note_item', 'usage_scenarios_json'
    UNION ALL SELECT 'english_note_item', 'classification_source'
) AS required
LEFT JOIN information_schema.columns AS existing
  ON existing.table_schema = DATABASE()
 AND existing.table_name = required.table_name
 AND existing.column_name = required.column_name
ORDER BY required.table_name, required.column_name;

-- These legacy columns/tables determine which conditional migration stages are
-- still needed.  Do not manually drop them before the release script runs.
SELECT
    'legacy_learning_course_topic_id' AS `check_name`,
    CASE WHEN EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = DATABASE() AND table_name = 'learning_course' AND column_name = 'topic_id'
    ) THEN 'present: topic-course mapping still required' ELSE 'absent: topic-course mapping already applied' END AS `state`
UNION ALL
SELECT
    'legacy_learning_material_topic_id',
    CASE WHEN EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = DATABASE() AND table_name = 'learning_material' AND column_name = 'topic_id'
    ) THEN 'present: material-topic decoupling still required' ELSE 'absent: material-topic decoupling already applied' END
UNION ALL
SELECT
    'legacy_daily_spoken_dialogue_item',
    CASE WHEN EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_name = 'daily_spoken_dialogue_item'
    ) THEN 'present: retain until --finalize' ELSE 'absent: legacy dialogue source already retired' END
UNION ALL
SELECT
    'legacy_learning_lesson_item_source',
    CASE WHEN EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_name = 'learning_lesson_item_source'
    ) THEN 'present: retain until --finalize' ELSE 'absent: source snapshot table already retired' END;

SELECT
    table_name,
    table_rows AS approximate_rows,
    table_collation
FROM information_schema.tables
WHERE table_schema = DATABASE()
  AND table_name IN (
      'user', 'english_note', 'english_note_item', 'everyday_sentence',
      'learning_module', 'learning_topic', 'learning_template', 'learning_material',
      'learning_material_lesson', 'learning_lesson_section', 'learning_lesson_item',
      'learning_course', 'learning_course_material', 'learning_topic_course',
      'courseware_block', 'courseware_block_source',
      'membership_plan', 'membership_benefit', 'membership_benefit_course'
  )
ORDER BY table_name;

SELECT
    index_name,
    GROUP_CONCAT(column_name ORDER BY seq_in_index SEPARATOR ', ') AS indexed_columns,
    non_unique
FROM information_schema.statistics
WHERE table_schema = DATABASE()
  AND table_name = 'user'
  AND index_name = 'uk_user_contact_number'
GROUP BY index_name, non_unique;

-- If app_schema_migration is present, inspect it separately after this
-- preflight.  Referencing it here would make a legacy database fail before
-- the release runner has had a chance to create the ledger.
