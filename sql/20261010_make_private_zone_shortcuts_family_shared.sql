-- Family-shared private-zone shortcuts.
--
-- A shortcut is configured by an administrator, but it belongs to a family
-- learning group.  Existing account-only shortcuts are moved into one active
-- family for their owner so the existing entries remain available after this
-- change.  When the owner has no active family yet, create a small starter
-- family with that owner as its first member.

SET @has_private_zone_shortcut_family_group_id = (
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'private_zone_shortcut'
      AND column_name = 'family_group_id'
);
SET @add_private_zone_shortcut_family_group_id = IF(
    @has_private_zone_shortcut_family_group_id = 0,
    'ALTER TABLE `private_zone_shortcut` ADD COLUMN `family_group_id` BIGINT UNSIGNED DEFAULT NULL AFTER `scope_type`',
    'SELECT 1'
);
PREPARE add_private_zone_shortcut_family_group_id FROM @add_private_zone_shortcut_family_group_id;
EXECUTE add_private_zone_shortcut_family_group_id;
DEALLOCATE PREPARE add_private_zone_shortcut_family_group_id;

SET @has_private_zone_shortcut_family_index = (
    SELECT COUNT(*) FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'private_zone_shortcut'
      AND index_name = 'idx_private_zone_shortcut_family_status_order'
);
SET @add_private_zone_shortcut_family_index = IF(
    @has_private_zone_shortcut_family_index = 0,
    'ALTER TABLE `private_zone_shortcut` ADD KEY `idx_private_zone_shortcut_family_status_order` (`family_group_id`, `status`, `sort_order`)',
    'SELECT 1'
);
PREPARE add_private_zone_shortcut_family_index FROM @add_private_zone_shortcut_family_index;
EXECUTE add_private_zone_shortcut_family_index;
DEALLOCATE PREPARE add_private_zone_shortcut_family_index;

SET @has_private_zone_shortcut_family_fk = (
    SELECT COUNT(*) FROM information_schema.referential_constraints
    WHERE constraint_schema = DATABASE()
      AND table_name = 'private_zone_shortcut'
      AND constraint_name = 'fk_private_zone_shortcut_family'
);
SET @add_private_zone_shortcut_family_fk = IF(
    @has_private_zone_shortcut_family_fk = 0,
    'ALTER TABLE `private_zone_shortcut` ADD CONSTRAINT `fk_private_zone_shortcut_family` FOREIGN KEY (`family_group_id`) REFERENCES `family_group` (`id`) ON DELETE CASCADE',
    'SELECT 1'
);
PREPARE add_private_zone_shortcut_family_fk FROM @add_private_zone_shortcut_family_fk;
EXECUTE add_private_zone_shortcut_family_fk;
DEALLOCATE PREPARE add_private_zone_shortcut_family_fk;

-- Give every shortcut owner without an active family a family that can later
-- receive invited members.  Owners who already belong to a family keep that
-- family instead of receiving an extra group.
INSERT INTO `family_group` (`name`, `owner_user_id`, `status`)
SELECT
    CONCAT(
        COALESCE(NULLIF(TRIM(account.`full_name`), ''), account.`username`, '学习'),
        '的家庭'
    ),
    account.`id`,
    'active'
FROM `user` AS account
JOIN (
    SELECT DISTINCT `user_id`
    FROM `private_zone_shortcut`
    WHERE `scope_type` IN ('personal', 'legacy_personal')
      AND `family_group_id` IS NULL
) AS shortcut_owner
  ON shortcut_owner.`user_id` = account.`id`
WHERE NOT EXISTS (
    SELECT 1
    FROM `family_group_member` AS member
    JOIN `family_group` AS family
      ON family.`id` = member.`family_group_id`
     AND family.`status` = 'active'
    WHERE member.`user_id` = account.`id`
      AND member.`status` = 'active'
      AND member.`role` IN ('owner', 'admin')
);

-- The fallback family needs an owner membership before it can be selected by
-- the normal family visibility query.
INSERT INTO `family_group_member`
    (`family_group_id`, `user_id`, `role`, `status`, `invited_by`, `joined_at`)
SELECT
    family.`id`, family.`owner_user_id`, 'owner', 'active',
    family.`owner_user_id`, CURRENT_TIMESTAMP
FROM `family_group` AS family
JOIN `user` AS account
  ON account.`id` = family.`owner_user_id`
JOIN (
    SELECT DISTINCT `user_id`
    FROM `private_zone_shortcut`
    WHERE `scope_type` IN ('personal', 'legacy_personal')
      AND `family_group_id` IS NULL
) AS shortcut_owner
  ON shortcut_owner.`user_id` = family.`owner_user_id`
LEFT JOIN `family_group_member` AS existing_member
  ON existing_member.`family_group_id` = family.`id`
 AND existing_member.`user_id` = family.`owner_user_id`
WHERE family.`status` = 'active'
  AND family.`name` = CONCAT(
      COALESCE(NULLIF(TRIM(account.`full_name`), ''), account.`username`, '学习'),
      '的家庭'
  )
  AND existing_member.`id` IS NULL;

-- Prefer the oldest active family the owner belongs to.  This keeps existing
-- real families intact and only uses the fallback group when needed.
UPDATE `private_zone_shortcut` AS shortcut
JOIN (
    SELECT
        shortcut_owner.`user_id`,
        MIN(member.`family_group_id`) AS `family_group_id`
    FROM (
        SELECT DISTINCT `user_id`
        FROM `private_zone_shortcut`
        WHERE `scope_type` IN ('personal', 'legacy_personal')
          AND `family_group_id` IS NULL
    ) AS shortcut_owner
    JOIN `family_group_member` AS member
      ON member.`user_id` = shortcut_owner.`user_id`
     AND member.`status` = 'active'
     AND member.`role` IN ('owner', 'admin')
    JOIN `family_group` AS family
      ON family.`id` = member.`family_group_id`
     AND family.`status` = 'active'
    GROUP BY shortcut_owner.`user_id`
) AS assignment
  ON assignment.`user_id` = shortcut.`user_id`
SET shortcut.`family_group_id` = assignment.`family_group_id`,
    shortcut.`scope_type` = 'family'
WHERE shortcut.`scope_type` IN ('personal', 'legacy_personal')
  AND shortcut.`family_group_id` IS NULL;

ALTER TABLE `private_zone_shortcut`
    MODIFY COLUMN `scope_type` VARCHAR(20) NOT NULL DEFAULT 'family';
