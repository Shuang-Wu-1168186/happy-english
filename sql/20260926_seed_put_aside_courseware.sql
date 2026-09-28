-- A first published courseware lesson using english_note_item #1514 (put aside).
-- Run after 20260926_add_courseware_blocks.sql. The script is safe to rerun.

SET @actor_id = (
    SELECT `id` FROM `user` WHERE `role` = 'admin' ORDER BY `id` LIMIT 1
);
SET @module_id = (
    SELECT `id` FROM `learning_module` WHERE `module_code` = 'elementary-english' LIMIT 1
);
SET @source_item_id = (
    SELECT `id` FROM `english_note_item` WHERE `id` = 1514 LIMIT 1
);

INSERT INTO `learning_topic` (
    `module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`, `created_by`
)
SELECT @module_id, 'phrase-courseware', '短语课件', 'Phrase Courseware',
       '通过记忆画面、真实场景和开口练习掌握高频短语。', 15, 1, @actor_id
WHERE @module_id IS NOT NULL AND @source_item_id IS NOT NULL
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`), `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`), `is_published` = VALUES(`is_published`),
    `updated_by` = @actor_id;

SET @topic_id = (
    SELECT `id` FROM `learning_topic`
    WHERE `module_id` = @module_id AND `topic_code` = 'phrase-courseware' LIMIT 1
);

-- A material is the reusable textbook container.  Keep the lesson's
-- `lesson_format = courseware` at the lesson layer, not in this material code.
UPDATE `learning_material`
SET `material_code` = 'idiomatic-everyday-english'
WHERE `topic_id` = @topic_id
  AND `material_code` = 'put-aside-courseware'
  AND NOT EXISTS (
      SELECT 1 FROM (
          SELECT `id` FROM `learning_material`
          WHERE `topic_id` = @topic_id AND `material_code` = 'idiomatic-everyday-english'
      ) AS `existing_material`
  );

INSERT INTO `learning_material` (
    `topic_id`, `material_code`, `title`, `title_en`, `summary`, `material_type`,
    `estimated_minutes`, `sort_order`, `is_published`, `created_by`
)
SELECT @topic_id, 'idiomatic-everyday-english', '地道日常用语', 'idiomatic everyday English',
       '把一个短语放进画面、场景和自己的表达里。', 'textbook', 8, 10, 1, @actor_id
WHERE @topic_id IS NOT NULL
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`), `title_en` = VALUES(`title_en`), `summary` = VALUES(`summary`),
    `estimated_minutes` = VALUES(`estimated_minutes`), `is_published` = VALUES(`is_published`),
    `updated_by` = @actor_id;

SET @material_id = (
    SELECT `id` FROM `learning_material`
    WHERE `topic_id` = @topic_id AND `material_code` = 'idiomatic-everyday-english' LIMIT 1
);

INSERT INTO `learning_material_lesson` (
    `material_id`, `lesson_code`, `title`, `title_en`, `summary`, `lesson_format`,
    `estimated_minutes`, `sort_order`, `is_published`, `created_by`
)
SELECT @material_id, 'phrase-put-aside', 'put aside', 'put aside',
       '放到一边、暂时搁置，以及留出时间或钱。', 'courseware', 8, 10, 0, @actor_id
WHERE @material_id IS NOT NULL
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`), `title_en` = VALUES(`title_en`), `summary` = VALUES(`summary`),
    `lesson_format` = 'courseware', `estimated_minutes` = VALUES(`estimated_minutes`),
    `updated_by` = @actor_id;

SET @lesson_id = (
    SELECT `id` FROM `learning_material_lesson`
    WHERE `material_id` = @material_id AND `lesson_code` = 'phrase-put-aside' LIMIT 1
);

INSERT INTO `courseware_block` (
    `material_lesson_id`, `block_code`, `block_type`, `title`, `payload_json`,
    `sort_order`, `status`, `created_by`, `updated_by`
)
SELECT @lesson_id, `block_code`, `block_type`, `title`, `payload_json`, `sort_order`, 'published', @actor_id, @actor_id
FROM (
    SELECT 'hero' AS `block_code`, 'hero' AS `block_type`, NULL AS `title`,
           '{"phrase":"put aside","meaning":"把……放到一边；暂时不考虑；留出 / 存下","memory":"put = 放 · aside = 到旁边","key_sentence":{"english":"Let’s put that aside for now.","chinese":"这件事我们现在先放一放。"}}' AS `payload_json`, 10 AS `sort_order`
    UNION ALL SELECT 'three-uses', 'usage_group', '一个画面，三种用法',
           '{"uses":[{"title":"把东西放到一边","description":"把……放到一边","tone":"physical","examples":[{"english":"She put the book aside and answered the phone.","chinese":"她把书放到一边，然后接电话。"},{"english":"Please put those documents aside for now.","chinese":"请先把那些文件放到一边。"}]},{"title":"暂时不考虑 / 撇开","description":"put aside + differences / concerns / feelings / arguments","tone":"decision","examples":[{"english":"We need to put aside our differences and work together.","chinese":"我们需要暂时搁置分歧，一起合作。"},{"english":"Let’s put that issue aside for the moment.","chinese":"我们暂时先搁置这个问题。"}]},{"title":"留出 / 存下一部分","description":"put aside money / time","tone":"reserve","examples":[{"english":"I try to put aside some money every month.","chinese":"我每个月都会尽量存一些钱。"},{"english":"We should put aside some time to review the design.","chinese":"我们应该留出一些时间来审核设计。"}]}]}', 20
    UNION ALL SELECT 'workplace-dialogue', 'dialogue', '工作 / IT 场景',
           '{"scene":"工作 / IT 场景","lines":[{"speaker":"同事 A","english":"Let’s put aside the UI issue and focus on the API first.","chinese":"我们先把 UI 的问题放一放，优先处理 API。"},{"speaker":"同事 B","english":"We need to put aside some time for testing.","chinese":"我们需要留出一些时间做测试。"},{"speaker":"同事 A","english":"Putting aside performance concerns, the current design is quite flexible.","chinese":"暂且不考虑性能问题，目前这个设计还是比较灵活的。"}]}', 30
    UNION ALL SELECT 'put-vs-set-aside', 'comparison', 'put aside vs set aside',
           '{"items":[{"expression":"put aside","label":"更口语","meaning":"放一边 / 暂时不管","english":"Put aside your phone and listen.","chinese":"把手机放一边，听我说。"},{"expression":"set aside","label":"也可表示留出，稍正式","meaning":"留出","english":"We set aside two hours for testing.","chinese":"我们专门留了两个小时做测试。"}]}', 40
    UNION ALL SELECT 'say-it', 'output', '轮到你开口',
           '{"instruction":"把空格替换成自己的内容。","patterns":["Let’s put aside ________ and focus on ________ first.","We should put aside some time to ________.","I try to put aside some ________ every month."]}', 50
    UNION ALL SELECT 'recap', 'recap', NULL,
           '{"summary":"问题放一边 → 暂时不考虑；钱放一边 → 存起来；时间放一边 → 预留出来","key_sentence":{"english":"Let’s put that aside for now.","chinese":"这件事我们现在先放一放。"}}', 60
) AS `blocks`
WHERE @lesson_id IS NOT NULL
ON DUPLICATE KEY UPDATE
    `block_type` = VALUES(`block_type`), `title` = VALUES(`title`),
    `payload_json` = VALUES(`payload_json`), `sort_order` = VALUES(`sort_order`),
    `status` = 'published', `updated_by` = @actor_id;

DELETE `source`
FROM `courseware_block_source` AS `source`
JOIN `courseware_block` AS `block` ON `block`.`id` = `source`.`courseware_block_id`
WHERE `block`.`material_lesson_id` = @lesson_id;

INSERT INTO `courseware_block_source` (
    `courseware_block_id`, `source_resource`, `source_reference_id`, `source_field`,
    `source_snapshot_text`, `source_hash`, `sort_order`
)
SELECT `id`, 'english_note_item', @source_item_id, 'raw_text', 'put aside', SHA2('put aside', 256), 10
FROM `courseware_block` WHERE `material_lesson_id` = @lesson_id;

UPDATE `learning_material_lesson`
SET `is_published` = 1, `updated_by` = @actor_id
WHERE `id` = @lesson_id
  AND (SELECT COUNT(*) FROM `courseware_block` WHERE `material_lesson_id` = @lesson_id AND `status` = 'published') = 6;

INSERT INTO `learning_course` (
    `topic_id`, `material_id`, `course_code`, `title`, `title_en`, `summary`, `course_type`,
    `estimated_minutes`, `difficulty_code`, `sort_order`, `is_published`, `access_policy`, `created_by`
)
SELECT @topic_id, @material_id, 'put-aside-course', 'put aside', 'put aside',
       '从理解到开口，掌握 put aside 的三种常见用法。', 'phrase', 8, 'elementary', 10, 1, 'free', @actor_id
WHERE @lesson_id IS NOT NULL
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`), `title_en` = VALUES(`title_en`), `summary` = VALUES(`summary`),
    `estimated_minutes` = VALUES(`estimated_minutes`), `is_published` = VALUES(`is_published`),
    `updated_by` = @actor_id;
