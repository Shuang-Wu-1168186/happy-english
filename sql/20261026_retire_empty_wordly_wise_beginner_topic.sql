-- The original beginner-level Wordlywise3000 topic has no course mappings.
-- The active Wordly Wise catalogue lives in intermediate-english topic `w`.
-- Keep the empty legacy card out of client navigation so it cannot lead to an
-- apparently broken "暂无可学习内容" page.

START TRANSACTION;

UPDATE `learning_topic` AS `topic`
JOIN `learning_module` AS `module`
  ON `module`.`id` = `topic`.`module_id`
SET `topic`.`is_published` = 0,
    `topic`.`updated_at` = CURRENT_TIMESTAMP
WHERE `module`.`module_code` = 'beginner-english'
  AND `topic`.`topic_code` = 'v'
  AND `topic`.`title` = 'Wordlywise3000'
  AND NOT EXISTS (
      SELECT 1
      FROM `learning_topic_course` AS `mapping`
      WHERE `mapping`.`topic_id` = `topic`.`id`
  );

COMMIT;
