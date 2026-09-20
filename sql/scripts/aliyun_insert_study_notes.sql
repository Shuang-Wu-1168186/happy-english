-- 学习笔记及其首张学习卡片。
-- 阿里云 RDS 使用 utf8mb4 字符集执行。

INSERT INTO `english_note` (
    `note_date`,
    `title`,
    `source`,
    `summary`,
    `share_status`,
    `priority_order`,
    `created_by`,
    `updated_by`
) SELECT
    '2026-09-15',
    'Study Notes',
    'self-study',
    'English learning notes.',
    0,
    0,
    1,
    1
WHERE NOT EXISTS (
    SELECT 1
    FROM `english_note`
    WHERE `note_date` = '2026-09-15'
      AND `title` = 'Study Notes'
);

SET @study_notes_id := (
    SELECT `id`
    FROM `english_note`
    WHERE `note_date` = '2026-09-15'
      AND `title` = 'Study Notes'
    ORDER BY `id` DESC
    LIMIT 1
);

INSERT INTO `english_note_item` (
    `note_id`,
    `item_order`,
    `item_type`,
    `item_title`,
    `raw_text`,
    `english_text`,
    `chinese_text`,
    `explanation`,
    `examples`,
    `keywords`,
    `share_status`,
    `priority_order`,
    `created_by`,
    `updated_by`
) SELECT
    @study_notes_id,
    1,
    'knowledge',
    'Study Notes',
    'Keep useful English in one place and review it regularly.',
    'New words · useful phrases · example sentences',
    '把新单词、实用短语和例句集中记录，并定期复习。',
    'Use this note as a starting point for your English learning records.',
    'Vocabulary\nPhrases\nExample sentences',
    'study notes, learning notes, 学习笔记',
    0,
    0,
    1,
    1
WHERE NOT EXISTS (
    SELECT 1
    FROM `english_note_item`
    WHERE `note_id` = @study_notes_id
      AND `item_order` = 1
);
