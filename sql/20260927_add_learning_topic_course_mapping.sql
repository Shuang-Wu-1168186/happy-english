-- A course is reusable content.  Topics own their own many-to-many course
-- associations and ordering instead of storing topic_id on learning_course.

CREATE TABLE IF NOT EXISTS `learning_topic_course` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '专题课程关联主键ID',
    `topic_id` BIGINT UNSIGNED NOT NULL COMMENT '专题ID',
    `course_id` BIGINT UNSIGNED NOT NULL COMMENT '课程ID',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '专题内课程排序',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_topic_course` (`topic_id`, `course_id`),
    KEY `idx_learning_topic_course_topic_order` (`topic_id`, `sort_order`),
    KEY `idx_learning_topic_course_course` (`course_id`),
    CONSTRAINT `fk_learning_topic_course_topic`
        FOREIGN KEY (`topic_id`) REFERENCES `learning_topic` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_topic_course_course`
        FOREIGN KEY (`course_id`) REFERENCES `learning_course` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_topic_course_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_topic_course_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='专题课程关联表';

INSERT INTO `learning_topic_course`
    (`topic_id`, `course_id`, `sort_order`, `created_by`, `updated_by`)
SELECT course.`topic_id`, course.`id`, course.`sort_order`,
       course.`created_by`, course.`updated_by`
FROM `learning_course` course
WHERE course.`topic_id` IS NOT NULL
ON DUPLICATE KEY UPDATE `course_id` = VALUES(`course_id`);

ALTER TABLE `learning_course`
    DROP FOREIGN KEY `fk_learning_course_topic`,
    DROP COLUMN `topic_id`,
    ADD UNIQUE KEY `uk_learning_course_code` (`course_code`);
