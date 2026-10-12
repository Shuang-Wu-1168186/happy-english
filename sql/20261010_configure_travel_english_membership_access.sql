-- Travel English is a membership collection. Learners can preview only the
-- first two lessons in the whole topic sequence through
-- MembershipService.FREE_PREVIEW_LESSON_COUNT; the all-courses membership
-- unlocks every travel material in full.

START TRANSACTION;

UPDATE `learning_course`
SET `access_policy` = 'benefit'
WHERE `course_code` IN (
    'travel-english-before-the-trip',
    'travel-english-at-the-airport',
    'travel-english-on-the-plane',
    'travel-english-immigration-and-customs',
    'travel-english-getting-around',
    'travel-english-at-the-hotel',
    'travel-english-eating-out',
    'travel-english-shopping',
    'travel-english-sightseeing',
    'travel-english-problems-and-real-life-travel'
);

INSERT INTO `membership_benefit_course`
    (`benefit_id`, `course_id`, `access_action`, `is_enabled`, `sort_order`)
SELECT benefit.`id`, course.`id`, 'study', 1, course.`sort_order`
FROM `membership_benefit` benefit
JOIN `learning_course` course
  ON course.`course_code` IN (
      'travel-english-before-the-trip',
      'travel-english-at-the-airport',
      'travel-english-on-the-plane',
      'travel-english-immigration-and-customs',
      'travel-english-getting-around',
      'travel-english-at-the-hotel',
      'travel-english-eating-out',
      'travel-english-shopping',
      'travel-english-sightseeing',
      'travel-english-problems-and-real-life-travel'
  )
WHERE benefit.`benefit_code` = 'all-courses-access'
ON DUPLICATE KEY UPDATE
    `access_action` = VALUES(`access_action`),
    `is_enabled` = VALUES(`is_enabled`),
    `sort_order` = VALUES(`sort_order`),
    `updated_at` = CURRENT_TIMESTAMP;

COMMIT;
