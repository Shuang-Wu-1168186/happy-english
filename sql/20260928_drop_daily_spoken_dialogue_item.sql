-- Retire the legacy daily-dialogue source after all learner traffic reads the
-- generic structured lesson tables.  Source snapshots remain in
-- learning_lesson_item_source for traceability.

DELIMITER //

CREATE PROCEDURE `drop_daily_spoken_dialogue_item_20260928`()
BEGIN
    IF EXISTS (
        SELECT 1
        FROM `learning_course`
        WHERE `content_resource` = 'dialogues'
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot drop daily_spoken_dialogue_item: a course still uses dialogues.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM `learning_material_lesson` lesson
        WHERE lesson.`source_resource` = 'dialogues'
          AND lesson.`lesson_format` <> 'structured'
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot drop daily_spoken_dialogue_item: a dialogue lesson is not structured.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM `learning_material_lesson` lesson
        WHERE lesson.`source_resource` = 'dialogues'
          AND NOT EXISTS (
              SELECT 1
              FROM `learning_lesson_section` section_row
              WHERE section_row.`lesson_id` = lesson.`id`
          )
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot drop daily_spoken_dialogue_item: a dialogue lesson has no generic sections.';
    END IF;

    UPDATE `learning_template`
    SET `description` = '按通用课时区块展示的情景对话页。',
        `content_kind` = 'structured'
    WHERE `template_code` = 'dialogue'
      AND `template_version` = 1;

    UPDATE `learning_material_lesson`
    SET `source_resource` = NULL,
        `source_reference_id` = NULL
    WHERE `source_resource` = 'dialogues'
      AND `lesson_format` = 'structured';

    DROP TABLE `daily_spoken_dialogue_item`;
END//

CALL `drop_daily_spoken_dialogue_item_20260928`();//
DROP PROCEDURE `drop_daily_spoken_dialogue_item_20260928`//

DELIMITER ;
