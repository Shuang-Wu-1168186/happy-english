-- Allow a learning course to contain multiple whole materials.
--
-- Run after 20260926_add_membership_material_management.sql.  This migration
-- is safe to run on an existing production database: it preserves each old
-- learning_course.material_id as the first course-material mapping.

CREATE TABLE IF NOT EXISTS `learning_course_material` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '课程教材关联主键ID',
    `course_id` BIGINT UNSIGNED NOT NULL COMMENT '课程ID',
    `material_id` BIGINT UNSIGNED NOT NULL COMMENT '教材ID',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '课程内教材排序',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_course_material` (`course_id`, `material_id`),
    KEY `idx_learning_course_material_course_order` (`course_id`, `sort_order`),
    KEY `idx_learning_course_material_material` (`material_id`, `sort_order`),
    CONSTRAINT `fk_learning_course_material_course`
        FOREIGN KEY (`course_id`) REFERENCES `learning_course` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_course_material_material`
        FOREIGN KEY (`material_id`) REFERENCES `learning_material` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_learning_course_material_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_course_material_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程教材关联表';

-- The duplicate-key clause makes reruns harmless and intentionally leaves any
-- admin-adjusted sort_order unchanged.
INSERT INTO `learning_course_material`
    (`course_id`, `material_id`, `sort_order`, `created_by`, `updated_by`)
SELECT course.`id`, course.`material_id`, 10, course.`created_by`, course.`updated_by`
FROM `learning_course` course
WHERE course.`material_id` IS NOT NULL
ON DUPLICATE KEY UPDATE `course_id` = VALUES(`course_id`);
