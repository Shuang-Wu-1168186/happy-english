-- Earlier catalogue imports identified textbook lessons by development-database
-- IDs. When those IDs differed on Aliyun, the same published source lesson
-- could be inserted a second time under a different lesson_code. Retain the
-- original target lesson (the lowest ID) so any learner references remain
-- valid, and remove later duplicate source associations.

START TRANSACTION;

DELETE `duplicate`
FROM `learning_material_lesson` AS `duplicate`
JOIN `learning_material` AS `material`
  ON `material`.`id` = `duplicate`.`material_id`
JOIN `learning_material_lesson` AS `canonical`
  ON `canonical`.`material_id` = `duplicate`.`material_id`
 AND `canonical`.`source_resource` = `duplicate`.`source_resource`
 AND `canonical`.`source_reference_id` = `duplicate`.`source_reference_id`
 AND `canonical`.`id` < `duplicate`.`id`
WHERE `material`.`material_code` = 'english-textbook-current'
  AND `duplicate`.`source_resource` = 'textbook'
  AND `duplicate`.`source_reference_id` IS NOT NULL;

COMMIT;
