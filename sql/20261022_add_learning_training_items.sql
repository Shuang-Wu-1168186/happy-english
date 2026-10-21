-- Store playable resources for training modules.  The resource_type column is
-- intentionally generic so speaking and future training formats use the same
-- catalogue and client contract as podcast episodes.

START TRANSACTION;

CREATE TABLE IF NOT EXISTS `learning_training_item` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `module_id` BIGINT UNSIGNED NOT NULL,
    `resource_type` VARCHAR(30) NOT NULL DEFAULT 'podcast',
    `item_code` VARCHAR(100) NOT NULL,
    `title` VARCHAR(200) NOT NULL,
    `title_en` VARCHAR(200) NULL,
    `summary` VARCHAR(500) NULL,
    `description` TEXT NULL,
    `cover_image_url` VARCHAR(500) NULL,
    `audio_url` VARCHAR(500) NULL,
    `subtitle_url` VARCHAR(500) NULL,
    `difficulty_code` VARCHAR(50) NULL,
    `duration_seconds` INT NOT NULL DEFAULT 0,
    `episode_number` INT NOT NULL DEFAULT 0,
    `speaker` VARCHAR(200) NULL,
    `sort_order` INT NOT NULL DEFAULT 0,
    `is_published` TINYINT NOT NULL DEFAULT 1,
    `requires_membership` TINYINT NOT NULL DEFAULT 0,
    `created_by` BIGINT UNSIGNED NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT UNSIGNED NULL,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_learning_training_item_module_code` (`module_id`, `item_code`),
    KEY `idx_learning_training_item_public_order` (`module_id`, `resource_type`, `is_published`, `sort_order`),
    CONSTRAINT `fk_learning_training_item_module`
        FOREIGN KEY (`module_id`) REFERENCES `learning_module` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `learning_training_item`
    (`module_id`, `resource_type`, `item_code`, `title`, `title_en`, `summary`,
     `description`, `cover_image_url`, `audio_url`, `subtitle_url`,
     `difficulty_code`, `duration_seconds`, `episode_number`, `speaker`,
     `sort_order`, `is_published`, `requires_membership`)
SELECT lm.`id`, 'podcast', 'daily-life-listening', '生活场景听力', 'Daily Life Listening',
       '从购物、出行和日常交流开始，练习听懂真实语速。',
       '围绕日常生活的短篇 Podcast，先听主旨，再结合字幕完成精听。',
       '/static/training/podcast/daily-life-listening.jpg',
       '/static/training/podcast/daily-life-listening.mp3',
       '/static/training/podcast/daily-life-listening.vtt',
       'A2', 754, 1, 'HappyLingo Podcast', 10, 1, 0
FROM `learning_module` AS lm
LEFT JOIN `learning_training_item` AS existing
  ON existing.`module_id` = lm.`id`
 AND existing.`item_code` = 'daily-life-listening'
WHERE lm.`module_code` = 'podcast-listening'
  AND existing.`id` IS NULL;

INSERT INTO `learning_training_item`
    (`module_id`, `resource_type`, `item_code`, `title`, `title_en`, `summary`,
     `description`, `cover_image_url`, `audio_url`, `subtitle_url`,
     `difficulty_code`, `duration_seconds`, `episode_number`, `speaker`,
     `sort_order`, `is_published`, `requires_membership`)
SELECT lm.`id`, 'podcast', 'city-life-listening', '城市生活听力', 'City Life Listening',
       '听懂城市生活中的通知、问路和轻松对话。',
       '用稍快的语速训练关键信息捕捉，适合完成生活场景听力后的进阶练习。',
       '/static/training/podcast/city-life-listening.jpg',
       '/static/training/podcast/city-life-listening.mp3',
       '/static/training/podcast/city-life-listening.vtt',
       'B1', 927, 2, 'HappyLingo Podcast', 20, 1, 0
FROM `learning_module` AS lm
LEFT JOIN `learning_training_item` AS existing
  ON existing.`module_id` = lm.`id`
 AND existing.`item_code` = 'city-life-listening'
WHERE lm.`module_code` = 'podcast-listening'
  AND existing.`id` IS NULL;

COMMIT;
