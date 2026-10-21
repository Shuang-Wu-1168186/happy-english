-- Classify learning modules by the dimension they represent. Existing level
-- areas stay under `level`; private-zone remains a resource entry point.

START TRANSACTION;

SET @has_learning_module_type := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_module'
      AND column_name = 'module_type'
);

SET @add_learning_module_type := IF(
    @has_learning_module_type = 0,
    'ALTER TABLE `learning_module` ADD COLUMN `module_type` VARCHAR(20) NOT NULL DEFAULT ''level'' COMMENT ''模块维度：level-分级课程，training-训练专区，resource-资源入口'' AFTER `module_code`',
    'SELECT 1'
);

PREPARE add_learning_module_type FROM @add_learning_module_type;
EXECUTE add_learning_module_type;
DEALLOCATE PREPARE add_learning_module_type;

UPDATE `learning_module`
SET `module_type` = CASE
    WHEN `module_code` = 'private-zone' THEN 'resource'
    ELSE 'level'
END,
    `updated_at` = CURRENT_TIMESTAMP;

COMMIT;
