-- Run once before deploying session revocation support to an existing MySQL database.
-- The migration is idempotent and gives each existing account a random version.

SET @has_session_version := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'user'
      AND column_name = 'session_version'
);

SET @add_session_version_sql := IF(
    @has_session_version = 0,
    'ALTER TABLE `user` ADD COLUMN `session_version` VARCHAR(64) NOT NULL DEFAULT '''' COMMENT ''会话撤销版本'' AFTER `password_hash`',
    'SELECT 1'
);
PREPARE add_session_version FROM @add_session_version_sql;
EXECUTE add_session_version;
DEALLOCATE PREPARE add_session_version;

UPDATE `user`
SET `session_version` = SHA2(CONCAT(UUID(), ':', `id`, ':', RAND(), ':', NOW(6)), 256)
WHERE `session_version` = '';
