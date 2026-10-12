-- Private-zone personal tools and the initial platform shortcut records.
--
-- These are deliberately separate from english_note: English Note remains
-- curated learning content, while personal_note is a private free-form
-- notebook for every user.

CREATE TABLE IF NOT EXISTS `private_zone_shortcut` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `title` VARCHAR(120) NOT NULL,
    `target_url` VARCHAR(1000) NOT NULL,
    `description` VARCHAR(500) DEFAULT NULL,
    `icon` VARCHAR(32) DEFAULT NULL,
    `sort_order` INT NOT NULL DEFAULT 0,
    `status` VARCHAR(20) NOT NULL DEFAULT 'active',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_private_zone_shortcut_user_status_order` (`user_id`, `status`, `sort_order`),
    CONSTRAINT `fk_private_zone_shortcut_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='私人专区常用入口';

CREATE TABLE IF NOT EXISTS `personal_note` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `title` VARCHAR(200) NOT NULL,
    `content` TEXT DEFAULT NULL,
    `tags` VARCHAR(500) DEFAULT NULL,
    `color` VARCHAR(32) DEFAULT NULL,
    `is_pinned` TINYINT(1) NOT NULL DEFAULT 0,
    `status` VARCHAR(20) NOT NULL DEFAULT 'active',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_personal_note_user_status_pinned_updated`
        (`user_id`, `status`, `is_pinned`, `updated_at`),
    CONSTRAINT `fk_personal_note_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户个人笔记';

-- Give the built-in admin a few useful shared examples.  Administrator-owned
-- rows are displayed to every learner and are maintained in the admin console.
INSERT INTO `private_zone_shortcut`
    (`user_id`, `title`, `target_url`, `description`, `icon`, `sort_order`, `status`)
SELECT
    admin.`id`, defaults.`title`, defaults.`target_url`, defaults.`description`,
    defaults.`icon`, defaults.`sort_order`, 'active'
FROM `user` AS admin
JOIN (
    SELECT '我的 English Note' AS `title`, '/learn/notes' AS `target_url`,
           '进入原有的英语学习笔记。' AS `description`, '📝' AS `icon`, 10 AS `sort_order`
    UNION ALL SELECT '小学英语单词', '/learn/kids-cards', '打开原有的小学英语词卡，从 northeast 开始学习。', '🔤', 30
    UNION ALL SELECT '数学练习', '/learn/math-cards', '打开原有的数学知识卡和练习。', '➗', 40
) AS defaults
  ON admin.`username` = 'admin'
 AND admin.`role` = 'admin'
LEFT JOIN `private_zone_shortcut` AS existing
  ON existing.`user_id` = admin.`id`
 AND existing.`title` = defaults.`title`
WHERE existing.`id` IS NULL;

-- The textbook needs its database ID in the learner-facing route, so seed it
-- separately from the static shortcuts above.
INSERT INTO `private_zone_shortcut`
    (`user_id`, `title`, `target_url`, `description`, `icon`, `sort_order`, `status`)
SELECT
    admin.`id`, '小学英语教材 · Guoguo 对话',
    CONCAT('/learning-materials/', material.`id`),
    '打开小学英语教材，学习 Guoguo、Lingling、Maomao 的情景对话。', '📖', 20, 'active'
FROM `user` AS admin
JOIN `learning_material` AS material
  ON material.`material_code` = 'english-textbook-current'
 AND material.`is_published` = 1
LEFT JOIN `private_zone_shortcut` AS existing
  ON existing.`user_id` = admin.`id`
 AND existing.`title` = '小学英语教材 · Guoguo 对话'
WHERE admin.`username` = 'admin'
  AND admin.`role` = 'admin'
  AND existing.`id` IS NULL;
