-- Happy English Aliyun release verification.
-- Run after the schema release or a scoped textbook content package.  It does
-- not modify data.

SET NAMES utf8mb4;

SELECT
    required.`table_name`,
    CASE WHEN existing.`table_name` IS NULL THEN 'MISSING' ELSE 'OK' END AS `state`
FROM (
    SELECT 'login_audit' AS `table_name`
    UNION ALL SELECT 'learning_module'
    UNION ALL SELECT 'learning_topic'
    UNION ALL SELECT 'learning_template'
    UNION ALL SELECT 'learning_material'
    UNION ALL SELECT 'learning_material_lesson'
    UNION ALL SELECT 'learning_lesson_section'
    UNION ALL SELECT 'learning_lesson_item'
    UNION ALL SELECT 'learning_course'
    UNION ALL SELECT 'learning_course_material'
    UNION ALL SELECT 'learning_topic_course'
    UNION ALL SELECT 'courseware_block'
    UNION ALL SELECT 'courseware_block_source'
    UNION ALL SELECT 'membership_plan'
    UNION ALL SELECT 'membership_benefit'
    UNION ALL SELECT 'english_note_item_frequency'
) AS required
LEFT JOIN information_schema.tables AS existing
  ON existing.table_schema = DATABASE() AND existing.table_name = required.table_name
ORDER BY required.table_name;

SELECT
    required.`table_name`,
    required.`column_name`,
    CASE WHEN existing.`column_name` IS NULL THEN 'MISSING' ELSE 'OK' END AS `state`
FROM (
    SELECT 'learning_material' AS `table_name`, 'template_id' AS `column_name`
    UNION ALL SELECT 'learning_material_lesson', 'lesson_format'
    UNION ALL SELECT 'learning_material_lesson', 'lesson_schema_version'
    UNION ALL SELECT 'learning_material_lesson', 'content_status'
    UNION ALL SELECT 'learning_material_lesson', 'published_at'
    UNION ALL SELECT 'learning_material_lesson', 'illustration_url'
    UNION ALL SELECT 'learning_course', 'access_policy'
    UNION ALL SELECT 'user', 'contact_number'
    UNION ALL SELECT 'english_note_item_frequency', 'user_id'
    UNION ALL SELECT 'english_note_item_frequency', 'note_item_id'
    UNION ALL SELECT 'english_note_item_frequency', 'frequency_count'
    UNION ALL SELECT 'english_note_item_frequency', 'last_recorded_at'
) AS required
LEFT JOIN information_schema.columns AS existing
  ON existing.table_schema = DATABASE()
 AND existing.table_name = required.table_name
 AND existing.column_name = required.column_name
ORDER BY required.table_name, required.column_name;

SELECT 'modules' AS `record_type`, COUNT(*) AS `count` FROM `learning_module`
UNION ALL SELECT 'templates', COUNT(*) FROM `learning_template`
UNION ALL SELECT 'topics', COUNT(*) FROM `learning_topic`
UNION ALL SELECT 'materials', COUNT(*) FROM `learning_material`
UNION ALL SELECT 'courses', COUNT(*) FROM `learning_course`
UNION ALL SELECT 'course_materials', COUNT(*) FROM `learning_course_material`
UNION ALL SELECT 'topic_courses', COUNT(*) FROM `learning_topic_course`
UNION ALL SELECT 'lessons', COUNT(*) FROM `learning_material_lesson`
UNION ALL SELECT 'sections', COUNT(*) FROM `learning_lesson_section`
UNION ALL SELECT 'items', COUNT(*) FROM `learning_lesson_item`
UNION ALL SELECT 'courseware_blocks', COUNT(*) FROM `courseware_block`
UNION ALL SELECT 'courseware_block_sources', COUNT(*) FROM `courseware_block_source`
UNION ALL SELECT 'membership_plans', COUNT(*) FROM `membership_plan`
UNION ALL SELECT 'membership_benefits', COUNT(*) FROM `membership_benefit`
UNION ALL SELECT 'note_item_frequency_records', COUNT(*) FROM `english_note_item_frequency`;

SELECT
    module.`module_code`,
    topic.`topic_code`,
    topic.`title`,
    COUNT(DISTINCT mapping.`course_id`) AS `course_count`,
    COUNT(DISTINCT material_mapping.`material_id`) AS `material_count`,
    COUNT(DISTINCT lesson.`id`) AS `lesson_count`
FROM `learning_topic` AS topic
JOIN `learning_module` AS module ON module.`id` = topic.`module_id`
LEFT JOIN `learning_topic_course` AS mapping ON mapping.`topic_id` = topic.`id`
LEFT JOIN `learning_course_material` AS material_mapping ON material_mapping.`course_id` = mapping.`course_id`
LEFT JOIN `learning_material_lesson` AS lesson ON lesson.`material_id` = material_mapping.`material_id`
WHERE (module.`module_code`, topic.`topic_code`) IN (
    ('intermediate-english', 'travel-english'),
    ('intermediate-english', 'shopping-english'),
    ('higher-english', 'software-developer-workplace-english'),
    ('elementary-english', 'commute-micro-english')
)
GROUP BY module.`module_code`, topic.`id`, topic.`topic_code`, topic.`title`
ORDER BY module.`module_code`, topic.`topic_code`;

SELECT COUNT(*) AS `duplicate_topic_code_groups`
FROM (
    SELECT topic_code
    FROM `learning_topic`
    GROUP BY topic_code
    HAVING COUNT(*) > 1
) AS duplicates;

SELECT
    COUNT(*) AS `structured_lessons_missing_sections`
FROM (
    SELECT lesson.`id`
    FROM `learning_material_lesson` AS lesson
    LEFT JOIN `learning_lesson_section` AS section_row ON section_row.`lesson_id` = lesson.`id`
    WHERE lesson.`lesson_format` = 'structured'
    GROUP BY lesson.`id`
    HAVING COUNT(section_row.`id`) = 0
) AS missing;

SELECT
    COUNT(*) AS `commute_lessons_missing_illustration_url`
FROM `learning_material_lesson` AS lesson
JOIN `learning_material` AS material ON material.`id` = lesson.`material_id`
WHERE material.`material_code` LIKE 'commute-%'
  AND (lesson.`illustration_url` IS NULL OR lesson.`illustration_url` = '');

SELECT
    COUNT(*) AS `legacy_dialogue_references`
FROM `learning_material_lesson`
WHERE `source_resource` = 'dialogues';

SELECT
    table_name AS `legacy_table`,
    CASE WHEN table_name IS NULL THEN 'removed' ELSE 'still present (expected before --finalize)' END AS `state`
FROM information_schema.tables
WHERE table_schema = DATABASE()
  AND table_name IN ('daily_spoken_dialogue_item', 'learning_lesson_item_source');
