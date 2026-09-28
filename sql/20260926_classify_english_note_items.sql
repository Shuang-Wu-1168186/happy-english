-- Add durable language-register labels to English study-note cards.
--
-- Run this before 20260926_seed_english_note_item_language_labels.sql.
-- The guarded ALTER statements support MySQL 5.7+ and are safe to re-run.

SET @has_language_register := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note_item'
      AND column_name = 'language_register'
);
SET @add_language_register := IF(
    @has_language_register = 0,
    'ALTER TABLE `english_note_item` ADD COLUMN `language_register` VARCHAR(32) NOT NULL DEFAULT ''unclassified'' COMMENT ''语体：common_spoken、formal_spoken、written、mixed、neutral、reference'' AFTER `keywords`',
    'SELECT 1'
);
PREPARE add_language_register FROM @add_language_register;
EXECUTE add_language_register;
DEALLOCATE PREPARE add_language_register;

SET @has_usage_scenarios_json := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note_item'
      AND column_name = 'usage_scenarios_json'
);
SET @add_usage_scenarios_json := IF(
    @has_usage_scenarios_json = 0,
    'ALTER TABLE `english_note_item` ADD COLUMN `usage_scenarios_json` JSON DEFAULT NULL COMMENT ''适用场景标签 JSON 数组'' AFTER `language_register`',
    'SELECT 1'
);
PREPARE add_usage_scenarios_json FROM @add_usage_scenarios_json;
EXECUTE add_usage_scenarios_json;
DEALLOCATE PREPARE add_usage_scenarios_json;

SET @has_register_reason := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note_item'
      AND column_name = 'register_reason'
);
SET @add_register_reason := IF(
    @has_register_reason = 0,
    'ALTER TABLE `english_note_item` ADD COLUMN `register_reason` VARCHAR(500) DEFAULT NULL COMMENT ''语体判断说明'' AFTER `usage_scenarios_json`',
    'SELECT 1'
);
PREPARE add_register_reason FROM @add_register_reason;
EXECUTE add_register_reason;
DEALLOCATE PREPARE add_register_reason;

SET @has_classification_confidence := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note_item'
      AND column_name = 'classification_confidence'
);
SET @add_classification_confidence := IF(
    @has_classification_confidence = 0,
    'ALTER TABLE `english_note_item` ADD COLUMN `classification_confidence` TINYINT UNSIGNED DEFAULT NULL COMMENT ''自动判断置信度，0 至 100'' AFTER `register_reason`',
    'SELECT 1'
);
PREPARE add_classification_confidence FROM @add_classification_confidence;
EXECUTE add_classification_confidence;
DEALLOCATE PREPARE add_classification_confidence;

SET @has_classification_source := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note_item'
      AND column_name = 'classification_source'
);
SET @add_classification_source := IF(
    @has_classification_source = 0,
    'ALTER TABLE `english_note_item` ADD COLUMN `classification_source` VARCHAR(32) NOT NULL DEFAULT ''unclassified'' COMMENT ''标注来源：auto_rule_v1 或 manual'' AFTER `classification_confidence`',
    'SELECT 1'
);
PREPARE add_classification_source FROM @add_classification_source;
EXECUTE add_classification_source;
DEALLOCATE PREPARE add_classification_source;

SET @has_language_register_index := (
    SELECT COUNT(*)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note_item'
      AND index_name = 'idx_english_note_item_language_register'
);
SET @add_language_register_index := IF(
    @has_language_register_index = 0,
    'ALTER TABLE `english_note_item` ADD KEY `idx_english_note_item_language_register` (`language_register`)',
    'SELECT 1'
);
PREPARE add_language_register_index FROM @add_language_register_index;
EXECUTE add_language_register_index;
DEALLOCATE PREPARE add_language_register_index;

-- Release verification after the data-label migration has run.
SELECT
    `language_register`,
    COUNT(*) AS `item_count`,
    SUM(`classification_source` = 'manual') AS `manually_reviewed_count`
FROM `english_note_item`
GROUP BY `language_register`
ORDER BY `item_count` DESC, `language_register`;
