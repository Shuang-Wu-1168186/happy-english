-- Add the Podcast listening training area as a separate training dimension.
-- Episodes and topics can be attached later without moving level-based areas.

START TRANSACTION;

INSERT INTO `learning_module`
    (`module_code`, `module_type`, `name`, `name_en`, `description`, `icon`, `color`, `route_key`, `sort_order`, `is_published`)
VALUES
    ('podcast-listening', 'training', 'Podcast 听力训练', 'Podcast Listening',
     '用真实语音和生活场景提升英语听力。', '🎧', '#1F9D82', 'podcast-listening', 70, 1)
ON DUPLICATE KEY UPDATE
    `module_type` = VALUES(`module_type`),
    `name` = VALUES(`name`),
    `name_en` = VALUES(`name_en`),
    `description` = VALUES(`description`),
    `icon` = VALUES(`icon`),
    `color` = VALUES(`color`),
    `route_key` = VALUES(`route_key`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`),
    `updated_at` = CURRENT_TIMESTAMP;

COMMIT;
