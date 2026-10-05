-- Optional visual for individual material lessons.  Commute micro lessons
-- require a local illustration smaller than 100KB at publish time.

SET @has_lesson_illustration_url = (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material_lesson'
      AND column_name = 'illustration_url'
);
SET @add_lesson_illustration_url = IF(
    @has_lesson_illustration_url = 0,
    'ALTER TABLE `learning_material_lesson` ADD COLUMN `illustration_url` VARCHAR(500) DEFAULT NULL COMMENT ''课时小配图地址'' AFTER `summary`',
    'SELECT 1'
);
PREPARE add_lesson_illustration_url FROM @add_lesson_illustration_url;
EXECUTE add_lesson_illustration_url;
DEALLOCATE PREPARE add_lesson_illustration_url;
