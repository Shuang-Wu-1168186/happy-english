-- Add the Everyday Speaking topics to an existing database after
-- 20260925_add_learning_catalog.sql has created the catalogue tables.

UPDATE `learning_module`
SET `description` = '每日口语与真实场景对话，帮助你自然开口。'
WHERE `module_code` = 'daily-speaking';

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'daily-speaking-practice', '每日口语', 'Daily Speaking',
       '每天练习实用句子和短语，让开口成为自然习惯。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'daily-speaking'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'daily-speaking-dialogues', '日常口语对话专区', 'Daily Spoken Dialogues',
       '围绕真实生活场景学习成组对话，练习自然回应。', 20, 1
FROM `learning_module`
WHERE `module_code` = 'daily-speaking'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);
