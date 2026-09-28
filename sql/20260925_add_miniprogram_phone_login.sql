-- Run this once on an existing Happy English MySQL database before enabling
-- WeChat Mini Program phone-number sign-in.
--
-- A phone number identifies one account for this login flow. Review the
-- result of this query first; any returned duplicate must be resolved before
-- the unique index can be added.
SELECT `contact_number`, COUNT(*) AS `account_count`
FROM `user`
WHERE `contact_number` IS NOT NULL AND TRIM(`contact_number`) <> ''
GROUP BY `contact_number`
HAVING COUNT(*) > 1;

-- Existing empty strings mean "no phone number" and must be NULL because a
-- unique index permits multiple NULL values but only one empty string.
UPDATE `user`
SET `contact_number` = NULL
WHERE `contact_number` IS NOT NULL AND TRIM(`contact_number`) = '';

-- Safe to re-run after the duplicate check above has been cleared.
SET @has_contact_number_index = (
    SELECT COUNT(*)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'user'
      AND index_name = 'uk_user_contact_number'
);
SET @add_contact_number_index = IF(
    @has_contact_number_index = 0,
    'ALTER TABLE `user` ADD UNIQUE KEY `uk_user_contact_number` (`contact_number`)',
    'SELECT 1'
);
PREPARE add_contact_number_index FROM @add_contact_number_index;
EXECUTE add_contact_number_index;
DEALLOCATE PREPARE add_contact_number_index;
