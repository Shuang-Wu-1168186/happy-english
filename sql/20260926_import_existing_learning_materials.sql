-- Import the existing platform content into the material → lesson → course catalogue.
--
-- Prerequisites:
--   1. 20260925_add_learning_catalog.sql
--   2. 20260926_add_membership_material_management.sql
--   3. 20260927_add_learning_course_material_mapping.sql
--   4. The existing content tables and their data have already been imported.
--
-- The script is intentionally idempotent.  It creates missing catalogue rows
-- without overwriting titles, descriptions, ordering, or publication choices
-- subsequently adjusted in the admin UI.
--
-- Private learning notes are excluded.  A note can only enter the catalogue
-- once english_note.share_status = 1, because learner-facing material lessons
-- may never expose a private note or its private cards.

START TRANSACTION;

-- Additional content topics, plus a compatibility seed for the permanent
-- personal-notes topic on databases created before that topic was added.
INSERT INTO `learning_topic`
    (`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'children-cards', '儿童英语卡片', 'Children English Cards',
       '按课本单元整理单词、短语和发音卡片。', 40, 1
FROM `learning_module`
WHERE `module_code` = 'foundation'
ON DUPLICATE KEY UPDATE `topic_code` = VALUES(`topic_code`);

INSERT INTO `learning_topic`
    (`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'math-cards', '数学卡片', 'Math Cards',
       '用英语学习数学概念、技巧与例题。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'math-zone'
ON DUPLICATE KEY UPDATE `topic_code` = VALUES(`topic_code`);

INSERT INTO `learning_topic`
    (`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'advanced-vocabulary', '进阶词汇', 'Advanced Vocabulary',
       '通用表达、标点和进阶词汇学习。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'advanced-english'
ON DUPLICATE KEY UPDATE `topic_code` = VALUES(`topic_code`);

INSERT INTO `learning_topic`
    (`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'my-english-notes', '我的英语笔记', 'My English Notes',
       '个人学习笔记与卡片的专属入口；私有内容仅对笔记作者可见。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'learning-notes'
ON DUPLICATE KEY UPDATE `topic_code` = VALUES(`topic_code`);

INSERT INTO `learning_topic`
    (`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'shared-notes', '公开学习笔记', 'Shared Learning Notes',
       '由作者公开分享、可作为平台内容学习的笔记。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'learning-notes'
  AND EXISTS (SELECT 1 FROM `english_note` WHERE `share_status` = 1)
ON DUPLICATE KEY UPDATE `topic_code` = VALUES(`topic_code`);

-- One current English textbook; its existing lesson rows become material lessons.
INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`, 'english-textbook-current', '现有英文课本', 'Current English Textbook',
       '按单元和课文学习现有英文课本内容。', 'textbook',
       'Happy English', '现有内容导入', COUNT(*) * 15, 10, 1
FROM `english_textbook_lesson` lesson
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'english-textbook'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'foundation'
  AND lesson.`is_published` = 1
GROUP BY topic.`id`
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

-- The existing phonics sequence is one continuous teaching material.
INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`, 'natural-phonics-current', '自然拼读课程', 'Natural Phonics',
       '从音素、拼读规律到复习测验的现有自然拼读课程。', 'phonics',
       'Happy English', '现有内容导入', COUNT(*) * 15, 10, 1
FROM `phonics_lesson` lesson
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'natural-phonics'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'foundation'
  AND lesson.`is_active` = 1
GROUP BY topic.`id`
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

-- Children cards are grouped by their textbook unit, instead of making every
-- card a separate material.
INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`,
       CONCAT('kids-cards-', LOWER(REPLACE(cards.`unit_title`, ' ', '-'))),
       CONCAT('儿童英语卡片 · ', cards.`unit_title`),
       CONCAT('Children English Cards · ', cards.`unit_title`),
       '按课本单元整理的单词、短语、发音与例句卡片。',
       'card_set', 'Happy English', '现有内容导入',
       cards.`card_count` * 3, cards.`first_order`, 1
FROM (
    SELECT SUBSTRING_INDEX(`category`, ' · ', 1) AS `unit_title`,
           COUNT(*) AS `card_count`,
           MIN(`priority_order`) AS `first_order`
    FROM `kids_english_card`
    WHERE `is_active` = 1
    GROUP BY SUBSTRING_INDEX(`category`, ' · ', 1)
) cards
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'children-cards'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'foundation'
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

-- The existing maths cards form one mathematics study material.
INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`, 'math-card-collection', '数学专区卡片', 'Math Zone Cards',
       '覆盖分数、组合图形、圆与扇形等知识点的数学英语学习卡片。', 'card_set',
       'Happy English', '现有内容导入', COUNT(*) * 10, 10, 1
FROM `math_card` card
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'math-cards'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'math-zone'
  AND card.`is_published` = 1
GROUP BY topic.`id`
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

-- Daily sentences remain one daily-speaking material; tags stay on the source
-- records and can be used for future filtering without fragmenting the course.
INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`, 'daily-speaking-sentences', '每日实用口语', 'Daily Practical Speaking',
       '现有日常英语句子、短语和表达练习。', 'dialogue',
       'Happy English', '现有内容导入', COUNT(*) * 3, 10, 1
FROM `everyday_sentence` sentence
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'daily-speaking-practice'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'daily-speaking'
GROUP BY topic.`id`
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

-- Each dialogue chapter becomes a material, and every dialogue lesson code
-- becomes one material lesson.  Opening it loads all of its dialogue items.
INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`,
       CONCAT('daily-dialogue-chapter-', LPAD(chapter.`first_lesson_order`, 3, '0')),
       CONCAT('日常口语对话 · ', chapter.`chapter_title`),
       chapter.`chapter_title`,
       '围绕真实生活场景练习完整对话、词汇和表达。',
       'dialogue', 'Happy English', '现有内容导入',
       chapter.`lesson_count` * 20, chapter.`first_lesson_order`, 1
FROM (
    SELECT COALESCE(NULLIF(`chapter_title`, ''), '未分类对话') AS `chapter_title`,
           MIN(`lesson_order`) AS `first_lesson_order`,
           COUNT(DISTINCT `lesson_code`) AS `lesson_count`
    FROM `daily_spoken_dialogue_item`
    WHERE `is_published` = 1
    GROUP BY COALESCE(NULLIF(`chapter_title`, ''), '未分类对话')
) chapter
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'daily-speaking-dialogues'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'daily-speaking'
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

-- An interview category with published questions becomes a standalone material.
INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`, CONCAT('interview-category-', category.`id`),
       CONCAT('面试英语 · ', category.`category_name`), category.`category_name`,
       COALESCE(NULLIF(category.`description`, ''), '按主题练习面试问题、回答与表达。'),
       'interview', 'Happy English', '现有内容导入',
       category.`question_count` * 10, category.`sort_order`, 1
FROM (
    SELECT interview_category.`id`, interview_category.`category_name`,
           interview_category.`description`, interview_category.`sort_order`,
           COUNT(interview_question.`id`) AS `question_count`
    FROM `interview_category`
    JOIN `interview_question`
      ON interview_question.`category_id` = interview_category.`id`
     AND interview_question.`status` = 1
    WHERE interview_category.`status` = 1
    GROUP BY interview_category.`id`, interview_category.`category_name`,
             interview_category.`description`, interview_category.`sort_order`
) category
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'interview-english'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'workplace'
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

-- Vocabulary is split by learner intent: general vocabulary in Advanced
-- English, and technical/professional vocabulary in Workplace English.
INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`, 'advanced-general-vocabulary', '通用英语词汇', 'General English Vocabulary',
       '通用词汇、标点与课程表达。', 'card_set',
       'Happy English', '现有内容导入', COUNT(*) * 3, 10, 1
FROM `vocabulary_library` vocabulary
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'advanced-vocabulary'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'advanced-english'
  AND vocabulary.`category` IN ('general', 'punctuation', 'course')
GROUP BY topic.`id`
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`, 'workplace-technical-vocabulary', '职场与技术词汇', 'Workplace and Technical Vocabulary',
       '编程、云服务、数据、架构、运维和专业沟通常用词汇。', 'card_set',
       'Happy English', '现有内容导入', COUNT(*) * 3, 10, 1
FROM `vocabulary_library` vocabulary
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'professional-vocabulary'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'workplace'
  AND vocabulary.`category` NOT IN ('general', 'punctuation', 'course')
GROUP BY topic.`id`
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

-- A shared note is an independent material.  This currently imports no rows
-- when all notes are private, but safely imports a note after it is shared.
INSERT INTO `learning_material`
    (`topic_id`, `material_code`, `title`, `summary`, `material_type`,
     `publisher`, `version_name`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT topic.`id`, CONCAT('shared-note-', note.`id`), note.`title`, note.`summary`,
       'note_collection', 'Happy English', '公开学习笔记', 10,
       note.`priority_order`, 1
FROM `english_note` note
JOIN `learning_topic` topic
  ON topic.`topic_code` = 'shared-notes'
JOIN `learning_module` module
  ON module.`id` = topic.`module_id`
WHERE module.`module_code` = 'learning-notes'
  AND note.`share_status` = 1
ON DUPLICATE KEY UPDATE `material_code` = VALUES(`material_code`);

-- Textbook lessons.
INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `title_en`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('textbook-lesson-', lesson.`id`),
       COALESCE(NULLIF(lesson.`title_cn`, ''), NULLIF(lesson.`title`, ''),
                CONCAT(lesson.`unit_name`, ' · ', lesson.`lesson_name`)),
       NULLIF(lesson.`title`, ''), lesson.`summary`,
       'textbook', lesson.`id`, 15,
       lesson.`unit_order` * 100 + lesson.`lesson_order`, 1
FROM `english_textbook_lesson` lesson
JOIN `learning_material` material
  ON material.`material_code` = 'english-textbook-current'
WHERE lesson.`is_published` = 1
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

-- Phonics lessons.
INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `title_en`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('phonics-', lesson.`id`), lesson.`title`, lesson.`subtitle`,
       lesson.`learning_tip`, 'phonics', lesson.`id`, 15, lesson.`priority_order`, 1
FROM `phonics_lesson` lesson
JOIN `learning_material` material
  ON material.`material_code` = 'natural-phonics-current'
WHERE lesson.`is_active` = 1
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

-- Children cards, one card per material lesson under its unit material.
INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `title_en`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('card-', card.`id`),
       CONCAT(card.`word`, ' · ', card.`translation`), card.`word`, card.`tip`,
       'kids-cards', card.`id`, 3, card.`priority_order`, 1
FROM `kids_english_card` card
JOIN `learning_material` material
  ON material.`material_code` = CONCAT(
      'kids-cards-', LOWER(REPLACE(SUBSTRING_INDEX(card.`category`, ' · ', 1), ' ', '-'))
  )
WHERE card.`is_active` = 1
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

-- Maths cards.
INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('math-card-', card.`id`), card.`title`, card.`summary`,
       'math-cards', card.`id`, 10, card.`sort_order` * 1000 + card.`id`, 1
FROM `math_card` card
JOIN `learning_material` material
  ON material.`material_code` = 'math-card-collection'
WHERE card.`is_published` = 1
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

-- Daily speaking sentences.
INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `title_en`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('sentence-', sentence.`id`), LEFT(sentence.`en`, 255),
       LEFT(sentence.`en`, 255), sentence.`cn`,
       'sentences', sentence.`id`, 3, sentence.`id`, 1
FROM `everyday_sentence` sentence
JOIN `learning_material` material
  ON material.`material_code` = 'daily-speaking-sentences'
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

-- Daily dialogue lessons.  A source reference points to the first item of a
-- lesson code; LearningCatalogService then loads the complete dialogue group.
INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `title_en`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('dialogue-', dialogue.`lesson_code`),
       COALESCE(NULLIF(dialogue.`lesson_title`, ''), CONCAT('对话 · ', dialogue.`lesson_code`)),
       NULLIF(dialogue.`lesson_title`, ''), dialogue.`chapter_title`,
       'dialogues', dialogue.`first_item_id`, 20, dialogue.`lesson_order`, 1
FROM (
    SELECT `lesson_code`,
           COALESCE(NULLIF(`chapter_title`, ''), '未分类对话') AS `chapter_title`,
           MAX(`lesson_title`) AS `lesson_title`, MIN(`lesson_order`) AS `lesson_order`,
           MIN(`id`) AS `first_item_id`
    FROM `daily_spoken_dialogue_item`
    WHERE `is_published` = 1
    GROUP BY `lesson_code`, COALESCE(NULLIF(`chapter_title`, ''), '未分类对话')
) dialogue
JOIN (
    SELECT COALESCE(NULLIF(`chapter_title`, ''), '未分类对话') AS `chapter_title`,
           MIN(`lesson_order`) AS `first_lesson_order`
    FROM `daily_spoken_dialogue_item`
    WHERE `is_published` = 1
    GROUP BY COALESCE(NULLIF(`chapter_title`, ''), '未分类对话')
) chapter
  ON chapter.`chapter_title` = dialogue.`chapter_title`
JOIN `learning_material` material
  ON material.`material_code` = CONCAT(
      'daily-dialogue-chapter-', LPAD(chapter.`first_lesson_order`, 3, '0')
  )
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

-- Interview questions.
INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `title_en`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('interview-question-', question.`id`),
       COALESCE(NULLIF(LEFT(question.`question_cn`, 255), ''),
                NULLIF(LEFT(question.`question`, 255), ''),
                CONCAT('面试题 ', question.`id`)),
       NULLIF(LEFT(question.`question`, 255), ''), question.`answer_tip`,
       'interviews', question.`id`, 10,
       question.`priority_order` * 1000 + question.`id`, 1
FROM `interview_question` question
JOIN `interview_category` category
  ON category.`id` = question.`category_id`
JOIN `learning_material` material
  ON material.`material_code` = CONCAT('interview-category-', category.`id`)
WHERE category.`status` = 1
  AND question.`status` = 1
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

-- Vocabulary cards: general and professional/technical collections.
INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `title_en`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('vocabulary-', vocabulary.`id`), vocabulary.`term`, vocabulary.`term`,
       vocabulary.`chinese_meaning`, 'vocabulary', vocabulary.`id`, 3,
       vocabulary.`sort_order` * 1000 + vocabulary.`id`, 1
FROM `vocabulary_library` vocabulary
JOIN `learning_material` material
  ON material.`material_code` = 'advanced-general-vocabulary'
WHERE vocabulary.`category` IN ('general', 'punctuation', 'course')
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `title_en`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('vocabulary-', vocabulary.`id`), vocabulary.`term`, vocabulary.`term`,
       vocabulary.`chinese_meaning`, 'vocabulary', vocabulary.`id`, 3,
       vocabulary.`sort_order` * 1000 + vocabulary.`id`, 1
FROM `vocabulary_library` vocabulary
JOIN `learning_material` material
  ON material.`material_code` = 'workplace-technical-vocabulary'
WHERE vocabulary.`category` NOT IN ('general', 'punctuation', 'course')
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

-- Public notes only.
INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `summary`,
     `source_resource`, `source_reference_id`, `estimated_minutes`, `sort_order`, `is_published`)
SELECT material.`id`, CONCAT('shared-note-', note.`id`), note.`title`, note.`summary`,
       'notes', note.`id`, 10, note.`priority_order`, 1
FROM `english_note` note
JOIN `learning_material` material
  ON material.`material_code` = CONCAT('shared-note-', note.`id`)
WHERE note.`share_status` = 1
ON DUPLICATE KEY UPDATE `lesson_code` = VALUES(`lesson_code`);

-- Every imported material is exposed through exactly one free course.  Course
-- codes are deliberately derived from material codes so future imports remain
-- stable and do not create duplicates.
INSERT INTO `learning_course`
    (`topic_id`, `material_id`, `course_code`, `title`, `title_en`, `summary`,
     `course_type`, `estimated_minutes`, `difficulty_code`, `sort_order`,
     `is_published`, `access_policy`)
SELECT material.`topic_id`, material.`id`, CONCAT(material.`material_code`, '-course'),
       material.`title`, material.`title_en`, material.`summary`, material.`material_type`,
       material.`estimated_minutes`, material.`difficulty_code`, material.`sort_order`,
       material.`is_published`, 'benefit'
FROM `learning_material` material
WHERE material.`material_code` IN (
    'english-textbook-current',
    'natural-phonics-current',
    'math-card-collection',
    'daily-speaking-sentences',
    'advanced-general-vocabulary',
    'workplace-technical-vocabulary'
)
   OR material.`material_code` LIKE 'kids-cards-%'
   OR material.`material_code` LIKE 'daily-dialogue-chapter-%'
   OR material.`material_code` LIKE 'interview-category-%'
   OR material.`material_code` LIKE 'shared-note-%'
ON DUPLICATE KEY UPDATE `course_code` = VALUES(`course_code`);

-- The course's material_id remains a compatibility mirror.  The ordered
-- mapping is the canonical course-to-material relationship.
INSERT INTO `learning_course_material`
    (`course_id`, `material_id`, `sort_order`)
SELECT course.`id`, course.`material_id`, 10
FROM `learning_course` course
WHERE course.`material_id` IS NOT NULL
ON DUPLICATE KEY UPDATE `course_id` = VALUES(`course_id`);

-- All existing courses are member-only.  A single reusable entitlement keeps
-- the initial commercial configuration simple while preserving the option to
-- create narrower course benefits later.
UPDATE `learning_course`
SET `access_policy` = 'benefit'
WHERE `access_policy` <> 'benefit';

INSERT INTO `membership_benefit`
    (`benefit_code`, `name`, `name_en`, `description`, `benefit_type`, `value_type`,
     `scope_json`, `default_value_json`, `icon`, `sort_order`, `status`)
VALUES
    ('all-courses-access', '全课程学习权益', 'All Courses Access',
     '解锁当前平台内的全部学习课程。', 'content_access', 'boolean',
     '{"scope":"all_courses","access_action":"study"}', 'true', '📚', 10, 'active')
ON DUPLICATE KEY UPDATE `benefit_code` = VALUES(`benefit_code`);

-- This active, manually issued plan is deliberately not the default plan:
-- administrators decide which users receive all-course access.
INSERT INTO `membership_plan`
    (`plan_code`, `name`, `name_en`, `description`, `tier_rank`, `billing_cycle`,
     `price`, `currency`, `icon`, `sort_order`, `status`, `is_default`)
VALUES
    ('all-courses-member', '全课程会员', 'All Courses Member',
     '包含全课程学习权益；初始配置为后台发放，可在后台修改价格和周期。',
     10, 'manual', 0.00, 'CNY', '👑', 10, 'active', 0)
ON DUPLICATE KEY UPDATE `plan_code` = VALUES(`plan_code`);

INSERT INTO `membership_plan_benefit`
    (`membership_plan_id`, `benefit_id`, `grant_value_json`, `is_enabled`, `sort_order`)
SELECT plan.`id`, benefit.`id`, NULL, 1, 10
FROM `membership_plan` plan
JOIN `membership_benefit` benefit
  ON benefit.`benefit_code` = 'all-courses-access'
WHERE plan.`plan_code` = 'all-courses-member'
ON DUPLICATE KEY UPDATE `membership_plan_id` = VALUES(`membership_plan_id`);

INSERT INTO `membership_benefit_course`
    (`benefit_id`, `course_id`, `access_action`, `is_enabled`, `sort_order`)
SELECT benefit.`id`, course.`id`, 'study', 1, course.`sort_order`
FROM `membership_benefit` benefit
CROSS JOIN `learning_course` course
WHERE benefit.`benefit_code` = 'all-courses-access'
ON DUPLICATE KEY UPDATE `benefit_id` = VALUES(`benefit_id`);

COMMIT;

-- Post-import verification.  The material and course counts should match,
-- and the lesson count represents navigable units rather than raw dialogue
-- line items.
SELECT 'materials' AS `entity`, COUNT(*) AS `count`
FROM `learning_material`
WHERE `material_code` IN (
    'english-textbook-current',
    'natural-phonics-current',
    'math-card-collection',
    'daily-speaking-sentences',
    'advanced-general-vocabulary',
    'workplace-technical-vocabulary'
)
   OR `material_code` LIKE 'kids-cards-%'
   OR `material_code` LIKE 'daily-dialogue-chapter-%'
   OR `material_code` LIKE 'interview-category-%'
   OR `material_code` LIKE 'shared-note-%'
UNION ALL
SELECT 'courses', COUNT(*)
FROM `learning_course` course
JOIN `learning_material` material ON material.`id` = course.`material_id`
WHERE material.`material_code` IN (
    'english-textbook-current',
    'natural-phonics-current',
    'math-card-collection',
    'daily-speaking-sentences',
    'advanced-general-vocabulary',
    'workplace-technical-vocabulary'
)
   OR material.`material_code` LIKE 'kids-cards-%'
   OR material.`material_code` LIKE 'daily-dialogue-chapter-%'
   OR material.`material_code` LIKE 'interview-category-%'
   OR material.`material_code` LIKE 'shared-note-%'
UNION ALL
SELECT 'material_lessons', COUNT(*)
FROM `learning_material_lesson` lesson
JOIN `learning_material` material ON material.`id` = lesson.`material_id`
WHERE material.`material_code` IN (
    'english-textbook-current',
    'natural-phonics-current',
    'math-card-collection',
    'daily-speaking-sentences',
    'advanced-general-vocabulary',
    'workplace-technical-vocabulary'
)
   OR material.`material_code` LIKE 'kids-cards-%'
   OR material.`material_code` LIKE 'daily-dialogue-chapter-%'
   OR material.`material_code` LIKE 'interview-category-%'
   OR material.`material_code` LIKE 'shared-note-%'
UNION ALL
SELECT 'member_only_courses', COUNT(*)
FROM `learning_course`
WHERE `access_policy` = 'benefit'
UNION ALL
SELECT 'all_course_benefit_mappings', COUNT(*)
FROM `membership_benefit_course` benefit_course
JOIN `membership_benefit` benefit ON benefit.`id` = benefit_course.`benefit_id`
WHERE benefit.`benefit_code` = 'all-courses-access';
