-- Inline the only learner-facing value still held in the source snapshots,
-- then retire the migration-only source table.  The conditional wrapper lets
-- a new installation skip this cleanup because its base schema has no source
-- table to remove.

DELIMITER //

CREATE PROCEDURE `drop_learning_lesson_item_source_20260928`()
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
          AND table_name = 'learning_lesson_item_source'
    ) THEN
        UPDATE `learning_lesson_item` item
        JOIN `learning_lesson_item_source` source_row
          ON source_row.`item_id` = item.`id`
        SET item.`payload_json` = JSON_SET(
            item.`payload_json`,
            '$.pronunciation',
            JSON_UNQUOTE(JSON_EXTRACT(source_row.`source_snapshot_json`, '$.pronunciation'))
        )
        WHERE JSON_EXTRACT(source_row.`source_snapshot_json`, '$.pronunciation') IS NOT NULL
          AND (
              JSON_EXTRACT(item.`payload_json`, '$.pronunciation') IS NULL
              OR JSON_UNQUOTE(JSON_EXTRACT(item.`payload_json`, '$.pronunciation')) = ''
          );

        DROP TABLE `learning_lesson_item_source`;
    END IF;
END//

CALL `drop_learning_lesson_item_source_20260928`();//
DROP PROCEDURE `drop_learning_lesson_item_source_20260928`//

DELIMITER ;
