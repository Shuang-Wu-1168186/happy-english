-- Repair source references imported from a development database.  The
-- catalogue export used the local english_textbook_lesson IDs, while the
-- deployed database has the same published lessons under different IDs.
-- Match by the stable unit/lesson pair so this remains safe across databases.

START TRANSACTION;

CREATE TEMPORARY TABLE `tmp_primary_textbook_source_reference_repair` (
    `lesson_code` VARCHAR(120) NOT NULL PRIMARY KEY,
    `unit_name` VARCHAR(100) NOT NULL,
    `lesson_name` VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `tmp_primary_textbook_source_reference_repair`
    (`lesson_code`, `unit_name`, `lesson_name`)
VALUES
    ('textbook-lesson-11', 'Unit 1', 'Lesson 4'),
    ('textbook-lesson-16', 'Unit 2', 'Lesson 5'),
    ('textbook-lesson-17', 'Unit 2', 'Lesson 6'),
    ('textbook-lesson-27', 'Unit 2', 'Lesson 7'),
    ('textbook-lesson-28', 'Unit 2', 'Lesson 8');

UPDATE `learning_material_lesson` AS `lesson`
JOIN `learning_material` AS `material`
  ON `material`.`id` = `lesson`.`material_id`
JOIN `tmp_primary_textbook_source_reference_repair` AS `repair`
  ON `repair`.`lesson_code` = `lesson`.`lesson_code`
JOIN `english_textbook_lesson` AS `source`
  ON `source`.`unit_name` = `repair`.`unit_name`
 AND `source`.`lesson_name` = `repair`.`lesson_name`
SET
    `lesson`.`source_reference_id` = `source`.`id`,
    `lesson`.`updated_at` = CURRENT_TIMESTAMP
WHERE `material`.`material_code` = 'english-textbook-current'
  AND `lesson`.`source_resource` = 'textbook';

-- A zero-row result means every repaired lesson points to a published source
-- row.  This remains a useful report when the migration is replayed manually.
SELECT
    `lesson`.`lesson_code`,
    `lesson`.`source_reference_id`
FROM `learning_material_lesson` AS `lesson`
JOIN `learning_material` AS `material`
  ON `material`.`id` = `lesson`.`material_id`
JOIN `tmp_primary_textbook_source_reference_repair` AS `repair`
  ON `repair`.`lesson_code` = `lesson`.`lesson_code`
LEFT JOIN `english_textbook_lesson` AS `source`
  ON `source`.`id` = `lesson`.`source_reference_id`
 AND `source`.`is_published` = 1
WHERE `material`.`material_code` = 'english-textbook-current'
  AND `lesson`.`source_resource` = 'textbook'
  AND `source`.`id` IS NULL;

DROP TEMPORARY TABLE `tmp_primary_textbook_source_reference_repair`;

COMMIT;
