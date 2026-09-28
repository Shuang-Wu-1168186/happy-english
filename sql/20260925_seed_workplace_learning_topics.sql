-- Add the Workplace English topics to an existing database after
-- 20260925_add_learning_catalog.sql has created the catalogue tables.

UPDATE `learning_module`
SET `description` = '面试英语、专业词汇和职场表达，提升工作场景沟通能力。'
WHERE `module_code` = 'workplace';

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'interview-english', '面试英语', 'Interview English',
       '围绕自我介绍、常见问题和完整回答，做好求职面试准备。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'workplace'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'professional-vocabulary', '专业词汇', 'Professional Vocabulary',
       '积累工作、技术和专业沟通常用的词汇与表达。', 20, 1
FROM `learning_module`
WHERE `module_code` = 'workplace'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);
