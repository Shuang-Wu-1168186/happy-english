-- A material belongs to courses, and courses are placed in topics.  This
-- migration preserves the old direct material topic as a topic-course mapping
-- before removing the material.topic_id column.
--
-- Run after the course-material and topic-course mapping migrations.

-- Keep the old one-material course field mirrored into the canonical mapping
-- table for installations that applied only part of the earlier migration.
INSERT INTO `learning_course_material`
    (`course_id`, `material_id`, `sort_order`, `created_by`, `updated_by`)
SELECT course.`id`, course.`material_id`, 10, course.`created_by`, course.`updated_by`
FROM `learning_course` course
WHERE course.`material_id` IS NOT NULL
ON DUPLICATE KEY UPDATE `course_id` = VALUES(`course_id`);

-- A material may now be reused by several courses.  Associate every course
-- that used to expose it with its former topic, without overwriting any
-- manually adjusted topic-course ordering already in place.
SET @has_material_topic = (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material'
      AND column_name = 'topic_id'
);
SET @backfill_topic_course = IF(
    @has_material_topic = 1,
    'INSERT INTO `learning_topic_course`\n        (`topic_id`, `course_id`, `sort_order`, `created_by`, `updated_by`)\n     SELECT material.`topic_id`, mapping.`course_id`, MIN(material.`sort_order`),\n            MIN(material.`created_by`), MIN(material.`updated_by`)\n     FROM `learning_material` material\n     JOIN `learning_course_material` mapping\n       ON mapping.`material_id` = material.`id`\n     WHERE material.`topic_id` IS NOT NULL\n     GROUP BY material.`topic_id`, mapping.`course_id`\n     ON DUPLICATE KEY UPDATE `course_id` = VALUES(`course_id`)',
    'SELECT 1'
);
PREPARE backfill_topic_course FROM @backfill_topic_course;
EXECUTE backfill_topic_course;
DEALLOCATE PREPARE backfill_topic_course;

-- `material_code` is now globally stable because topic is no longer part of
-- a material identity.  Existing installations must resolve duplicate codes
-- before this ALTER can succeed.
SET @has_material_topic_fk = (
    SELECT COUNT(*)
    FROM information_schema.table_constraints
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material'
      AND constraint_name = 'fk_learning_material_topic'
      AND constraint_type = 'FOREIGN KEY'
);
SET @drop_material_topic_fk = IF(
    @has_material_topic_fk = 1,
    'ALTER TABLE `learning_material` DROP FOREIGN KEY `fk_learning_material_topic`',
    'SELECT 1'
);
PREPARE drop_material_topic_fk FROM @drop_material_topic_fk;
EXECUTE drop_material_topic_fk;
DEALLOCATE PREPARE drop_material_topic_fk;

SET @has_material_topic_code_key = (
    SELECT COUNT(*)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material'
      AND index_name = 'uk_learning_material_topic_code'
);
SET @drop_material_topic_code_key = IF(
    @has_material_topic_code_key = 1,
    'ALTER TABLE `learning_material` DROP INDEX `uk_learning_material_topic_code`',
    'SELECT 1'
);
PREPARE drop_material_topic_code_key FROM @drop_material_topic_code_key;
EXECUTE drop_material_topic_code_key;
DEALLOCATE PREPARE drop_material_topic_code_key;

SET @has_material_topic_order_key = (
    SELECT COUNT(*)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material'
      AND index_name = 'idx_learning_material_topic_published_order'
);
SET @drop_material_topic_order_key = IF(
    @has_material_topic_order_key = 1,
    'ALTER TABLE `learning_material` DROP INDEX `idx_learning_material_topic_published_order`',
    'SELECT 1'
);
PREPARE drop_material_topic_order_key FROM @drop_material_topic_order_key;
EXECUTE drop_material_topic_order_key;
DEALLOCATE PREPARE drop_material_topic_order_key;

SET @drop_material_topic_column = IF(
    @has_material_topic = 1,
    'ALTER TABLE `learning_material` DROP COLUMN `topic_id`',
    'SELECT 1'
);
PREPARE drop_material_topic_column FROM @drop_material_topic_column;
EXECUTE drop_material_topic_column;
DEALLOCATE PREPARE drop_material_topic_column;

SET @has_material_code_key = (
    SELECT COUNT(*)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material'
      AND index_name = 'uk_learning_material_code'
);
SET @add_material_code_key = IF(
    @has_material_code_key = 0,
    'ALTER TABLE `learning_material` ADD UNIQUE KEY `uk_learning_material_code` (`material_code`)',
    'SELECT 1'
);
PREPARE add_material_code_key FROM @add_material_code_key;
EXECUTE add_material_code_key;
DEALLOCATE PREPARE add_material_code_key;

SET @has_material_published_order_key = (
    SELECT COUNT(*)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material'
      AND index_name = 'idx_learning_material_published_order'
);
SET @add_material_published_order_key = IF(
    @has_material_published_order_key = 0,
    'ALTER TABLE `learning_material` ADD KEY `idx_learning_material_published_order` (`is_published`, `sort_order`)',
    'SELECT 1'
);
PREPARE add_material_published_order_key FROM @add_material_published_order_key;
EXECUTE add_material_published_order_key;
DEALLOCATE PREPARE add_material_published_order_key;
