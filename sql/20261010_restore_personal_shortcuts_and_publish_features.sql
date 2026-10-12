-- Restore the intended two-level navigation model for the private zone:
-- * private_zone_feature contains public learning entries for every learner;
-- * private_zone_shortcut contains shortcuts owned by one learner.

SET @has_private_zone_feature_target_url = (
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'private_zone_feature'
      AND column_name = 'target_url'
);
SET @add_private_zone_feature_target_url = IF(
    @has_private_zone_feature_target_url = 0,
    'ALTER TABLE `private_zone_feature` ADD COLUMN `target_url` VARCHAR(1000) DEFAULT NULL AFTER `route_key`',
    'SELECT 1'
);
PREPARE add_private_zone_feature_target_url FROM @add_private_zone_feature_target_url;
EXECUTE add_private_zone_feature_target_url;
DEALLOCATE PREPARE add_private_zone_feature_target_url;

-- Preserve an administrator's later edits.  These values only fill records
-- created before public entries had their own concrete destination.
UPDATE `private_zone_feature`
SET `target_url` = CASE `feature_code`
    WHEN 'my-english-notes' THEN '/learn/notes'
    WHEN 'my-textbooks' THEN '/learning-materials/1'
    WHEN 'textbook-vocabulary' THEN '/learn/kids-cards'
    WHEN 'my-interview-questions' THEN '/learn/interviews'
    WHEN 'saved-learning' THEN '/private-zone/favorite-courses'
    ELSE `target_url`
END
WHERE (`target_url` IS NULL OR `target_url` = '')
  AND `feature_code` IN (
      'my-english-notes',
      'my-textbooks',
      'textbook-vocabulary',
      'my-interview-questions',
      'saved-learning'
  );

-- The textbook ID differs between deployments, so replace only the original
-- placeholder with the actual published Guoguo textbook destination.
UPDATE `private_zone_feature` AS feature
JOIN `learning_material` AS material
  ON material.`material_code` = 'english-textbook-current'
 AND material.`is_published` = 1
SET feature.`target_url` = CONCAT('/learning-materials/', material.`id`)
WHERE feature.`feature_code` = 'my-textbooks'
  AND feature.`target_url` = '/learning-materials/1';

-- The previous interim release marked the bundled administrator shortcuts as
-- platform rows.  They are personal entries and must only appear for their
-- owner.  Public entries now come from private_zone_feature above.
UPDATE `private_zone_shortcut`
SET `scope_type` = 'personal'
WHERE `scope_type` IN ('platform', 'legacy_personal');
