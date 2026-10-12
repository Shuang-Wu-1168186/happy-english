-- Consumer family joining uses a short-lived code that an owner can share.

SET @has_family_group_invite_code = (
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'family_group'
      AND column_name = 'invite_code'
);
SET @add_family_group_invite_code = IF(
    @has_family_group_invite_code = 0,
    'ALTER TABLE `family_group` ADD COLUMN `invite_code` VARCHAR(20) DEFAULT NULL AFTER `status`',
    'SELECT 1'
);
PREPARE add_family_group_invite_code FROM @add_family_group_invite_code;
EXECUTE add_family_group_invite_code;
DEALLOCATE PREPARE add_family_group_invite_code;

SET @has_family_group_invite_expiry = (
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'family_group'
      AND column_name = 'invite_code_expires_at'
);
SET @add_family_group_invite_expiry = IF(
    @has_family_group_invite_expiry = 0,
    'ALTER TABLE `family_group` ADD COLUMN `invite_code_expires_at` DATETIME DEFAULT NULL AFTER `invite_code`',
    'SELECT 1'
);
PREPARE add_family_group_invite_expiry FROM @add_family_group_invite_expiry;
EXECUTE add_family_group_invite_expiry;
DEALLOCATE PREPARE add_family_group_invite_expiry;

SET @has_family_group_invite_code_index = (
    SELECT COUNT(*) FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'family_group'
      AND index_name = 'uk_family_group_invite_code'
);
SET @add_family_group_invite_code_index = IF(
    @has_family_group_invite_code_index = 0,
    'ALTER TABLE `family_group` ADD UNIQUE KEY `uk_family_group_invite_code` (`invite_code`)',
    'SELECT 1'
);
PREPARE add_family_group_invite_code_index FROM @add_family_group_invite_code_index;
EXECUTE add_family_group_invite_code_index;
DEALLOCATE PREPARE add_family_group_invite_code_index;
