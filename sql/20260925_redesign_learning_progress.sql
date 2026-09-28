-- Course progress and learning-time tracking for the module → topic → course
-- catalogue.  The old study_progress table is intentionally retained for
-- existing note and sentence pages until those resources are assigned courses.

CREATE TABLE IF NOT EXISTS `learning_progress` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '课程学习进度主键ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '学习用户ID',
    `course_id` BIGINT UNSIGNED NOT NULL COMMENT '学习课程ID',
    `status` VARCHAR(20) NOT NULL DEFAULT 'in_progress' COMMENT '学习状态：in_progress、completed',
    `total_item_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '课程学习条目总数快照',
    `completed_item_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '已完成学习条目数',
    `last_item_key` VARCHAR(160) DEFAULT NULL COMMENT '最后学习条目的稳定键',
    `last_item_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后学习条目的关联记录ID',
    `last_position_seconds` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '最后学习位置秒数',
    `started_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '首次开始学习时间',
    `last_studied_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近学习时间',
    `completed_at` DATETIME DEFAULT NULL COMMENT '课程完成时间',
    `accumulated_seconds` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '已累计有效学习秒数',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_progress_user_course` (`user_id`, `course_id`),
    KEY `idx_learning_progress_user_status_last_studied` (`user_id`, `status`, `last_studied_at`),
    KEY `idx_learning_progress_course` (`course_id`),
    CONSTRAINT `fk_learning_progress_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_progress_course` FOREIGN KEY (`course_id`) REFERENCES `learning_course` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户课程学习进度表';

CREATE TABLE IF NOT EXISTS `learning_progress_item` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '课程条目进度主键ID',
    `progress_id` BIGINT UNSIGNED NOT NULL COMMENT '所属课程学习进度ID',
    `item_key` VARCHAR(160) NOT NULL COMMENT '课程内条目的稳定键',
    `item_type` VARCHAR(50) NOT NULL DEFAULT 'course_item' COMMENT '条目类型，例如 dialogue、video、quiz',
    `item_reference_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '关联内容记录ID',
    `is_completed` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否完成：0-否，1-是',
    `last_position_seconds` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '条目最后学习位置秒数',
    `attempt_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '作答或完成尝试次数',
    `score` TINYINT UNSIGNED DEFAULT NULL COMMENT '最近一次得分，0-100',
    `started_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '首次开始学习时间',
    `last_studied_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近学习时间',
    `completed_at` DATETIME DEFAULT NULL COMMENT '完成时间',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_progress_item_key` (`progress_id`, `item_key`),
    KEY `idx_learning_progress_item_progress_completed` (`progress_id`, `is_completed`),
    CONSTRAINT `fk_learning_progress_item_progress`
        FOREIGN KEY (`progress_id`) REFERENCES `learning_progress` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户课程条目学习进度表';

CREATE TABLE IF NOT EXISTS `learning_study_session` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '学习会话主键ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '学习用户ID',
    `progress_id` BIGINT UNSIGNED NOT NULL COMMENT '所属课程学习进度ID',
    `course_id` BIGINT UNSIGNED NOT NULL COMMENT '学习课程ID，便于按课程汇总',
    `platform` VARCHAR(30) NOT NULL DEFAULT 'web' COMMENT '学习端：web、mini_program',
    `entry_source` VARCHAR(100) DEFAULT NULL COMMENT '进入来源，例如 home、recommendation',
    `started_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '会话开始时间',
    `last_heartbeat_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后活跃时间',
    `ended_at` DATETIME DEFAULT NULL COMMENT '会话结束时间',
    `active_seconds` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '有效学习秒数',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

    PRIMARY KEY (`id`),
    KEY `idx_learning_study_session_user_started` (`user_id`, `started_at`),
    KEY `idx_learning_study_session_course_started` (`course_id`, `started_at`),
    KEY `idx_learning_study_session_progress_open` (`progress_id`, `ended_at`),
    CONSTRAINT `fk_learning_study_session_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_study_session_progress`
        FOREIGN KEY (`progress_id`) REFERENCES `learning_progress` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_study_session_course`
        FOREIGN KEY (`course_id`) REFERENCES `learning_course` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户学习时间会话记录表';
