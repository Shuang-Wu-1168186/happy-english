-- Rebuild the learner-facing module directory as English proficiency levels.
--
-- Run after 20260926_import_existing_learning_materials.sql.  It preserves all
-- existing materials, lessons, courses and membership mappings.  Only the two
-- requested topics remain published in the learner directory for now:
--   入门英语 → 自然拼读专区
--   初级英语 → 日常口语专区
--
-- The migration is safe to run again after a successful run: the legacy
-- learning-notes module is used as the one-time migration marker.

START TRANSACTION;

SET @restructure_learning_modules := (
    SELECT COUNT(*)
    FROM `learning_module`
    WHERE `module_code` = 'learning-notes'
);

-- The old advanced-english code is reused by 进阶英语.  Move all legacy codes
-- out of the unique index first, then assign the six new level codes.
UPDATE `learning_module`
SET `module_code` = CASE `module_code`
    WHEN 'learning-notes' THEN '__legacy_learning_notes__'
    WHEN 'foundation' THEN '__legacy_foundation__'
    WHEN 'math-zone' THEN '__legacy_math_zone__'
    WHEN 'daily-speaking' THEN '__legacy_daily_speaking__'
    WHEN 'workplace' THEN '__legacy_workplace__'
    WHEN 'advanced-english' THEN '__legacy_advanced_english__'
END
WHERE @restructure_learning_modules = 1
  AND `module_code` IN (
      'learning-notes',
      'foundation',
      'math-zone',
      'daily-speaking',
      'workplace',
      'advanced-english'
  );

UPDATE `learning_module`
SET `module_code` = 'beginner-english',
    `name` = '入门英语',
    `name_en` = 'Beginner English',
    `description` = '从自然拼读开始，建立英文发音和阅读的第一步。',
    `icon` = '🔤',
    `color` = '#2DAA8A',
    `route_key` = 'phonics',
    `sort_order` = 10,
    `is_published` = 1
WHERE @restructure_learning_modules = 1
  AND `module_code` = '__legacy_learning_notes__';

UPDATE `learning_module`
SET `module_code` = 'elementary-english',
    `name` = '初级英语',
    `name_en` = 'Elementary English',
    `description` = '通过真实生活场景的日常口语对话，逐步建立表达能力。',
    `icon` = '💬',
    `color` = '#EC6A8C',
    `route_key` = 'dialogues',
    `sort_order` = 20,
    `is_published` = 1
WHERE @restructure_learning_modules = 1
  AND `module_code` = '__legacy_foundation__';

UPDATE `learning_module`
SET `module_code` = 'intermediate-english',
    `name` = '中级英语',
    `name_en` = 'Intermediate English',
    `description` = '课程正在筹备中。',
    `icon` = '📘',
    `color` = '#4F8DD8',
    `route_key` = 'intermediate',
    `sort_order` = 30,
    `is_published` = 1
WHERE @restructure_learning_modules = 1
  AND `module_code` = '__legacy_math_zone__';

UPDATE `learning_module`
SET `module_code` = 'advanced-english',
    `name` = '进阶英语',
    `name_en` = 'Advanced English',
    `description` = '课程正在筹备中。',
    `icon` = '🚀',
    `color` = '#8B5CF6',
    `route_key` = 'advanced',
    `sort_order` = 40,
    `is_published` = 1
WHERE @restructure_learning_modules = 1
  AND `module_code` = '__legacy_daily_speaking__';

UPDATE `learning_module`
SET `module_code` = 'higher-english',
    `name` = '高级英语',
    `name_en` = 'Higher English',
    `description` = '课程正在筹备中。',
    `icon` = '🏅',
    `color` = '#D69A2D',
    `route_key` = 'higher',
    `sort_order` = 50,
    `is_published` = 1
WHERE @restructure_learning_modules = 1
  AND `module_code` = '__legacy_workplace__';

UPDATE `learning_module`
SET `module_code` = 'private-zone',
    `name` = '私人专区',
    `name_en` = 'Private Zone',
    `description` = '集中查看个人学习笔记、重点卡片和复习内容。',
    `icon` = '🔒',
    `color` = '#64748B',
    `route_key` = 'private',
    `sort_order` = 60,
    `is_published` = 1
WHERE @restructure_learning_modules = 1
  AND `module_code` = '__legacy_advanced_english__';

-- Keep the existing data for later configuration, but remove every old topic
-- from learner-facing lists until it is deliberately assigned to a level.
UPDATE `learning_topic`
SET `is_published` = 0
WHERE @restructure_learning_modules = 1
  AND `topic_code` NOT IN (
      'natural-phonics',
      'daily-speaking-dialogues',
      'my-english-notes'
  );

UPDATE `learning_topic` AS `topic`
JOIN `learning_module` AS `module`
  ON `module`.`module_code` = 'beginner-english'
SET `topic`.`module_id` = `module`.`id`,
    `topic`.`title` = '自然拼读专区',
    `topic`.`title_en` = 'Natural Phonics',
    `topic`.`description` = '从字母、音素和拼读规律开始，练出见词能读的能力。',
    `topic`.`sort_order` = 10,
    `topic`.`is_published` = 1
WHERE @restructure_learning_modules = 1
  AND `topic`.`topic_code` = 'natural-phonics';

UPDATE `learning_topic` AS `topic`
JOIN `learning_module` AS `module`
  ON `module`.`module_code` = 'elementary-english'
SET `topic`.`module_id` = `module`.`id`,
    `topic`.`title` = '日常口语专区',
    `topic`.`title_en` = 'Daily Spoken English',
    `topic`.`description` = '围绕购物、出行和社交等真实场景，练习完整的日常英语对话。',
    `topic`.`sort_order` = 10,
    `topic`.`is_published` = 1
WHERE @restructure_learning_modules = 1
  AND `topic`.`topic_code` = 'daily-speaking-dialogues';

UPDATE `learning_topic` AS `topic`
JOIN `learning_module` AS `module`
  ON `module`.`module_code` = 'private-zone'
SET `topic`.`module_id` = `module`.`id`,
    `topic`.`title` = '我的英语笔记',
    `topic`.`title_en` = 'My English Notes',
    `topic`.`description` = '整理个人学习笔记、卡片和复习内容。',
    `topic`.`sort_order` = 10,
    `topic`.`is_published` = 1
WHERE @restructure_learning_modules = 1
  AND `topic`.`topic_code` = 'my-english-notes';

COMMIT;

-- Release verification: this should show six modules. 入门英语和初级英语各有
-- 平台课程；私人专区下保留“我的英语笔记”个人入口，不建立平台课程。
SELECT
    `module`.`sort_order`,
    `module`.`module_code`,
    `module`.`name`,
    `topic`.`topic_code`,
    `topic`.`title`,
    COUNT(`course`.`id`) AS `published_course_count`
FROM `learning_module` AS `module`
LEFT JOIN `learning_topic` AS `topic`
  ON `topic`.`module_id` = `module`.`id`
 AND `topic`.`is_published` = 1
LEFT JOIN `learning_course` AS `course`
  ON `course`.`topic_id` = `topic`.`id`
 AND `course`.`is_published` = 1
WHERE `module`.`module_code` IN (
    'beginner-english',
    'elementary-english',
    'intermediate-english',
    'advanced-english',
    'higher-english',
    'private-zone'
)
GROUP BY
    `module`.`id`,
    `module`.`sort_order`,
    `module`.`module_code`,
    `module`.`name`,
    `topic`.`id`,
    `topic`.`topic_code`,
    `topic`.`title`,
    `topic`.`sort_order`
ORDER BY `module`.`sort_order`, `topic`.`sort_order`, `topic`.`id`;
