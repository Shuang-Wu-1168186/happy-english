-- Per-user manual "遇到一次" counts for vocabulary and expressions in English notes.
CREATE TABLE IF NOT EXISTS `english_note_item_frequency` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '笔记词条出现频次主键ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '学习用户ID',
    `note_item_id` BIGINT UNSIGNED NOT NULL COMMENT '英语笔记词条ID',
    `frequency_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '用户手动记录的遇到次数',
    `last_recorded_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近一次记录时间',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_english_note_item_frequency_user_item` (`user_id`, `note_item_id`),
    KEY `idx_english_note_item_frequency_user_count` (`user_id`, `frequency_count`),
    CONSTRAINT `fk_english_note_item_frequency_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_english_note_item_frequency_item`
        FOREIGN KEY (`note_item_id`) REFERENCES `english_note_item` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户笔记词条遇到频次';
