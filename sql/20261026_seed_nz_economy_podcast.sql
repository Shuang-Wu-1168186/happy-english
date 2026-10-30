-- Add the NZME Economy of Everything episode to Podcast Listening.
-- The media files are deployed under data/static/training/podcast.

START TRANSACTION;

INSERT INTO `learning_training_item`
    (`module_id`, `resource_type`, `item_code`, `title`, `title_en`, `summary`,
     `description`, `cover_image_url`, `audio_url`, `subtitle_url`,
     `difficulty_code`, `duration_seconds`, `episode_number`, `speaker`,
     `sort_order`, `is_published`, `requires_membership`)
SELECT lm.`id`, 'podcast', 'nz-economy-recovery',
       '新西兰经济正在复苏，为什么体感却不是这样？',
       'NZ’s economy is recovering. So why doesn’t it feel like it?',
       '通过新西兰经济新闻 Podcast 练习理解观点、数据和现实生活中的经济感受。',
       '围绕新西兰经济复苏、企业倒闭、债务和选举前景展开的真实播客听力，适合训练较长对话中的事实、数字和观点理解。',
       '/static/training/podcast/podcast-default.svg',
       '/static/training/podcast/nz-economy-recovery.mp3',
       '/static/training/podcast/nz-economy-recovery.vtt',
       'B2', 1814, 4, 'The Economy of Everything', 40, 1, 0
FROM `learning_module` AS lm
LEFT JOIN `learning_training_item` AS existing
  ON existing.`module_id` = lm.`id`
 AND existing.`item_code` = 'nz-economy-recovery'
WHERE lm.`module_code` = 'podcast-listening'
  AND existing.`id` IS NULL;

COMMIT;
