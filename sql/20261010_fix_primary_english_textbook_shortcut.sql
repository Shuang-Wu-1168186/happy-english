-- Name the imported textbook for learners and repair the original admin
-- shortcut, which incorrectly sent learners to natural phonics.

UPDATE `learning_material`
SET
    `title` = '小学英语教材',
    `title_en` = 'Primary English Textbook',
    `summary` = '按单元和课文学习小学英语，包含 Guoguo、Lingling、Maomao 等角色对话。'
WHERE `material_code` = 'english-textbook-current';

-- Keep the existing personal favorite in "我的" consistent with the shortcut.
UPDATE `private_zone_item` AS item
JOIN `user` AS admin
  ON admin.`id` = item.`owner_user_id`
 AND admin.`username` = 'admin'
 AND admin.`role` = 'admin'
JOIN `learning_material` AS material
  ON material.`id` = item.`resource_id`
 AND material.`material_code` = 'english-textbook-current'
SET item.`label` = '小学英语教材 · Guoguo 对话'
WHERE item.`scope_type` = 'personal'
  AND item.`resource_type` = 'material'
  AND item.`label` = '小学英语课本';

-- If a previous deployment already created the canonical entry, discard only
-- the old seeded duplicate for the built-in admin account.
DELETE legacy
FROM `private_zone_shortcut` AS legacy
JOIN `user` AS admin
  ON admin.`id` = legacy.`user_id`
 AND admin.`username` = 'admin'
 AND admin.`role` = 'admin'
JOIN `private_zone_shortcut` AS canonical
  ON canonical.`user_id` = legacy.`user_id`
 AND canonical.`title` = '小学英语教材 · Guoguo 对话'
WHERE legacy.`title` = '英语教材课本';

-- Convert the old default entry to the real textbook route.
UPDATE `private_zone_shortcut` AS shortcut
JOIN `user` AS admin
  ON admin.`id` = shortcut.`user_id`
 AND admin.`username` = 'admin'
 AND admin.`role` = 'admin'
JOIN `learning_material` AS material
  ON material.`material_code` = 'english-textbook-current'
 AND material.`is_published` = 1
SET
    shortcut.`title` = '小学英语教材 · Guoguo 对话',
    shortcut.`target_url` = CONCAT('/learning-materials/', material.`id`),
    shortcut.`description` = '打开小学英语教材，学习 Guoguo、Lingling、Maomao 的情景对话。',
    shortcut.`icon` = '📖',
    shortcut.`sort_order` = 20,
    shortcut.`status` = 'active'
WHERE shortcut.`title` IN ('英语教材课本', '小学英语教材 · Guoguo 对话');

-- Add the shortcut when the database did not yet contain either version.
INSERT INTO `private_zone_shortcut`
    (`user_id`, `title`, `target_url`, `description`, `icon`, `sort_order`, `status`)
SELECT
    admin.`id`, '小学英语教材 · Guoguo 对话',
    CONCAT('/learning-materials/', material.`id`),
    '打开小学英语教材，学习 Guoguo、Lingling、Maomao 的情景对话。', '📖', 20, 'active'
FROM `user` AS admin
JOIN `learning_material` AS material
  ON material.`material_code` = 'english-textbook-current'
 AND material.`is_published` = 1
LEFT JOIN `private_zone_shortcut` AS existing
  ON existing.`user_id` = admin.`id`
 AND existing.`title` = '小学英语教材 · Guoguo 对话'
WHERE admin.`username` = 'admin'
  AND admin.`role` = 'admin'
  AND existing.`id` IS NULL;
