-- Move the Wordly Wise 3000 series into its dedicated topic and sell it as
-- one membership collection. Non-members retain the normal topic-wide
-- two-lesson preview; the all-courses membership unlocks every book.

START TRANSACTION;

INSERT INTO `learning_topic`
    (`module_id`, `topic_code`, `title`, `title_en`, `description`, `cover_url`, `sort_order`, `is_published`)
SELECT `id`, 'w', 'Wordly wise 3000系列', 'wordly-wise-3000',
       'Wordly Wise 3000 系列词汇课程。', NULL, 0, 1
FROM `learning_module`
WHERE `module_code` = 'intermediate-english'
ON DUPLICATE KEY UPDATE
    `is_published` = VALUES(`is_published`),
    `updated_at` = CURRENT_TIMESTAMP;

UPDATE `learning_course`
SET `access_policy` = 'benefit',
    `is_published` = 1,
    `updated_at` = CURRENT_TIMESTAMP
WHERE `course_code` IN (
    'wordly-wise-1-preview', 'wordly-wise-2-preview',
    'wordly-wise-3-preview', 'wordly-wise-4-preview',
    'wordly-wise-5-preview', 'wordly-wise-6-preview',
    'wordly-wise-7-preview', 'wordly-wise-8-preview',
    'wordly-wise-9-preview', 'wordly-wise-10-preview',
    'wordly-wise-11-preview', 'wordly-wise-12-preview'
);

-- The series is shown only in its own intermediate topic, rather than
-- duplicated in any elementary-English catalogue topic.
DELETE `mapping`
FROM `learning_topic_course` AS `mapping`
JOIN `learning_course` AS `course`
  ON `course`.`id` = `mapping`.`course_id`
JOIN `learning_topic` AS `topic`
  ON `topic`.`id` = `mapping`.`topic_id`
JOIN `learning_module` AS `module`
  ON `module`.`id` = `topic`.`module_id`
WHERE `module`.`module_code` = 'elementary-english'
  AND `course`.`course_code` IN (
      'wordly-wise-1-preview', 'wordly-wise-2-preview',
      'wordly-wise-3-preview', 'wordly-wise-4-preview',
      'wordly-wise-5-preview', 'wordly-wise-6-preview',
      'wordly-wise-7-preview', 'wordly-wise-8-preview',
      'wordly-wise-9-preview', 'wordly-wise-10-preview',
      'wordly-wise-11-preview', 'wordly-wise-12-preview'
  );

INSERT INTO `learning_topic_course`
    (`topic_id`, `course_id`, `sort_order`)
SELECT `topic`.`id`, `course`.`id`, `course`.`sort_order`
FROM `learning_topic` AS `topic`
JOIN `learning_module` AS `module`
  ON `module`.`id` = `topic`.`module_id`
JOIN `learning_course` AS `course`
WHERE `module`.`module_code` = 'intermediate-english'
  AND `topic`.`topic_code` = 'w'
  AND `course`.`course_code` IN (
      'wordly-wise-1-preview', 'wordly-wise-2-preview',
      'wordly-wise-3-preview', 'wordly-wise-4-preview',
      'wordly-wise-5-preview', 'wordly-wise-6-preview',
      'wordly-wise-7-preview', 'wordly-wise-8-preview',
      'wordly-wise-9-preview', 'wordly-wise-10-preview',
      'wordly-wise-11-preview', 'wordly-wise-12-preview'
  )
ON DUPLICATE KEY UPDATE
    `sort_order` = VALUES(`sort_order`),
    `updated_at` = CURRENT_TIMESTAMP;

INSERT INTO `membership_benefit_course`
    (`benefit_id`, `course_id`, `access_action`, `is_enabled`, `sort_order`)
SELECT `benefit`.`id`, `course`.`id`, 'study', 1, `course`.`sort_order`
FROM `membership_benefit` AS `benefit`
JOIN `learning_course` AS `course`
WHERE `benefit`.`benefit_code` = 'all-courses-access'
  AND `course`.`course_code` IN (
      'wordly-wise-1-preview', 'wordly-wise-2-preview',
      'wordly-wise-3-preview', 'wordly-wise-4-preview',
      'wordly-wise-5-preview', 'wordly-wise-6-preview',
      'wordly-wise-7-preview', 'wordly-wise-8-preview',
      'wordly-wise-9-preview', 'wordly-wise-10-preview',
      'wordly-wise-11-preview', 'wordly-wise-12-preview'
  )
ON DUPLICATE KEY UPDATE
    `access_action` = VALUES(`access_action`),
    `is_enabled` = VALUES(`is_enabled`),
    `sort_order` = VALUES(`sort_order`),
    `updated_at` = CURRENT_TIMESTAMP;

COMMIT;
