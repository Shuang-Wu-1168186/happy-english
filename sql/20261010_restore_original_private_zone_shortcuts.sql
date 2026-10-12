-- The private-zone examples must open the established learner study screens.
-- Scope this repair to the bundled admin examples so user-created shortcuts
-- are never rewritten.

UPDATE `private_zone_shortcut` AS shortcut
JOIN `user` AS account
  ON account.`id` = shortcut.`user_id`
SET shortcut.`target_url` = '/learn/kids-cards',
    shortcut.`description` = '打开原有的小学英语词卡，从 northeast 开始学习。'
WHERE account.`username` = 'admin'
  AND account.`role` = 'admin'
  AND shortcut.`title` = '小学英语单词';

UPDATE `private_zone_shortcut` AS shortcut
JOIN `user` AS account
  ON account.`id` = shortcut.`user_id`
SET shortcut.`target_url` = '/learn/math-cards',
    shortcut.`description` = '打开原有的数学知识卡和练习。'
WHERE account.`username` = 'admin'
  AND account.`role` = 'admin'
  AND shortcut.`title` = '数学练习';
