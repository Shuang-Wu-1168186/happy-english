-- Group published podcast episodes under learner-facing training topics.
-- This keeps a topic's editorial order on the server and lets clients render
-- the Podcast list without duplicating individual episodes on their home page.

START TRANSACTION;

ALTER TABLE `learning_training_item`
    ADD COLUMN `topic_id` BIGINT UNSIGNED NULL AFTER `module_id`,
    ADD KEY `idx_learning_training_item_topic_public_order`
        (`topic_id`, `resource_type`, `is_published`, `sort_order`),
    ADD CONSTRAINT `fk_learning_training_item_topic`
        FOREIGN KEY (`topic_id`) REFERENCES `learning_topic` (`id`) ON DELETE SET NULL;

INSERT INTO `learning_topic`
    (`module_id`, `topic_code`, `title`, `title_en`, `description`, `cover_url`, `sort_order`, `is_published`)
SELECT lm.`id`, 'new-zealand-podcast', '新西兰 Podcast', 'New Zealand Podcast',
       '通过新西兰真实新闻播客，练习听懂事实、观点、数字和自然语速。',
       '/static/training/podcast/podcast-default.svg', 10, 1
FROM `learning_module` AS lm
WHERE lm.`module_code` = 'podcast-listening'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `cover_url` = VALUES(`cover_url`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`),
    `updated_at` = CURRENT_TIMESTAMP;

UPDATE `learning_training_item` AS item
JOIN `learning_module` AS module
  ON module.`id` = item.`module_id`
JOIN `learning_topic` AS topic
  ON topic.`module_id` = module.`id`
 AND topic.`topic_code` = 'new-zealand-podcast'
SET item.`topic_id` = topic.`id`,
    item.`updated_at` = CURRENT_TIMESTAMP
WHERE module.`module_code` = 'podcast-listening'
  AND item.`item_code` IN (
      'maggots-missed-cancer-rest-home-investigation',
      'music-lesson-teacher-career',
      'repeat-offender-sentencing-discount',
      'nz-economy-recovery'
  );

COMMIT;
