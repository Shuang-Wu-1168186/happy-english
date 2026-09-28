-- Move the personal-notes entry below 私人专区.
--
-- Run after 20260926_restructure_learning_modules.sql on databases where the
-- six learning areas already exist.  This is idempotent and does not alter
-- english_note or english_note_item rows.

START TRANSACTION;

UPDATE `learning_module`
SET `name` = '私人专区',
    `name_en` = 'Private Zone',
    `description` = '集中查看个人学习笔记、重点卡片和复习内容。',
    `icon` = '🔒',
    `color` = '#64748B',
    `route_key` = 'private',
    `sort_order` = 60,
    `is_published` = 1
WHERE `module_code` = 'private-zone';

-- Move the legacy topic when there is no competing private-zone copy.  The
-- self join keeps a manually created private-zone topic intact if one exists.
UPDATE `learning_topic` AS `topic`
JOIN `learning_module` AS `private_module`
  ON `private_module`.`module_code` = 'private-zone'
LEFT JOIN `learning_topic` AS `private_copy`
  ON `private_copy`.`module_id` = `private_module`.`id`
 AND `private_copy`.`topic_code` = 'my-english-notes'
 AND `private_copy`.`id` <> `topic`.`id`
SET `topic`.`module_id` = `private_module`.`id`,
    `topic`.`title` = '我的英语笔记',
    `topic`.`title_en` = 'My English Notes',
    `topic`.`description` = '整理个人学习笔记、卡片和复习内容。',
    `topic`.`sort_order` = 10,
    `topic`.`is_published` = 1
WHERE `topic`.`topic_code` = 'my-english-notes'
  AND `private_copy`.`id` IS NULL;

-- A database that was restructured before the original notes topic was
-- imported still receives the same personal entry.
INSERT INTO `learning_topic`
    (`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `module`.`id`, 'my-english-notes', '我的英语笔记', 'My English Notes',
       '整理个人学习笔记、卡片和复习内容。', 10, 1
FROM `learning_module` AS `module`
WHERE `module`.`module_code` = 'private-zone'
  AND NOT EXISTS (
      SELECT 1
      FROM `learning_topic` AS `topic`
      WHERE `topic`.`module_id` = `module`.`id`
        AND `topic`.`topic_code` = 'my-english-notes'
  );

-- If a historical copy exists under another module, hide it so the learner
-- directory has exactly one visible "我的英语笔记" entry.
UPDATE `learning_topic` AS `topic`
JOIN `learning_module` AS `private_module`
  ON `private_module`.`module_code` = 'private-zone'
JOIN `learning_topic` AS `private_copy`
  ON `private_copy`.`module_id` = `private_module`.`id`
 AND `private_copy`.`topic_code` = 'my-english-notes'
SET `topic`.`is_published` = 0
WHERE `topic`.`topic_code` = 'my-english-notes'
  AND `topic`.`id` <> `private_copy`.`id`;

COMMIT;

SELECT
    `module`.`module_code`,
    `topic`.`topic_code`,
    `topic`.`title`,
    `topic`.`is_published`
FROM `learning_topic` AS `topic`
JOIN `learning_module` AS `module` ON `module`.`id` = `topic`.`module_id`
WHERE `topic`.`topic_code` = 'my-english-notes';
