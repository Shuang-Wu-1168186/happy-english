-- Publish the podcast audio already present in data/audio. The files are
-- copied to data/static/training/podcast during deployment. This migration
-- keeps their public paths and editorial metadata in the database.

START TRANSACTION;

UPDATE `learning_training_item`
SET `is_published` = 0,
    `updated_at` = CURRENT_TIMESTAMP
WHERE `item_code` IN ('daily-life-listening', 'city-life-listening')
  AND `audio_url` IN (
      '/static/training/podcast/daily-life-listening.mp3',
      '/static/training/podcast/city-life-listening.mp3'
  );

INSERT INTO `learning_training_item`
    (`module_id`, `resource_type`, `item_code`, `title`, `title_en`, `summary`,
     `description`, `cover_image_url`, `audio_url`, `subtitle_url`,
     `difficulty_code`, `duration_seconds`, `episode_number`, `speaker`,
     `sort_order`, `is_published`, `requires_membership`)
SELECT lm.`id`, 'podcast', 'maggots-missed-cancer-rest-home-investigation',
       '养老院调查：被忽视的照护问题',
       'Maggots and Missed Cancer: Rest Home Investigation',
       '通过新闻调查练习理解事实、细节和事件经过。',
       '一篇关于养老院调查的真实新闻听力，适合训练较长篇幅内容中的关键信息捕捉。',
       '/static/training/podcast/podcast-default.svg',
       '/static/training/podcast/maggots-missed-cancer-rest-home-investigation.mp3',
       '/static/training/podcast/maggots-missed-cancer-rest-home-investigation.vtt',
       'B2', 952, 1, 'News Podcast', 10, 1, 0
FROM `learning_module` AS lm
LEFT JOIN `learning_training_item` AS existing
  ON existing.`module_id` = lm.`id`
 AND existing.`item_code` = 'maggots-missed-cancer-rest-home-investigation'
WHERE lm.`module_code` = 'podcast-listening'
  AND existing.`id` IS NULL;

INSERT INTO `learning_training_item`
    (`module_id`, `resource_type`, `item_code`, `title`, `title_en`, `summary`,
     `description`, `cover_image_url`, `audio_url`, `subtitle_url`,
     `difficulty_code`, `duration_seconds`, `episode_number`, `speaker`,
     `sort_order`, `is_published`, `requires_membership`)
SELECT lm.`id`, 'podcast', 'music-lesson-teacher-career',
       '音乐课改变了老师的职业生涯',
       'The Music Lesson That Ended a Teacher’s Career',
       '围绕教育新闻练习听懂人物、原因和结果。',
       '一篇教育新闻 Podcast，适合练习人物关系、因果关系和叙事细节。',
       '/static/training/podcast/podcast-default.svg',
       '/static/training/podcast/music-lesson-teacher-career.mp3',
       '/static/training/podcast/music-lesson-teacher-career.vtt',
       'B2', 1067, 2, 'News Podcast', 20, 1, 0
FROM `learning_module` AS lm
LEFT JOIN `learning_training_item` AS existing
  ON existing.`module_id` = lm.`id`
 AND existing.`item_code` = 'music-lesson-teacher-career'
WHERE lm.`module_code` = 'podcast-listening'
  AND existing.`id` IS NULL;

INSERT INTO `learning_training_item`
    (`module_id`, `resource_type`, `item_code`, `title`, `title_en`, `summary`,
     `description`, `cover_image_url`, `audio_url`, `subtitle_url`,
     `difficulty_code`, `duration_seconds`, `episode_number`, `speaker`,
     `sort_order`, `is_published`, `requires_membership`)
SELECT lm.`id`, 'podcast', 'repeat-offender-sentencing-discount',
       '重复违法者为何获得量刑折扣',
       'Why a Repeat Offender Got a 55% Sentencing Discount',
       '通过法律新闻训练理解数字、观点和复杂解释。',
       '一篇法律新闻听力，包含数字信息和较复杂的解释，适合作为进阶训练。',
       '/static/training/podcast/podcast-default.svg',
       '/static/training/podcast/repeat-offender-sentencing-discount.mp3',
       '/static/training/podcast/repeat-offender-sentencing-discount.vtt',
       'B2', 1470, 3, 'News Podcast', 30, 1, 0
FROM `learning_module` AS lm
LEFT JOIN `learning_training_item` AS existing
  ON existing.`module_id` = lm.`id`
 AND existing.`item_code` = 'repeat-offender-sentencing-discount'
WHERE lm.`module_code` = 'podcast-listening'
  AND existing.`id` IS NULL;

COMMIT;
