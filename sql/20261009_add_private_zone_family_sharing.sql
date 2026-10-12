-- Private-zone configuration and family sharing.
--
-- The private zone stores references to the existing learning catalogue. It
-- does not copy textbook, vocabulary, or course bodies. Family membership is
-- also independent from paid membership: it controls visibility of a saved
-- item, while course opening still resolves the current learner's entitlement.

CREATE TABLE IF NOT EXISTS `family_group` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(120) NOT NULL,
    `owner_user_id` BIGINT UNSIGNED DEFAULT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'active',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_family_group_owner_status` (`owner_user_id`, `status`),
    CONSTRAINT `fk_family_group_owner`
        FOREIGN KEY (`owner_user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='家庭学习组';

CREATE TABLE IF NOT EXISTS `family_group_member` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `family_group_id` BIGINT UNSIGNED NOT NULL,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `role` VARCHAR(20) NOT NULL DEFAULT 'member',
    `status` VARCHAR(20) NOT NULL DEFAULT 'active',
    `invited_by` BIGINT UNSIGNED DEFAULT NULL,
    `joined_at` DATETIME DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_family_group_member_user` (`family_group_id`, `user_id`),
    KEY `idx_family_group_member_user_status` (`user_id`, `status`),
    KEY `idx_family_group_member_group_status` (`family_group_id`, `status`),
    CONSTRAINT `fk_family_group_member_group`
        FOREIGN KEY (`family_group_id`) REFERENCES `family_group` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_family_group_member_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_family_group_member_invited_by`
        FOREIGN KEY (`invited_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='家庭学习组成员';

CREATE TABLE IF NOT EXISTS `private_zone_feature` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `feature_code` VARCHAR(80) NOT NULL,
    `title` VARCHAR(120) NOT NULL,
    `title_en` VARCHAR(120) DEFAULT NULL,
    `description` VARCHAR(500) DEFAULT NULL,
    `icon` VARCHAR(32) DEFAULT NULL,
    `route_key` VARCHAR(100) NOT NULL,
    `target_url` VARCHAR(1000) DEFAULT NULL,
    `config_json` JSON DEFAULT NULL,
    `sort_order` INT NOT NULL DEFAULT 0,
    `is_enabled` TINYINT(1) NOT NULL DEFAULT 1,
    `created_by` BIGINT UNSIGNED DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT UNSIGNED DEFAULT NULL,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_private_zone_feature_code` (`feature_code`),
    KEY `idx_private_zone_feature_enabled_order` (`is_enabled`, `sort_order`),
    CONSTRAINT `fk_private_zone_feature_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_private_zone_feature_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='私人专区功能配置';

CREATE TABLE IF NOT EXISTS `private_zone_item` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `scope_type` VARCHAR(20) NOT NULL COMMENT 'personal 或 family',
    `owner_user_id` BIGINT UNSIGNED DEFAULT NULL,
    `family_group_id` BIGINT UNSIGNED DEFAULT NULL,
    `resource_type` VARCHAR(30) NOT NULL COMMENT 'material、course、note、note_item',
    `resource_id` BIGINT UNSIGNED NOT NULL,
    `label` VARCHAR(255) DEFAULT NULL,
    `sort_order` INT NOT NULL DEFAULT 0,
    `status` VARCHAR(20) NOT NULL DEFAULT 'active',
    `added_by_user_id` BIGINT UNSIGNED DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_private_zone_item_user_status_order`
        (`owner_user_id`, `status`, `sort_order`),
    KEY `idx_private_zone_item_family_status_order`
        (`family_group_id`, `status`, `sort_order`),
    KEY `idx_private_zone_item_resource` (`resource_type`, `resource_id`),
    CONSTRAINT `fk_private_zone_item_owner`
        FOREIGN KEY (`owner_user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_private_zone_item_family`
        FOREIGN KEY (`family_group_id`) REFERENCES `family_group` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_private_zone_item_added_by`
        FOREIGN KEY (`added_by_user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='私人专区内容引用';

-- Existing notes remain platform records. New note rows can be personal or
-- family scoped and are therefore hidden from the legacy public content API.
SET @has_english_note_scope_type = (
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note'
      AND column_name = 'scope_type'
);
SET @add_english_note_scope_type = IF(
    @has_english_note_scope_type = 0,
    'ALTER TABLE `english_note` ADD COLUMN `scope_type` VARCHAR(20) NOT NULL DEFAULT ''platform'' COMMENT ''platform、personal、family'' AFTER `share_status`',
    'SELECT 1'
);
PREPARE add_english_note_scope_type FROM @add_english_note_scope_type;
EXECUTE add_english_note_scope_type;
DEALLOCATE PREPARE add_english_note_scope_type;

SET @has_english_note_owner_user_id = (
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note'
      AND column_name = 'owner_user_id'
);
SET @add_english_note_owner_user_id = IF(
    @has_english_note_owner_user_id = 0,
    'ALTER TABLE `english_note` ADD COLUMN `owner_user_id` BIGINT UNSIGNED DEFAULT NULL AFTER `scope_type`',
    'SELECT 1'
);
PREPARE add_english_note_owner_user_id FROM @add_english_note_owner_user_id;
EXECUTE add_english_note_owner_user_id;
DEALLOCATE PREPARE add_english_note_owner_user_id;

SET @has_english_note_family_group_id = (
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note'
      AND column_name = 'family_group_id'
);
SET @add_english_note_family_group_id = IF(
    @has_english_note_family_group_id = 0,
    'ALTER TABLE `english_note` ADD COLUMN `family_group_id` BIGINT UNSIGNED DEFAULT NULL AFTER `owner_user_id`',
    'SELECT 1'
);
PREPARE add_english_note_family_group_id FROM @add_english_note_family_group_id;
EXECUTE add_english_note_family_group_id;
DEALLOCATE PREPARE add_english_note_family_group_id;

SET @has_english_note_scope_index = (
    SELECT COUNT(*) FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note'
      AND index_name = 'idx_english_note_scope_owner_family'
);
SET @add_english_note_scope_index = IF(
    @has_english_note_scope_index = 0,
    'ALTER TABLE `english_note` ADD KEY `idx_english_note_scope_owner_family` (`scope_type`, `owner_user_id`, `family_group_id`)',
    'SELECT 1'
);
PREPARE add_english_note_scope_index FROM @add_english_note_scope_index;
EXECUTE add_english_note_scope_index;
DEALLOCATE PREPARE add_english_note_scope_index;

SET @has_english_note_owner_fk = (
    SELECT COUNT(*) FROM information_schema.table_constraints
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note'
      AND constraint_name = 'fk_english_note_owner_user'
);
SET @add_english_note_owner_fk = IF(
    @has_english_note_owner_fk = 0,
    'ALTER TABLE `english_note` ADD CONSTRAINT `fk_english_note_owner_user` FOREIGN KEY (`owner_user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL',
    'SELECT 1'
);
PREPARE add_english_note_owner_fk FROM @add_english_note_owner_fk;
EXECUTE add_english_note_owner_fk;
DEALLOCATE PREPARE add_english_note_owner_fk;

SET @has_english_note_family_fk = (
    SELECT COUNT(*) FROM information_schema.table_constraints
    WHERE table_schema = DATABASE()
      AND table_name = 'english_note'
      AND constraint_name = 'fk_english_note_family_group'
);
SET @add_english_note_family_fk = IF(
    @has_english_note_family_fk = 0,
    'ALTER TABLE `english_note` ADD CONSTRAINT `fk_english_note_family_group` FOREIGN KEY (`family_group_id`) REFERENCES `family_group` (`id`) ON DELETE SET NULL',
    'SELECT 1'
);
PREPARE add_english_note_family_fk FROM @add_english_note_family_fk;
EXECUTE add_english_note_family_fk;
DEALLOCATE PREPARE add_english_note_family_fk;

INSERT INTO `private_zone_feature`
    (`feature_code`, `title`, `title_en`, `description`, `icon`, `route_key`, `target_url`, `config_json`, `sort_order`, `is_enabled`)
VALUES
    ('my-english-notes', '我的英语笔记', 'My English Notes',
     '整理个人笔记、家庭共学笔记和复习内容。', 'notebook', 'private-notes',
     '/learn/notes', JSON_OBJECT('resource_types', JSON_ARRAY('note', 'note_item')), 10, 1),
    ('my-textbooks', '我的课本', 'My Textbooks',
     '收藏课本、教材和按单元组织的学习材料。', 'book-open', 'private-textbooks',
     '/learning-materials/1', JSON_OBJECT('resource_types', JSON_ARRAY('material'), 'material_types', JSON_ARRAY('textbook', 'book', 'courseware')), 20, 1),
    ('textbook-vocabulary', '课本单词', 'Textbook Vocabulary',
     '收藏课本单词、词卡和复习词表。', 'languages', 'textbook-vocabulary',
     '/learn/kids-cards', JSON_OBJECT('resource_types', JSON_ARRAY('material'), 'material_types', JSON_ARRAY('vocabulary', 'word_list', 'card_set', 'cards')), 30, 1),
    ('saved-learning', '我的学习内容', 'Saved Learning',
     '收藏课程和其他可复用的学习材料。', 'bookmark', 'saved-learning',
     '/private-zone/favorite-courses', JSON_OBJECT('resource_types', JSON_ARRAY('course', 'material')), 40, 1)
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `icon` = VALUES(`icon`),
    `route_key` = VALUES(`route_key`),
    `target_url` = COALESCE(NULLIF(`target_url`, ''), VALUES(`target_url`)),
    `config_json` = VALUES(`config_json`),
    `sort_order` = VALUES(`sort_order`);
