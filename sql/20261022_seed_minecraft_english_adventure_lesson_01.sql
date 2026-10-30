-- First web lesson for Minecraft English Adventure.
-- Reuses the existing module -> topic -> course -> material -> lesson ->
-- structured section/item tables and is safe to run more than once.

START TRANSACTION;

INSERT INTO `learning_module`
    (`module_code`, `module_type`, `name`, `name_en`, `description`, `icon`, `color`, `route_key`, `sort_order`, `is_published`, `created_by`, `updated_by`)
VALUES
    ('game-english', 'resource', '游戏英语', 'Game English', '把英语练习放进游戏冒险，在任务和故事中自然开口。', '🎮', '#3B82F6', 'game-english', 75, 1, 1, 1)
ON DUPLICATE KEY UPDATE
    `module_type` = VALUES(`module_type`), `name` = VALUES(`name`), `name_en` = VALUES(`name_en`),
    `description` = VALUES(`description`), `icon` = VALUES(`icon`), `color` = VALUES(`color`),
    `route_key` = VALUES(`route_key`), `sort_order` = VALUES(`sort_order`), `is_published` = VALUES(`is_published`),
    `updated_by` = VALUES(`updated_by`);
SET @module_id = (SELECT `id` FROM `learning_module` WHERE `module_code` = 'game-english' LIMIT 1);

INSERT INTO `learning_topic`
    (`module_id`, `topic_code`, `title`, `title_en`, `description`, `cover_url`, `sort_order`, `is_published`, `created_by`, `updated_by`)
VALUES
    (@module_id, 'minecraft-english-adventure', 'Minecraft 英语冒险', 'Minecraft English Adventure', '从创建世界开始，跟着 Alex 和 Ben 用英语收集资源、建造基地并完成冒险。', '/static/minecraft/lesson-01-realistic.jpg', 10, 1, 1, 1)
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`), `title_en` = VALUES(`title_en`), `description` = VALUES(`description`),
    `cover_url` = VALUES(`cover_url`), `sort_order` = VALUES(`sort_order`), `is_published` = VALUES(`is_published`),
    `updated_by` = VALUES(`updated_by`);
SET @topic_id = (SELECT `id` FROM `learning_topic` WHERE `module_id` = @module_id AND `topic_code` = 'minecraft-english-adventure' LIMIT 1);

INSERT INTO `learning_material`
    (`template_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`, `publisher`, `version_name`, `cover_url`, `difficulty_code`, `estimated_minutes`, `sort_order`, `is_published`, `created_by`, `updated_by`)
VALUES
    ((SELECT `id` FROM `learning_template` WHERE `template_code` = 'dialogue' AND `template_version` = 1 AND `status` = 'active' LIMIT 1), 'minecraft-english-adventure', 'Minecraft 英语冒险', 'Minecraft English Adventure', '100 节连续英语冒险故事：Play Minecraft. Speak English. Learn Through Adventure.', 'dialogue', 'HappyLingo', 'Season 1', '/static/minecraft/lesson-01-realistic.jpg', 'a1', 1200, 10, 1, 1, 1)
ON DUPLICATE KEY UPDATE
    `template_id` = VALUES(`template_id`), `title` = VALUES(`title`), `title_en` = VALUES(`title_en`),
    `summary` = VALUES(`summary`), `material_type` = VALUES(`material_type`), `publisher` = VALUES(`publisher`),
    `version_name` = VALUES(`version_name`), `cover_url` = VALUES(`cover_url`), `difficulty_code` = VALUES(`difficulty_code`),
    `estimated_minutes` = VALUES(`estimated_minutes`), `sort_order` = VALUES(`sort_order`), `is_published` = VALUES(`is_published`),
    `updated_by` = VALUES(`updated_by`);
SET @material_id = (SELECT `id` FROM `learning_material` WHERE `material_code` = 'minecraft-english-adventure' LIMIT 1);

INSERT INTO `learning_course`
    (`material_id`, `course_code`, `title`, `title_en`, `summary`, `course_type`, `cover_url`, `estimated_minutes`, `difficulty_code`, `sort_order`, `is_published`, `access_policy`, `created_by`, `updated_by`)
VALUES
    (@material_id, 'minecraft-english-adventure', 'Minecraft 英语冒险', 'Minecraft English Adventure', '从创建世界到挑战末影龙，100 节连续故事课程。第一节：一起玩我的世界。', 'dialogue', '/static/minecraft/lesson-01-realistic.jpg', 1200, 'a1', 10, 1, 'free', 1, 1)
ON DUPLICATE KEY UPDATE
    `material_id` = VALUES(`material_id`), `title` = VALUES(`title`), `title_en` = VALUES(`title_en`), `summary` = VALUES(`summary`),
    `course_type` = VALUES(`course_type`), `cover_url` = VALUES(`cover_url`), `estimated_minutes` = VALUES(`estimated_minutes`),
    `difficulty_code` = VALUES(`difficulty_code`), `sort_order` = VALUES(`sort_order`), `is_published` = VALUES(`is_published`),
    `access_policy` = VALUES(`access_policy`), `updated_by` = VALUES(`updated_by`);
SET @course_id = (SELECT `id` FROM `learning_course` WHERE `course_code` = 'minecraft-english-adventure' LIMIT 1);

INSERT INTO `learning_topic_course` (`topic_id`, `course_id`, `sort_order`, `created_by`, `updated_by`)
VALUES (@topic_id, @course_id, 10, 1, 1)
ON DUPLICATE KEY UPDATE `sort_order` = VALUES(`sort_order`), `updated_by` = VALUES(`updated_by`);

INSERT INTO `learning_course_material` (`course_id`, `material_id`, `sort_order`, `created_by`, `updated_by`)
VALUES (@course_id, @material_id, 10, 1, 1)
ON DUPLICATE KEY UPDATE `sort_order` = VALUES(`sort_order`), `updated_by` = VALUES(`updated_by`);

INSERT INTO `learning_material_lesson`
    (`material_id`, `lesson_code`, `title`, `title_en`, `summary`, `illustration_url`, `content_json`, `lesson_format`, `lesson_schema_version`, `content_status`, `published_at`, `estimated_minutes`, `sort_order`, `is_published`, `created_by`, `updated_by`)
VALUES
    (@material_id, 'minecraft-english-adventure-lesson-01', '一起玩我的世界', 'Let’s Play Minecraft!', 'Alex 和 Ben 创建新世界，学习用英语观察环境、提出计划并开始收集资源。', '/static/minecraft/lesson-01-realistic.jpg', NULL, 'structured', 2, 'published', NOW(), 12, 10, 1, 1, 1)
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`), `title_en` = VALUES(`title_en`), `summary` = VALUES(`summary`), `illustration_url` = VALUES(`illustration_url`),
    `content_json` = NULL, `lesson_format` = 'structured', `lesson_schema_version` = 2, `content_status` = 'published', `published_at` = NOW(),
    `estimated_minutes` = VALUES(`estimated_minutes`), `sort_order` = VALUES(`sort_order`), `is_published` = 1, `updated_by` = VALUES(`updated_by`);
SET @lesson_id = (SELECT `id` FROM `learning_material_lesson` WHERE `material_id` = @material_id AND `lesson_code` = 'minecraft-english-adventure-lesson-01' LIMIT 1);

INSERT INTO `learning_lesson_section` (`lesson_id`, `section_code`, `title`, `title_en`, `sort_order`, `status`, `created_by`, `updated_by`)
VALUES
    (@lesson_id, 'core_vocabulary', '核心词汇', 'Core Vocabulary', 10, 'published', 1, 1),
    (@lesson_id, 'situational_dialogues', '情景对话', 'Situational Dialogues', 20, 'published', 1, 1),
    (@lesson_id, 'key_sentence_patterns', '核心句型', 'Key Sentence Patterns', 30, 'published', 1, 1),
    (@lesson_id, 'speaking_practice', '口语练习', 'Speaking Practice', 40, 'published', 1, 1),
    (@lesson_id, 'mini_exercises', '小练习', 'Mini Exercises', 50, 'published', 1, 1),
    (@lesson_id, 'useful_tips', '实用表达提示', 'Useful Tips', 60, 'published', 1, 1),
    (@lesson_id, 'extended_reading', '扩展阅读', 'Extended Reading', 70, 'published', 1, 1)
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`), `title_en` = VALUES(`title_en`), `sort_order` = VALUES(`sort_order`), `status` = 'published', `updated_by` = VALUES(`updated_by`);

INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'world', 10, 'world', '{"term":"world","meaning":"世界","pronunciation":"/wɜːrld/","examples":[{"english":"This world is amazing.","chinese":"这个世界太棒了。"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'core_vocabulary'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);
INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'create', 20, 'create', '{"term":"create","meaning":"创建","pronunciation":"/kriˈeɪt/","examples":[{"english":"Let’s create a new world.","chinese":"我们来创建一个新世界。"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'core_vocabulary'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);
INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'explore', 30, 'explore', '{"term":"explore","meaning":"探索","pronunciation":"/ɪkˈsplɔːr/","examples":[{"english":"Let’s explore the river.","chinese":"我们来探索这条河。"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'core_vocabulary'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);
INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'move', 40, 'move', '{"term":"move","meaning":"移动；前进","pronunciation":"/muːv/","examples":[{"english":"Move toward the river.","chinese":"向河边走。"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'core_vocabulary'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);
INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'block', 50, 'block', '{"term":"block","meaning":"方块","pronunciation":"/blɒk/","examples":[{"english":"A block can become a house.","chinese":"方块可以变成房子。"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'core_vocabulary'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);

INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'opening-scene', 10, 'Opening scene', '{"turns":[{"speaker":"Alex","english":"Ready to play?","chinese":"准备好开始游戏了吗？"},{"speaker":"Ben","english":"Yes! Let’s create a new world.","chinese":"准备好了！我们来创建一个新世界。"},{"speaker":"Alex","english":"Look around. I can see trees and a river.","chinese":"看看周围。我能看到树和一条河。"},{"speaker":"Ben","english":"Great. Let’s move toward the river.","chinese":"太好了。我们向河边走吧。"},{"speaker":"Alex","english":"What should we do first?","chinese":"我们首先应该做什么？"},{"speaker":"Ben","english":"We should collect some wood.","chinese":"我们应该收集一些木头。"},{"speaker":"Alex","english":"Good idea. Our adventure starts now!","chinese":"好主意。我们的冒险现在开始！"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'situational_dialogues'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);

INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'lets-pattern', 10, 'Let’s + verb', '{"pattern":"Let’s + verb","meaning":"我们来……吧","examples":[{"english":"Let’s explore!","chinese":"我们来探索吧！"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'key_sentence_patterns'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);
INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'can-see-pattern', 20, 'I can see + noun', '{"pattern":"I can see + noun","meaning":"我能看到……","examples":[{"english":"I can see trees.","chinese":"我能看到树。"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'key_sentence_patterns'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);
INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'should-first-pattern', 30, 'What should we do first?', '{"pattern":"What should we do first?","meaning":"我们首先应该做什么？","examples":[{"english":"We should collect some wood.","chinese":"我们应该收集一些木头。"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'key_sentence_patterns'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);

INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'say-it-together', 10, 'Say it together', '{"turns":[{"speaker":"Alex","english":"Let’s explore the new world!","chinese":"我们来探索新世界吧！"},{"speaker":"Ben","english":"I can see trees and a river.","chinese":"我能看到树和一条河。"},{"speaker":"Alex","english":"What should we do first?","chinese":"我们首先应该做什么？"},{"speaker":"Ben","english":"Let’s collect some wood.","chinese":"我们收集一些木头吧。"}]}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'speaking_practice'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);

INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'choose-resource', 10, 'Choose the first resource', '{"question":"What should Alex and Ben collect first?","question_zh":"Alex 和 Ben 首先应该收集什么？","answer":"wood","explanation":"Wood is an important first resource for tools and a shelter."}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'mini_exercises'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);
INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'make-a-plan', 20, 'Make a plan', '{"question":"Complete: Let’s ____ toward the river.","question_zh":"完成句子：我们向河边____。","answer":"move","explanation":"Use Let’s + verb to make a friendly plan."}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'mini_exercises'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);
INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'see-and-say', 30, 'See and say', '{"question":"Make a sentence with I can see.","question_zh":"用 I can see 造一个句子。","answer":"I can see trees.","explanation":"Look around your room and name one thing you can see."}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'mini_exercises'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);

INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'team-language', 10, 'Use Let’s when you invite a teammate', '{"text":"Use Let’s + verb when you invite someone to do something together.","chinese":"当你邀请队友一起做某事时，可以使用 Let’s + 动词。","guidance":"Keep the verb in its base form: Let’s explore, Let’s move, Let’s collect."}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'useful_tips'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);
INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'look-around', 20, 'Turn the game into English practice', '{"text":"Pause after each scene and say one sentence about what you can see.","chinese":"每完成一个场景就停下来，用一句英语说说你看到了什么。","guidance":"Start with I can see …"}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'useful_tips'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);

INSERT INTO `learning_lesson_item` (`section_id`, `item_code`, `item_order`, `title`, `payload_json`, `status`, `created_by`, `updated_by`)
SELECT `id`, 'story-reading', 10, 'Our new world', '{"text":"Alex and Ben wake up in a new world. They can see trees, grass, and a river. Alex asks what they should do first. Ben has a plan: collect wood, make tools, and build a small shelter before night. They move toward the river together. Their adventure has just begun!","chinese":"Alex 和 Ben 在一个新世界中醒来。他们能看到树、草地和一条河。Alex 问他们首先应该做什么。Ben 已经有了计划：收集木头、制作工具，并在天黑前建一个小庇护所。他们一起向河边走去。他们的冒险才刚刚开始！"}', 'published', 1, 1 FROM `learning_lesson_section` WHERE `lesson_id` = @lesson_id AND `section_code` = 'extended_reading'
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `payload_json` = VALUES(`payload_json`), `status` = 'published', `updated_by` = VALUES(`updated_by`);

-- Each card can carry its own visual without changing the lesson schema. The
-- browser renderer reads image_url from the structured payload.
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(i.`payload_json`, '$.image_url', '/static/minecraft/world-realistic.jpg')
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'core_vocabulary' AND i.`item_code` = 'world';
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(i.`payload_json`, '$.image_url', '/static/minecraft/house-realistic.jpg')
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'core_vocabulary' AND i.`item_code` = 'create';
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(i.`payload_json`, '$.image_url', '/static/minecraft/river-realistic.jpg')
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'core_vocabulary' AND i.`item_code` IN ('explore', 'move');
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(i.`payload_json`, '$.image_url', '/static/minecraft/wood-realistic.jpg')
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'core_vocabulary' AND i.`item_code` = 'block';

UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(
    i.`payload_json`,
    '$.turns[0].image_url', '/static/minecraft/world-realistic.jpg',
    '$.turns[1].image_url', '/static/minecraft/world-realistic.jpg',
    '$.turns[2].image_url', '/static/minecraft/river-realistic.jpg',
    '$.turns[3].image_url', '/static/minecraft/river-realistic.jpg',
    '$.turns[4].image_url', '/static/minecraft/world-realistic.jpg',
    '$.turns[5].image_url', '/static/minecraft/wood-realistic.jpg',
    '$.turns[6].image_url', '/static/minecraft/world-realistic.jpg'
)
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'situational_dialogues' AND i.`item_code` = 'opening-scene';
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(i.`payload_json`, '$.image_url', '/static/minecraft/river-realistic.jpg')
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'key_sentence_patterns' AND i.`item_code` IN ('lets-pattern', 'can-see-pattern');
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(i.`payload_json`, '$.image_url', '/static/minecraft/wood-realistic.jpg')
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'key_sentence_patterns' AND i.`item_code` = 'should-first-pattern';
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(
    i.`payload_json`,
    '$.turns[0].image_url', '/static/minecraft/river-realistic.jpg',
    '$.turns[1].image_url', '/static/minecraft/river-realistic.jpg',
    '$.turns[2].image_url', '/static/minecraft/world-realistic.jpg',
    '$.turns[3].image_url', '/static/minecraft/wood-realistic.jpg'
)
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'speaking_practice' AND i.`item_code` = 'say-it-together';
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(i.`payload_json`, '$.image_url', '/static/minecraft/wood-realistic.jpg')
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'mini_exercises' AND i.`item_code` = 'choose-resource';
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(i.`payload_json`, '$.image_url', '/static/minecraft/river-realistic.jpg')
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'mini_exercises' AND i.`item_code` IN ('make-a-plan', 'see-and-say');
UPDATE `learning_lesson_item` i
JOIN `learning_lesson_section` s ON s.`id` = i.`section_id`
SET i.`payload_json` = JSON_SET(i.`payload_json`, '$.image_url', '/static/minecraft/world-realistic.jpg')
WHERE s.`lesson_id` = @lesson_id AND s.`section_code` = 'extended_reading' AND i.`item_code` = 'story-reading';

COMMIT;
