-- Vocabulary-memory content, learner state, and append-only review history.
-- The seed at the end mirrors the initial software-English deck used by the
-- client prototype, so a deployment has one complete deck to exercise.

START TRANSACTION;

CREATE TABLE IF NOT EXISTS `vocabulary_deck` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `deck_code` VARCHAR(100) NOT NULL,
    `title` VARCHAR(200) NOT NULL,
    `title_en` VARCHAR(200) DEFAULT NULL,
    `description` TEXT DEFAULT NULL,
    `category` VARCHAR(100) DEFAULT NULL,
    `cover_image_url` VARCHAR(500) DEFAULT NULL,
    `difficulty_code` VARCHAR(50) DEFAULT NULL,
    `sort_order` INT NOT NULL DEFAULT 0,
    `is_published` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_vocabulary_deck_code` (`deck_code`),
    KEY `idx_vocabulary_deck_published_order` (`is_published`, `sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='可发布的单词记忆词库包';

CREATE TABLE IF NOT EXISTS `vocabulary_word` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `word` VARCHAR(255) NOT NULL,
    `normalized_word` VARCHAR(255) NOT NULL,
    `phonetic_uk` VARCHAR(255) DEFAULT NULL,
    `phonetic_us` VARCHAR(255) DEFAULT NULL,
    `audio_url` VARCHAR(500) DEFAULT NULL,
    `word_level` VARCHAR(50) DEFAULT NULL,
    `tags_json` TEXT DEFAULT NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_vocabulary_word_normalized` (`normalized_word`),
    KEY `idx_vocabulary_word_active_normalized` (`is_active`, `normalized_word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='可跨词库复用的英语单词主数据';

CREATE TABLE IF NOT EXISTS `vocabulary_word_sense` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `word_id` BIGINT UNSIGNED NOT NULL,
    `part_of_speech` VARCHAR(32) DEFAULT NULL,
    `translation` VARCHAR(500) NOT NULL,
    `definition` TEXT DEFAULT NULL,
    `memory_hint` TEXT DEFAULT NULL,
    `sort_order` INT NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_vocabulary_word_sense_order` (`word_id`, `sort_order`),
    KEY `idx_vocabulary_word_sense_word_order` (`word_id`, `sort_order`),
    CONSTRAINT `fk_vocabulary_word_sense_word`
        FOREIGN KEY (`word_id`) REFERENCES `vocabulary_word` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='单词词义、释义和记忆提示';

CREATE TABLE IF NOT EXISTS `vocabulary_word_example` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `sense_id` BIGINT UNSIGNED NOT NULL,
    `english_text` TEXT NOT NULL,
    `chinese_text` TEXT DEFAULT NULL,
    `sort_order` INT NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_vocabulary_word_example_order` (`sense_id`, `sort_order`),
    KEY `idx_vocabulary_word_example_sense_order` (`sense_id`, `sort_order`),
    CONSTRAINT `fk_vocabulary_word_example_sense`
        FOREIGN KEY (`sense_id`) REFERENCES `vocabulary_word_sense` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='单词词义例句';

CREATE TABLE IF NOT EXISTS `vocabulary_deck_word` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `deck_id` BIGINT UNSIGNED NOT NULL,
    `word_id` BIGINT UNSIGNED NOT NULL,
    `sort_order` INT NOT NULL DEFAULT 0,
    `is_enabled` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_vocabulary_deck_word` (`deck_id`, `word_id`),
    UNIQUE KEY `uk_vocabulary_deck_word_order` (`deck_id`, `sort_order`),
    KEY `idx_vocabulary_deck_word_deck_enabled_order` (`deck_id`, `is_enabled`, `sort_order`),
    CONSTRAINT `fk_vocabulary_deck_word_deck`
        FOREIGN KEY (`deck_id`) REFERENCES `vocabulary_deck` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_vocabulary_deck_word_word`
        FOREIGN KEY (`word_id`) REFERENCES `vocabulary_word` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='词库包内的单词顺序和启用状态';

CREATE TABLE IF NOT EXISTS `user_vocabulary_progress` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `deck_word_id` BIGINT UNSIGNED NOT NULL,
    `learning_state` VARCHAR(20) NOT NULL DEFAULT 'new',
    `mastery_level` INT NOT NULL DEFAULT 0,
    `is_marked` TINYINT(1) NOT NULL DEFAULT 0,
    `seen_count` INT UNSIGNED NOT NULL DEFAULT 0,
    `review_count` INT UNSIGNED NOT NULL DEFAULT 0,
    `correct_count` INT UNSIGNED NOT NULL DEFAULT 0,
    `last_rating` VARCHAR(20) DEFAULT NULL,
    `last_reviewed_at` DATETIME DEFAULT NULL,
    `next_review_at` DATETIME DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_vocabulary_progress_card` (`user_id`, `deck_word_id`),
    KEY `idx_user_vocabulary_progress_user_due` (`user_id`, `next_review_at`),
    KEY `idx_user_vocabulary_progress_user_state` (`user_id`, `learning_state`),
    CONSTRAINT `fk_user_vocabulary_progress_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_vocabulary_progress_card`
        FOREIGN KEY (`deck_word_id`) REFERENCES `vocabulary_deck_word` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='用户在某个词库卡片上的当前学习进度';

CREATE TABLE IF NOT EXISTS `vocabulary_review_log` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `deck_word_id` BIGINT UNSIGNED NOT NULL,
    `rating` VARCHAR(20) NOT NULL,
    `previous_mastery_level` INT NOT NULL DEFAULT 0,
    `mastery_level` INT NOT NULL DEFAULT 0,
    `duration_millis` INT UNSIGNED DEFAULT NULL,
    `reviewed_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `next_review_at` DATETIME DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_vocabulary_review_log_user_card_reviewed`
        (`user_id`, `deck_word_id`, `reviewed_at`),
    KEY `idx_vocabulary_review_log_card_reviewed` (`deck_word_id`, `reviewed_at`),
    CONSTRAINT `fk_vocabulary_review_log_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_vocabulary_review_log_card`
        FOREIGN KEY (`deck_word_id`) REFERENCES `vocabulary_deck_word` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='用户单词复习操作流水';

-- One complete deck is seeded for the initial mobile interaction prototype.
INSERT IGNORE INTO `vocabulary_deck`
    (`deck_code`, `title`, `title_en`, `description`, `category`, `difficulty_code`, `sort_order`, `is_published`)
VALUES
    ('software-english-demo', '技术英语（软件开发）', 'Software Development English',
     '软件开发中常见的核心表达。', '技术英语', 'B1', 10, 1);

INSERT IGNORE INTO `vocabulary_word`
    (`word`, `normalized_word`, `phonetic_uk`, `phonetic_us`, `word_level`, `tags_json`)
VALUES
    ('refine', 'refine', '/rɪˈfaɪn/', '/rɪˈfaɪn/', 'B1', '["technical","software"]'),
    ('reliable', 'reliable', '/rɪˈlaɪəb(ə)l/', '/rɪˈlaɪəb(ə)l/', 'B1', '["technical","software"]'),
    ('deploy', 'deploy', '/dɪˈplɔɪ/', '/dɪˈplɔɪ/', 'B1', '["technical","software"]'),
    ('iterate', 'iterate', '/ˈɪtəreɪt/', '/ˈɪtəreɪt/', 'B2', '["technical","software"]'),
    ('scalable', 'scalable', '/ˈskeɪləb(ə)l/', '/ˈskeɪləb(ə)l/', 'B2', '["technical","software"]'),
    ('maintain', 'maintain', '/meɪnˈteɪn/', '/meɪnˈteɪn/', 'B1', '["technical","software"]'),
    ('validate', 'validate', '/ˈvælɪdeɪt/', '/ˈvælɪdeɪt/', 'B1', '["technical","software"]'),
    ('efficient', 'efficient', '/ɪˈfɪʃ(ə)nt/', '/ɪˈfɪʃ(ə)nt/', 'B1', '["technical","software"]'),
    ('dependency', 'dependency', '/dɪˈpendənsi/', '/dɪˈpendənsi/', 'B2', '["technical","software"]'),
    ('compatible', 'compatible', '/kəmˈpætəb(ə)l/', '/kəmˈpætəb(ə)l/', 'B2', '["technical","software"]'),
    ('optimize', 'optimize', '/ˈɒptɪmaɪz/', '/ˈɑːptɪmaɪz/', 'B2', '["technical","software"]'),
    ('resolve', 'resolve', '/rɪˈzɒlv/', '/rɪˈzɑːlv/', 'B1', '["technical","software"]');

INSERT IGNORE INTO `vocabulary_word_sense`
    (`word_id`, `part_of_speech`, `translation`, `definition`, `memory_hint`, `sort_order`)
SELECT word.`id`, seed.`part_of_speech`, seed.`translation`, seed.`definition`, seed.`memory_hint`, 1
FROM `vocabulary_word` AS word
JOIN (
    SELECT 'refine' AS `normalized_word`, 'verb' AS `part_of_speech`, '完善；提炼' AS `translation`,
           '通过小幅调整，让内容或方案变得更好。' AS `definition`,
           're- 表示反复，fine 表示精细：反复打磨，变得更精细。' AS `memory_hint`
    UNION ALL SELECT 'reliable', 'adjective', '可靠的；可信赖的',
           '能够稳定、按预期工作，值得依赖。', 'rely 是“依赖”，reliable 就是“可以被依赖的”。'
    UNION ALL SELECT 'deploy', 'verb', '部署；发布',
           '把应用或服务发布到可供用户使用的环境中。', '开发完成后把程序布置到服务器上，就是 deploy。'
    UNION ALL SELECT 'iterate', 'verb', '迭代；反复改进',
           '根据反馈重复调整同一件事，使它逐步变好。', '不是一次做完，而是做、反馈、再做的循环。'
    UNION ALL SELECT 'scalable', 'adjective', '可扩展的',
           '在用户或数据增长时，仍能有效运作并容易扩大规模。', 'scale 是规模；scalable 就是能随着规模变大的。'
    UNION ALL SELECT 'maintain', 'verb', '维护；保持',
           '持续让系统保持正常、稳定的状态。', 'main + tain：把主要状态拿住，就是维持和维护。'
    UNION ALL SELECT 'validate', 'verb', '验证；校验',
           '检查数据、想法或功能是否符合要求、是否有效。', 'valid 是“有效的”，validate 就是确认它是否有效。'
    UNION ALL SELECT 'efficient', 'adjective', '高效的',
           '用较少的时间、资源或步骤完成目标。', 'efficiency 是效率；efficient 是“有效率的”。'
    UNION ALL SELECT 'dependency', 'noun', '依赖项；依赖关系',
           '项目运行或构建时需要的其他库、模块或服务。', 'depend 是依赖；dependency 是被依赖的那一项。'
    UNION ALL SELECT 'compatible', 'adjective', '兼容的',
           '能够和另一种系统、设备或版本一起正常使用。', '能够一起工作、不冲突，就是 compatible。'
    UNION ALL SELECT 'optimize', 'verb', '优化',
           '调整实现方式，让性能、体验或资源使用达到更好的结果。', 'optimal 是“最佳的”，optimize 就是朝最佳状态调整。'
    UNION ALL SELECT 'resolve', 'verb', '解决；解析',
           '处理问题、冲突或错误，使其得到明确结果。', '看到 bug 被 resolve，就可以理解为问题被解决了。'
) AS seed ON seed.`normalized_word` = word.`normalized_word`;

INSERT IGNORE INTO `vocabulary_word_example`
    (`sense_id`, `english_text`, `chinese_text`, `sort_order`)
SELECT sense.`id`, seed.`english_text`, seed.`chinese_text`, 1
FROM `vocabulary_word` AS word
JOIN `vocabulary_word_sense` AS sense
  ON sense.`word_id` = word.`id`
 AND sense.`sort_order` = 1
JOIN (
    SELECT 'refine' AS `normalized_word`, 'We need to refine the design before launch.' AS `english_text`,
           '我们需要在上线前完善这个设计。' AS `chinese_text`
    UNION ALL SELECT 'reliable', 'We need a reliable way to store user data.',
           '我们需要一种可靠的方式来存储用户数据。'
    UNION ALL SELECT 'deploy', 'The team will deploy the update tonight.',
           '团队会在今晚部署这次更新。'
    UNION ALL SELECT 'iterate', 'We can iterate on the prototype after user testing.',
           '用户测试后，我们再迭代这个原型。'
    UNION ALL SELECT 'scalable', 'We need a scalable architecture for future growth.',
           '我们需要一个可扩展的架构来支持未来增长。'
    UNION ALL SELECT 'maintain', 'Clean code is easier to maintain over time.',
           '整洁的代码更容易长期维护。'
    UNION ALL SELECT 'validate', 'Validate the form before sending the request.',
           '发送请求前先校验表单。'
    UNION ALL SELECT 'efficient', 'This query is more efficient on a large dataset.',
           '这个查询在大数据集上更高效。'
    UNION ALL SELECT 'dependency', 'Update the dependency to fix the security issue.',
           '更新这个依赖项以修复安全问题。'
    UNION ALL SELECT 'compatible', 'The new API is compatible with older clients.',
           '新的 API 与旧版客户端兼容。'
    UNION ALL SELECT 'optimize', 'We optimized the image loading time.',
           '我们优化了图片加载时间。'
    UNION ALL SELECT 'resolve', 'The patch resolves a crash on startup.',
           '这个补丁解决了启动时崩溃的问题。'
) AS seed ON seed.`normalized_word` = word.`normalized_word`;

INSERT IGNORE INTO `vocabulary_deck_word` (`deck_id`, `word_id`, `sort_order`, `is_enabled`)
SELECT deck.`id`, word.`id`, seed.`sort_order`, 1
FROM `vocabulary_deck` AS deck
JOIN (
    SELECT 'refine' AS `normalized_word`, 10 AS `sort_order`
    UNION ALL SELECT 'reliable', 20
    UNION ALL SELECT 'deploy', 30
    UNION ALL SELECT 'iterate', 40
    UNION ALL SELECT 'scalable', 50
    UNION ALL SELECT 'maintain', 60
    UNION ALL SELECT 'validate', 70
    UNION ALL SELECT 'efficient', 80
    UNION ALL SELECT 'dependency', 90
    UNION ALL SELECT 'compatible', 100
    UNION ALL SELECT 'optimize', 110
    UNION ALL SELECT 'resolve', 120
) AS seed
JOIN `vocabulary_word` AS word ON word.`normalized_word` = seed.`normalized_word`
WHERE deck.`deck_code` = 'software-english-demo';

COMMIT;
