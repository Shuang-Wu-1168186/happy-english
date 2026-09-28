-- Add the Foundation Learning topics to an existing database after
-- 20260925_add_learning_catalog.sql has created the catalogue tables.

UPDATE `learning_module`
SET `description` = '英文课本、自然拼读和课本单词，按方向打好英语基础。'
WHERE `module_code` = 'foundation';

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'english-textbook', '英文课本', 'English Textbook',
       '跟着课文听读、理解和练习，按单元建立扎实基础。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'foundation'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'natural-phonics', '自然拼读', 'Natural Phonics',
       '从字母、音素和拼读规律开始，练出见词能读的能力。', 20, 1
FROM `learning_module`
WHERE `module_code` = 'foundation'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'textbook-vocabulary', '课本单词', 'Textbook Vocabulary',
       '围绕课本单元积累核心单词、发音和例句。', 30, 1
FROM `learning_module`
WHERE `module_code` = 'foundation'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);
