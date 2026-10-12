-- Common shortcuts are curated platform configuration.  Preserve any old
-- learner-owned rows as legacy data, then promote only the bundled entries
-- that were previously seeded under the built-in administrator account.

ALTER TABLE `private_zone_shortcut`
    ADD COLUMN `scope_type` VARCHAR(20) NOT NULL DEFAULT 'legacy_personal' AFTER `user_id`,
    ADD KEY `idx_private_zone_shortcut_scope_status_order`
        (`scope_type`, `status`, `sort_order`);

UPDATE `private_zone_shortcut` AS shortcut
JOIN `user` AS account
  ON account.`id` = shortcut.`user_id`
SET shortcut.`scope_type` = 'platform'
WHERE account.`username` = 'admin'
  AND account.`role` = 'admin'
  AND shortcut.`title` IN (
      '我的 English Note',
      '英语教材课本',
      '小学英语教材 · Guoguo 对话',
      '小学英语单词',
      '数学练习'
  );
