-- Give the built-in admin account a useful starting private learning space.
--
-- These are references to the existing catalogue records, not copies of the
-- notes, questions, textbook, or vocabulary.  A removed (archived) favourite
-- is deliberately not recreated when this migration is run again.

START TRANSACTION;

INSERT INTO `private_zone_feature`
    (`feature_code`, `title`, `title_en`, `description`, `icon`, `route_key`, `target_url`, `config_json`, `sort_order`, `is_enabled`)
VALUES
    ('textbook-vocabulary', '课本单词', 'Textbook Vocabulary',
     '收藏小学课本单词、词卡和复习词表。', 'languages', 'textbook-vocabulary',
     '/learn/kids-cards',
     JSON_OBJECT(
         'resource_types', JSON_ARRAY('material'),
         'material_types', JSON_ARRAY('card_set', 'cards'),
         'material_code_prefixes', JSON_ARRAY('kids-cards-')
     ), 30, 1),
    ('my-interview-questions', '我的面试题', 'My Interview Practice',
     '收藏常见面试题、技术面试题和回答练习。', 'briefcase', 'private-interviews',
     '/learn/interviews',
     JSON_OBJECT('resource_types', JSON_ARRAY('material'), 'material_types', JSON_ARRAY('interview')),
     35, 1)
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `icon` = VALUES(`icon`),
    `route_key` = VALUES(`route_key`),
    `target_url` = COALESCE(NULLIF(`target_url`, ''), VALUES(`target_url`)),
    `config_json` = VALUES(`config_json`),
    `sort_order` = VALUES(`sort_order`),
    `is_enabled` = VALUES(`is_enabled`);

-- The four direct learning entries above are the learner-facing navigation.
-- Keep generic course favourites in the saved-content list without showing a
-- fifth, duplicate "我的学习内容" entry card below them.
UPDATE `private_zone_feature`
SET `is_enabled` = 0
WHERE `feature_code` = 'saved-learning';

-- The existing notes remain platform records, so they still work from the
-- legacy note screen.  The personal favourite is what makes them appear in
-- the admin's private space.
INSERT INTO `private_zone_item`
    (`scope_type`, `owner_user_id`, `family_group_id`, `resource_type`, `resource_id`,
     `label`, `sort_order`, `status`, `added_by_user_id`)
SELECT
    'personal', admin.`id`, NULL, 'note', note.`id`, NULL,
    note.`priority_order`, 'active', admin.`id`
FROM `english_note` AS note
JOIN `user` AS admin
  ON admin.`username` = 'admin'
 AND admin.`role` = 'admin'
LEFT JOIN `private_zone_item` AS existing
  ON existing.`scope_type` = 'personal'
 AND existing.`owner_user_id` = admin.`id`
 AND existing.`resource_type` = 'note'
 AND existing.`resource_id` = note.`id`
WHERE note.`scope_type` = 'platform'
  AND note.`created_by` = admin.`id`
  AND existing.`id` IS NULL;

INSERT INTO `private_zone_item`
    (`scope_type`, `owner_user_id`, `family_group_id`, `resource_type`, `resource_id`,
     `label`, `sort_order`, `status`, `added_by_user_id`)
SELECT
    'personal', admin.`id`, NULL, 'material', material.`id`, NULL,
    material.`sort_order`, 'active', admin.`id`
FROM `learning_material` AS material
JOIN `user` AS admin
  ON admin.`username` = 'admin'
 AND admin.`role` = 'admin'
LEFT JOIN `private_zone_item` AS existing
  ON existing.`scope_type` = 'personal'
 AND existing.`owner_user_id` = admin.`id`
 AND existing.`resource_type` = 'material'
 AND existing.`resource_id` = material.`id`
WHERE material.`is_published` = 1
  AND material.`material_type` = 'interview'
  AND existing.`id` IS NULL;

INSERT INTO `private_zone_item`
    (`scope_type`, `owner_user_id`, `family_group_id`, `resource_type`, `resource_id`,
     `label`, `sort_order`, `status`, `added_by_user_id`)
SELECT
    'personal', admin.`id`, NULL, 'material', material.`id`, '小学英语教材 · Guoguo 对话',
    material.`sort_order`, 'active', admin.`id`
FROM `learning_material` AS material
JOIN `user` AS admin
  ON admin.`username` = 'admin'
 AND admin.`role` = 'admin'
LEFT JOIN `private_zone_item` AS existing
  ON existing.`scope_type` = 'personal'
 AND existing.`owner_user_id` = admin.`id`
 AND existing.`resource_type` = 'material'
 AND existing.`resource_id` = material.`id`
WHERE material.`is_published` = 1
  AND material.`material_code` = 'english-textbook-current'
  AND existing.`id` IS NULL;

INSERT INTO `private_zone_item`
    (`scope_type`, `owner_user_id`, `family_group_id`, `resource_type`, `resource_id`,
     `label`, `sort_order`, `status`, `added_by_user_id`)
SELECT
    'personal', admin.`id`, NULL, 'material', material.`id`,
    CONCAT('小学课本单词 · ', SUBSTRING_INDEX(material.`title`, ' · ', -1)),
    material.`sort_order`, 'active', admin.`id`
FROM `learning_material` AS material
JOIN `user` AS admin
  ON admin.`username` = 'admin'
 AND admin.`role` = 'admin'
LEFT JOIN `private_zone_item` AS existing
  ON existing.`scope_type` = 'personal'
 AND existing.`owner_user_id` = admin.`id`
 AND existing.`resource_type` = 'material'
 AND existing.`resource_id` = material.`id`
WHERE material.`is_published` = 1
  AND material.`material_code` LIKE 'kids-cards-%'
  AND existing.`id` IS NULL;

COMMIT;
