-- A material owns one versioned rendering template.  Both the Web client and
-- the mini program register the same code/version pair, so the database never
-- stores a client-specific component name.

CREATE TABLE IF NOT EXISTS `learning_template` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '教材模板主键ID',
    `template_code` VARCHAR(80) NOT NULL COMMENT '稳定模板编号，例如 put-aside',
    `template_version` INT NOT NULL DEFAULT 1 COMMENT '模板渲染版本',
    `name` VARCHAR(120) NOT NULL COMMENT '后台展示名称',
    `description` TEXT DEFAULT NULL COMMENT '模板用途说明',
    `content_kind` VARCHAR(50) NOT NULL COMMENT 'courseware、dialogue 或 source',
    `supported_clients_json` TEXT NOT NULL COMMENT '已注册客户端，例如 ["web","mini"]',
    `config_json` TEXT DEFAULT NULL COMMENT '模板配置 JSON',
    `status` VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT 'active 或 inactive',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '后台排序',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_template_code_version` (`template_code`, `template_version`),
    KEY `idx_learning_template_status_order` (`status`, `sort_order`),
    CONSTRAINT `fk_learning_template_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_template_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教材跨端渲染模板表';

SET @has_material_template_id = (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material'
      AND column_name = 'template_id'
);
SET @add_material_template_id = IF(
    @has_material_template_id = 0,
    'ALTER TABLE `learning_material` ADD COLUMN `template_id` BIGINT UNSIGNED DEFAULT NULL COMMENT ''教材渲染模板ID'' AFTER `topic_id`, ADD KEY `idx_learning_material_template` (`template_id`)',
    'SELECT 1'
);
PREPARE add_material_template_id FROM @add_material_template_id;
EXECUTE add_material_template_id;
DEALLOCATE PREPARE add_material_template_id;

SET @has_material_template_fk = (
    SELECT COUNT(*)
    FROM information_schema.key_column_usage
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_material'
      AND constraint_name = 'fk_learning_material_template'
);
SET @add_material_template_fk = IF(
    @has_material_template_fk = 0,
    'ALTER TABLE `learning_material` ADD CONSTRAINT `fk_learning_material_template` FOREIGN KEY (`template_id`) REFERENCES `learning_template` (`id`) ON DELETE RESTRICT',
    'SELECT 1'
);
PREPARE add_material_template_fk FROM @add_material_template_fk;
EXECUTE add_material_template_fk;
DEALLOCATE PREPARE add_material_template_fk;

-- These records correspond to renderers checked into both client projects.
-- Rerunning the migration does not overwrite names, descriptions, activation,
-- order, or JSON configuration adjusted by an administrator.
INSERT INTO `learning_template`
    (`template_code`, `template_version`, `name`, `description`, `content_kind`, `supported_clients_json`, `config_json`, `status`, `sort_order`)
VALUES
    ('standard', 1, '通用课时', '适合句子、笔记和自包含内容的通用学习页。', 'source', '["web","mini"]', '{}', 'active', 10),
    ('put-aside', 1, 'Put aside 课件', '按短语、用法、情景和输出区块组织的课件。', 'courseware', '["web","mini"]', '{}', 'active', 20),
    ('dialogue', 1, '情景对话', '按词汇、对话和练习分区展示的口语对话页。', 'dialogue', '["web","mini"]', '{}', 'active', 30),
    ('textbook', 1, '课本课文', '按单元、课文和中英对照展示的教材页。', 'source', '["web","mini"]', '{}', 'active', 40),
    ('cards', 1, '单词卡片', '适合儿童卡片、数学卡片和词汇卡片的学习页。', 'source', '["web","mini"]', '{}', 'active', 50),
    ('phonics', 1, '自然拼读', '按音素、示例和小测展示的拼读学习页。', 'source', '["web","mini"]', '{}', 'active', 60),
    ('interview', 1, '面试练习', '按面试问题、答案和要点展示的练习页。', 'source', '["web","mini"]', '{}', 'active', 70)
ON DUPLICATE KEY UPDATE `template_code` = VALUES(`template_code`);

-- Existing content is inferred from its actual lesson shape first.  This
-- avoids assigning a source template to a material that was later converted
-- into courseware while its historical material_type still says textbook.
UPDATE `learning_material` material
SET material.`template_id` = (
    SELECT template.`id`
    FROM `learning_template` template
    WHERE template.`template_code` = CASE
        WHEN EXISTS (
            SELECT 1 FROM `learning_material_lesson` lesson
            WHERE lesson.`material_id` = material.`id`
              AND lesson.`lesson_format` = 'courseware'
        ) THEN 'put-aside'
        WHEN EXISTS (
            SELECT 1 FROM `learning_material_lesson` lesson
            WHERE lesson.`material_id` = material.`id`
              AND lesson.`source_resource` = 'dialogues'
        ) THEN 'dialogue'
        WHEN EXISTS (
            SELECT 1 FROM `learning_material_lesson` lesson
            WHERE lesson.`material_id` = material.`id`
              AND lesson.`source_resource` = 'textbook'
        ) THEN 'textbook'
        WHEN EXISTS (
            SELECT 1 FROM `learning_material_lesson` lesson
            WHERE lesson.`material_id` = material.`id`
              AND lesson.`source_resource` IN ('kids-cards', 'math-cards', 'vocabulary')
        ) THEN 'cards'
        WHEN EXISTS (
            SELECT 1 FROM `learning_material_lesson` lesson
            WHERE lesson.`material_id` = material.`id`
              AND lesson.`source_resource` = 'phonics'
        ) THEN 'phonics'
        WHEN EXISTS (
            SELECT 1 FROM `learning_material_lesson` lesson
            WHERE lesson.`material_id` = material.`id`
              AND lesson.`source_resource` = 'interviews'
        ) THEN 'interview'
        WHEN material.`material_type` = 'courseware' THEN 'put-aside'
        -- A sentence collection and a scene dialogue are both historically
        -- labelled dialogue, but only the latter uses the dialogue renderer.
        WHEN material.`material_type` = 'dialogue' THEN 'standard'
        WHEN material.`material_type` = 'phonics' THEN 'phonics'
        WHEN material.`material_type` IN ('card_set', 'vocabulary') THEN 'cards'
        WHEN material.`material_type` IN ('interview', 'exam') THEN 'interview'
        WHEN material.`material_type` = 'textbook' THEN 'textbook'
        ELSE 'standard'
    END
      AND template.`template_version` = 1
    LIMIT 1
)
WHERE material.`template_id` IS NULL;

-- The fallback above covers empty materials and legacy sentence collections.
UPDATE `learning_material` material
JOIN `learning_template` template
  ON template.`template_code` = 'standard'
 AND template.`template_version` = 1
SET material.`template_id` = template.`id`
WHERE material.`template_id` IS NULL;

-- Correct data that may have been backfilled by an earlier execution of this
-- migration before the sentence-collection distinction was added.
UPDATE `learning_material` material
JOIN `learning_template` current_template
  ON current_template.`id` = material.`template_id`
JOIN `learning_template` standard_template
  ON standard_template.`template_code` = 'standard'
 AND standard_template.`template_version` = 1
SET material.`template_id` = standard_template.`id`
WHERE material.`material_type` = 'dialogue'
  AND current_template.`template_code` = 'dialogue'
  AND EXISTS (
      SELECT 1 FROM `learning_material_lesson` lesson
      WHERE lesson.`material_id` = material.`id`
        AND lesson.`source_resource` = 'sentences'
  )
  AND NOT EXISTS (
      SELECT 1 FROM `learning_material_lesson` lesson
      WHERE lesson.`material_id` = material.`id`
        AND lesson.`source_resource` = 'dialogues'
  );
