-- Keep the idiomatic-English series in the elementary learner directory.
-- The original courseware seed created this topic for elementary English, but
-- a later module restructure left the topic attached to advanced English.

START TRANSACTION;

SET @actor_id = (
    SELECT `id`
    FROM `user`
    WHERE `role` = 'admin'
    ORDER BY `id`
    LIMIT 1
);
SET @elementary_module_id = (
    SELECT `id`
    FROM `learning_module`
    WHERE `module_code` = 'elementary-english'
    LIMIT 1
);

UPDATE `learning_topic`
SET `module_id` = @elementary_module_id,
    `title` = '地道英语系列',
    `title_en` = 'Idiomatic English',
    `description` = '按月份和主题积累地道表达，在短课时里练习理解与开口。',
    `sort_order` = 20,
    `is_published` = 1,
    `updated_by` = @actor_id
WHERE `topic_code` = 'phrase-courseware'
  AND @elementary_module_id IS NOT NULL;

COMMIT;
