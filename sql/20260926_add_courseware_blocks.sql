-- Courseware block model for learning_material_lesson.
-- Existing lessons remain lesson_format = source and keep their current behaviour.

SET @has_lesson_format = (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material_lesson'
      AND column_name = 'lesson_format'
);
SET @add_lesson_format = IF(
    @has_lesson_format = 0,
    'ALTER TABLE `learning_material_lesson` ADD COLUMN `lesson_format` VARCHAR(50) NOT NULL DEFAULT ''source'' COMMENT ''source：既有来源内容；courseware：按课件区块渲染'' AFTER `content_json`, ADD KEY `idx_learning_material_lesson_format` (`lesson_format`, `is_published`)',
    'SELECT 1'
);
PREPARE add_lesson_format FROM @add_lesson_format;
EXECUTE add_lesson_format;
DEALLOCATE PREPARE add_lesson_format;

CREATE TABLE IF NOT EXISTS `courseware_block` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '课件区块主键ID',
    `material_lesson_id` BIGINT UNSIGNED NOT NULL COMMENT '所属教材课时ID',
    `block_code` VARCHAR(120) NOT NULL COMMENT '课时内稳定区块编码',
    `block_type` VARCHAR(50) NOT NULL COMMENT 'hero、usage_group、dialogue、comparison、output、recap',
    `title` VARCHAR(255) DEFAULT NULL COMMENT '区块标题',
    `payload_json` LONGTEXT NOT NULL COMMENT '按区块类型校验的内容 JSON',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '课时内排序',
    `status` VARCHAR(20) NOT NULL DEFAULT 'draft' COMMENT 'draft、published、archived',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_courseware_block_lesson_code` (`material_lesson_id`, `block_code`),
    KEY `idx_courseware_block_lesson_status_order` (`material_lesson_id`, `status`, `sort_order`),
    CONSTRAINT `fk_courseware_block_lesson`
        FOREIGN KEY (`material_lesson_id`) REFERENCES `learning_material_lesson` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_courseware_block_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_courseware_block_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课件教学区块表';

CREATE TABLE IF NOT EXISTS `courseware_block_source` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '课件区块来源主键ID',
    `courseware_block_id` BIGINT UNSIGNED NOT NULL COMMENT '所属课件区块ID',
    `source_resource` VARCHAR(80) NOT NULL COMMENT '来源类型，例如 english_note_item',
    `source_reference_id` BIGINT UNSIGNED NOT NULL COMMENT '来源记录主键ID',
    `source_field` VARCHAR(80) NOT NULL COMMENT '来源字段',
    `source_locator_json` LONGTEXT DEFAULT NULL COMMENT '字段内定位信息',
    `source_snapshot_text` MEDIUMTEXT NOT NULL COMMENT '发布时使用的原文快照',
    `source_hash` CHAR(64) DEFAULT NULL COMMENT '原文快照 SHA-256',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '同一课件区块内的来源顺序',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    PRIMARY KEY (`id`),
    KEY `idx_courseware_block_source_block_order` (`courseware_block_id`, `sort_order`),
    KEY `idx_courseware_block_source_reference` (`source_resource`, `source_reference_id`, `source_field`),
    CONSTRAINT `fk_courseware_block_source_block`
        FOREIGN KEY (`courseware_block_id`) REFERENCES `courseware_block` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课件区块内容来源表';
