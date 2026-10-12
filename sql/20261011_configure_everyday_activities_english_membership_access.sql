-- 日常生活英语 is sold as one topic-level member benefit.  The application
-- limits non-members to the first two material lessons in the complete topic
-- sequence, rather than granting two lessons in every textbook.

START TRANSACTION;

UPDATE `learning_course` AS course
JOIN `learning_topic_course` AS topic_course
  ON topic_course.`course_id` = course.`id`
JOIN `learning_topic` AS topic
  ON topic.`id` = topic_course.`topic_id`
SET course.`access_policy` = 'benefit',
    course.`updated_at` = CURRENT_TIMESTAMP
WHERE topic.`topic_code` = 'everyday-activities-english';

INSERT INTO `membership_benefit_course`
    (`benefit_id`, `course_id`, `access_action`, `is_enabled`, `sort_order`)
SELECT benefit.`id`, course.`id`, 'study', 1, topic_course.`sort_order`
FROM `membership_benefit` AS benefit
JOIN `learning_topic` AS topic
  ON topic.`topic_code` = 'everyday-activities-english'
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
