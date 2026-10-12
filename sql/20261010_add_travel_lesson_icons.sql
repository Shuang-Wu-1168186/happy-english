-- Attach the generated local icon for every published Travel English lesson.
-- The matching PNG files live in data/static/images/learning_material/icon/.

START TRANSACTION;

UPDATE `learning_material_lesson` AS lesson
JOIN `learning_material` AS material
  ON material.`id` = lesson.`material_id`
JOIN `learning_course_material` AS course_material
  ON course_material.`material_id` = material.`id`
JOIN `learning_topic_course` AS topic_course
  ON topic_course.`course_id` = course_material.`course_id`
JOIN `learning_topic` AS topic
  ON topic.`id` = topic_course.`topic_id`
SET lesson.`illustration_url` = CONCAT(
    '/static/images/learning_material/icon/travel-english-',
    material.`material_code`,
    '--',
    lesson.`lesson_code`,
    '.png'
),
    lesson.`updated_at` = CURRENT_TIMESTAMP
WHERE topic.`topic_code` = 'travel-english'
  AND material.`material_code` IN (
      'before-the-trip',
      'at-the-airport',
      'on-the-plane',
      'immigration-and-customs',
      'getting-around',
      'at-the-hotel',
      'eating-out',
      'shopping',
      'sightseeing',
      'problems-and-real-life-travel'
  )
  AND lesson.`is_published` = 1;

COMMIT;
