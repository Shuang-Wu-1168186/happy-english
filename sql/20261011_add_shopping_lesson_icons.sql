-- Attach the generated local icon for every published Practical Shopping
-- English lesson. The matching PNG files live in
-- data/static/images/learning_material/icon/.
--
-- Shopping English remains a free collection; this migration changes only
-- its lesson illustration URLs.

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
    '/static/images/learning_material/icon/',
    material.`material_code`,
    '--',
    lesson.`lesson_code`,
    '.png'
),
    lesson.`updated_at` = CURRENT_TIMESTAMP
WHERE topic.`topic_code` = 'shopping-english'
  AND material.`material_code` IN (
      'shopping-english-getting-started',
      'shopping-english-finding-the-right-product',
      'shopping-english-asking-about-products',
      'shopping-english-clothes-and-shoes',
      'shopping-english-supermarket-english',
      'shopping-english-prices-discounts-and-promotions',
      'shopping-english-checkout-and-payment',
      'shopping-english-returns-exchanges-and-refunds',
      'shopping-english-online-shopping-and-delivery',
      'shopping-english-real-life-shopping-challenges'
  )
  AND lesson.`is_published` = 1;

COMMIT;
