-- Generic lesson content model.
-- learning_material_lesson remains the lesson identity so existing catalogue,
-- course access, and progress records keep their current IDs.

SET @has_lesson_schema_version = (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material_lesson'
      AND column_name = 'lesson_schema_version'
);
SET @add_lesson_schema_version = IF(
    @has_lesson_schema_version = 0,
    'ALTER TABLE `learning_material_lesson` ADD COLUMN `lesson_schema_version` INT NOT NULL DEFAULT 1 COMMENT ''通用课时内容版本'' AFTER `lesson_format`',
    'SELECT 1'
);
PREPARE add_lesson_schema_version FROM @add_lesson_schema_version;
EXECUTE add_lesson_schema_version;
DEALLOCATE PREPARE add_lesson_schema_version;

SET @has_content_status = (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material_lesson'
      AND column_name = 'content_status'
);
SET @add_content_status = IF(
    @has_content_status = 0,
    'ALTER TABLE `learning_material_lesson` ADD COLUMN `content_status` VARCHAR(20) NOT NULL DEFAULT ''draft'' COMMENT ''课时内容状态'' AFTER `lesson_schema_version`',
    'SELECT 1'
);
PREPARE add_content_status FROM @add_content_status;
EXECUTE add_content_status;
DEALLOCATE PREPARE add_content_status;

SET @has_published_at = (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material_lesson'
      AND column_name = 'published_at'
);
SET @add_published_at = IF(
    @has_published_at = 0,
    'ALTER TABLE `learning_material_lesson` ADD COLUMN `published_at` DATETIME DEFAULT NULL COMMENT ''课时内容发布时间'' AFTER `content_status`',
    'SELECT 1'
);
PREPARE add_published_at FROM @add_published_at;
EXECUTE add_published_at;
DEALLOCATE PREPARE add_published_at;

-- Preserve the visibility state of existing legacy lessons while their
-- content is still served through the compatibility reader.
UPDATE `learning_material_lesson`
SET `content_status` = CASE WHEN `is_published` = 1 THEN 'published' ELSE 'draft' END
WHERE `lesson_schema_version` = 1
  AND `content_status` = 'draft';

CREATE TABLE IF NOT EXISTS `learning_lesson_section` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `lesson_id` BIGINT UNSIGNED NOT NULL COMMENT '所属通用课时ID',
    `section_code` VARCHAR(50) NOT NULL COMMENT '内容区块编号',
    `title` VARCHAR(150) NOT NULL,
    `title_en` VARCHAR(150) NOT NULL,
    `sort_order` INT NOT NULL DEFAULT 0,
    `status` VARCHAR(20) NOT NULL DEFAULT 'draft',
    `created_by` BIGINT UNSIGNED DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT UNSIGNED DEFAULT NULL,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_lesson_section` (`lesson_id`, `section_code`),
    KEY `idx_learning_lesson_section_order` (`lesson_id`, `status`, `sort_order`),
    CONSTRAINT `fk_learning_lesson_section_lesson`
        FOREIGN KEY (`lesson_id`) REFERENCES `learning_material_lesson` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_lesson_section_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_lesson_section_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通用课时内容区块';

CREATE TABLE IF NOT EXISTS `learning_lesson_item` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `section_id` BIGINT UNSIGNED NOT NULL COMMENT '所属课时区块ID',
    `item_code` VARCHAR(120) NOT NULL,
    `item_order` INT NOT NULL DEFAULT 0,
    `title` VARCHAR(255) DEFAULT NULL,
    `payload_json` LONGTEXT NOT NULL COMMENT '按区块类型校验的内容JSON',
    `status` VARCHAR(20) NOT NULL DEFAULT 'draft',
    `created_by` BIGINT UNSIGNED DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT UNSIGNED DEFAULT NULL,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_lesson_item_code` (`section_id`, `item_code`),
    KEY `idx_learning_lesson_item_order` (`section_id`, `status`, `item_order`),
    CONSTRAINT `fk_learning_lesson_item_section`
        FOREIGN KEY (`section_id`) REFERENCES `learning_lesson_section` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_lesson_item_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_lesson_item_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通用课时内容项';
