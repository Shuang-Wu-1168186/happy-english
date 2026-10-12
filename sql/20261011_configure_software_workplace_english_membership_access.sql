-- Software Developer Workplace English is sold as one membership collection.
-- Learners can preview only the first two lessons in the whole topic sequence
-- through MembershipService.FREE_PREVIEW_LESSON_COUNT; the all-courses
-- membership unlocks all software workplace materials in full.

START TRANSACTION;

UPDATE `learning_course` AS course
JOIN `learning_topic_course` AS topic_course
  ON topic_course.`course_id` = course.`id`
JOIN `learning_topic` AS topic
  ON topic.`id` = topic_course.`topic_id`
SET course.`access_policy` = 'benefit',
    course.`updated_at` = CURRENT_TIMESTAMP
WHERE topic.`topic_code` = 'software-developer-workplace-english';

INSERT INTO `membership_benefit_course`
    (`benefit_id`, `course_id`, `access_action`, `is_enabled`, `sort_order`)
SELECT benefit.`id`, course.`id`, 'study', 1, topic_course.`sort_order`
FROM `membership_benefit` AS benefit
JOIN `learning_topic` AS topic
  ON topic.`topic_code` = 'software-developer-workplace-english'
JOIN `learning_topic_course` AS topic_course
  ON topic_course.`topic_id` = topic.`id`
JOIN `learning_course` AS course
  ON course.`id` = topic_course.`course_id`
WHERE benefit.`benefit_code` = 'all-courses-access'
ON DUPLICATE KEY UPDATE
    `access_action` = VALUES(`access_action`),
    `is_enabled` = VALUES(`is_enabled`),
    `sort_order` = VALUES(`sort_order`),
    `updated_at` = CURRENT_TIMESTAMP;

COMMIT;
