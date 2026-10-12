-- The saved primary textbook is a learner-facing reading experience.  Its
-- parent topic must be public so direct material links can resolve.

UPDATE `learning_topic` AS topic
JOIN `learning_module` AS module
  ON module.`id` = topic.`module_id`
SET topic.`is_published` = 1
WHERE topic.`topic_code` = 'english-textbook'
  AND module.`module_code` IN ('foundation', 'elementary-english');

UPDATE `learning_material`
SET `is_published` = 1
WHERE `material_code` = 'english-textbook-current';
