-- Remove one known, abandoned travel topic before the current catalogue sync.
--
-- The row was created under beginner-english before the real travel curriculum
-- was created under intermediate-english.  It has no course mapping, material
-- or lesson.  The predicates intentionally make this a no-op for any real or
-- manually maintained topic.

START TRANSACTION;

DELETE `orphan_topic`
FROM `learning_topic` AS `orphan_topic`
JOIN `learning_module` AS `orphan_module`
  ON `orphan_module`.`id` = `orphan_topic`.`module_id`
JOIN `learning_topic` AS `active_topic`
  ON `active_topic`.`topic_code` = `orphan_topic`.`topic_code`
JOIN `learning_module` AS `active_module`
  ON `active_module`.`id` = `active_topic`.`module_id`
WHERE `orphan_module`.`module_code` = 'beginner-english'
  AND `orphan_topic`.`topic_code` = 'travel-english'
  AND `orphan_topic`.`title` = '旅游英语'
  AND `orphan_topic`.`title_en` = 'Travel English'
  AND `orphan_topic`.`description` IS NULL
  AND `orphan_topic`.`cover_url` IS NULL
  AND `orphan_topic`.`sort_order` = 0
  AND `orphan_topic`.`is_published` = 1
  AND `active_module`.`module_code` = 'intermediate-english'
  AND EXISTS (
      SELECT 1
      FROM `learning_topic_course` AS `active_mapping`
      WHERE `active_mapping`.`topic_id` = `active_topic`.`id`
  )
  AND NOT EXISTS (
      SELECT 1
      FROM `learning_topic_course` AS `orphan_mapping`
      WHERE `orphan_mapping`.`topic_id` = `orphan_topic`.`id`
  );

COMMIT;
