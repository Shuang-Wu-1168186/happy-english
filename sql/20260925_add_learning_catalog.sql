-- Module → topic → course catalogue for the whole learning application.
-- Run this once on an existing Happy English MySQL database.

CREATE TABLE IF NOT EXISTS `learning_module` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '学习区域主键ID',
    `module_code` VARCHAR(80) NOT NULL COMMENT '稳定业务编码',
    `name` VARCHAR(100) NOT NULL COMMENT '学习区域名称',
    `name_en` VARCHAR(100) DEFAULT NULL COMMENT '英文名称',
    `description` VARCHAR(500) DEFAULT NULL COMMENT '学习区域简介',
    `icon` VARCHAR(32) DEFAULT NULL COMMENT '图标或 emoji',
    `color` VARCHAR(32) DEFAULT NULL COMMENT '展示颜色',
    `route_key` VARCHAR(100) DEFAULT NULL COMMENT '客户端路由或已有内容资源标识',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序值，越小越靠前',
    `is_published` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否对学习者可见：0-否，1-是',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建人ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '修改人ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_module_code` (`module_code`),
    KEY `idx_learning_module_published_order` (`is_published`, `sort_order`),
    CONSTRAINT `fk_learning_module_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_module_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习应用学习区域表';

CREATE TABLE IF NOT EXISTS `learning_topic` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主题主键ID',
    `module_id` BIGINT UNSIGNED NOT NULL COMMENT '所属学习区域ID',
    `topic_code` VARCHAR(100) NOT NULL COMMENT '区域内稳定业务编码',
    `title` VARCHAR(200) NOT NULL COMMENT '主题标题',
    `title_en` VARCHAR(200) DEFAULT NULL COMMENT '主题英文标题',
    `description` TEXT DEFAULT NULL COMMENT '主题简介',
    `cover_url` VARCHAR(500) DEFAULT NULL COMMENT '主题封面图片地址',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序值，越小越靠前',
    `is_published` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否对学习者可见：0-否，1-是',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建人ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '修改人ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_topic_module_code` (`module_id`, `topic_code`),
    KEY `idx_learning_topic_module_published_order` (`module_id`, `is_published`, `sort_order`),
    CONSTRAINT `fk_learning_topic_module` FOREIGN KEY (`module_id`) REFERENCES `learning_module` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_learning_topic_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_topic_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习主题表';

CREATE TABLE IF NOT EXISTS `learning_course` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '课程主键ID',
    `topic_id` BIGINT UNSIGNED NOT NULL COMMENT '所属主题ID',
    `course_code` VARCHAR(120) NOT NULL COMMENT '主题内稳定业务编码',
    `title` VARCHAR(255) NOT NULL COMMENT '课程标题',
    `title_en` VARCHAR(255) DEFAULT NULL COMMENT '课程英文标题',
    `summary` TEXT DEFAULT NULL COMMENT '课程简介',
    `course_type` VARCHAR(50) NOT NULL DEFAULT 'lesson' COMMENT '课程类型，例如 lesson、dialogue、exam',
    `content_resource` VARCHAR(80) DEFAULT NULL COMMENT '关联的已有内容资源，例如 dialogues、notes',
    `content_reference_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '关联资源的记录ID',
    `content_json` LONGTEXT DEFAULT NULL COMMENT '课程自包含的结构化学习内容 JSON',
    `cover_url` VARCHAR(500) DEFAULT NULL COMMENT '课程封面图片地址',
    `estimated_minutes` SMALLINT UNSIGNED DEFAULT NULL COMMENT '预计学习分钟数',
    `difficulty_code` VARCHAR(50) DEFAULT NULL COMMENT '难度编码',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序值，越小越靠前',
    `is_published` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否对学习者可见：0-否，1-是',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建人ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '修改人ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_course_topic_code` (`topic_id`, `course_code`),
    KEY `idx_learning_course_topic_published_order` (`topic_id`, `is_published`, `sort_order`),
    CONSTRAINT `fk_learning_course_topic` FOREIGN KEY (`topic_id`) REFERENCES `learning_topic` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_learning_course_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_course_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习课程表';

-- The codes are stable identifiers for APIs and clients; administrators may
-- change display text without breaking the hierarchy.
INSERT INTO `learning_module`
(`module_code`, `name`, `name_en`, `description`, `icon`, `color`, `route_key`, `sort_order`, `is_published`)
VALUES
('learning-notes', '学习笔记', 'Learning Notes', '沉淀个人学习笔记和重点卡片。', '📝', '#5B7CFA', 'notes', 10, 1),
('foundation', '基础学习', 'Foundation Learning', '英文课本、自然拼读和课本单词，按方向打好英语基础。', '📘', '#2DAA8A', 'textbook', 20, 1),
('math-zone', '数学专区', 'Math Zone', '用英语学习和理解数学知识。', '📐', '#F59E0B', 'math-cards', 30, 1),
('daily-speaking', '日常开口', 'Everyday Speaking', '每日口语与真实场景对话，帮助你自然开口。', '💬', '#EC6A8C', 'sentences', 40, 1),
('workplace', '职场专区', 'Workplace English', '面试英语、专业词汇和职场表达，提升工作场景沟通能力。', '💼', '#64748B', 'interviews', 50, 1),
('advanced-english', '高级英语', 'Advanced English', '进阶词汇、表达与高阶学习内容。', '🚀', '#8B5CF6', 'vocabulary', 60, 1)
ON DUPLICATE KEY UPDATE `module_code` = VALUES(`module_code`);

-- 学习笔记是每位用户的固定入口；笔记本身保留在用户私有内容中，
-- 不会因为建立这个专题而变成平台公开教材。
INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'my-english-notes', '我的英语笔记', 'My English Notes',
       '整理个人学习笔记、卡片和复习内容。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'learning-notes'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

-- 基础学习的三个固定学习主题。每个主题下面的具体教材、拼读课和
-- 单词课会作为 learning_course 记录按 topic_id 导入。
INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'english-textbook', '英文课本', 'English Textbook',
       '跟着课文听读、理解和练习，按单元建立扎实基础。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'foundation'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'natural-phonics', '自然拼读', 'Natural Phonics',
       '从字母、音素和拼读规律开始，练出见词能读的能力。', 20, 1
FROM `learning_module`
WHERE `module_code` = 'foundation'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'textbook-vocabulary', '课本单词', 'Textbook Vocabulary',
       '围绕课本单元积累核心单词、发音和例句。', 30, 1
FROM `learning_module`
WHERE `module_code` = 'foundation'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

-- 日常开口的两个入口分别承接每日句子练习和成组的场景对话。
INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'daily-speaking-practice', '每日口语', 'Daily Speaking',
       '每天练习实用句子和短语，让开口成为自然习惯。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'daily-speaking'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'daily-speaking-dialogues', '日常口语对话专区', 'Daily Spoken Dialogues',
       '围绕真实生活场景学习成组对话，练习自然回应。', 20, 1
FROM `learning_module`
WHERE `module_code` = 'daily-speaking'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

-- 职场专区的主题。各具体题库、词汇课会作为 learning_course 记录按
-- topic_id 导入，保留后续扩展商务沟通、会议表达等内容的空间。
INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'interview-english', '面试英语', 'Interview English',
       '围绕自我介绍、常见问题和完整回答，做好求职面试准备。', 10, 1
FROM `learning_module`
WHERE `module_code` = 'workplace'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);

INSERT INTO `learning_topic`
(`module_id`, `topic_code`, `title`, `title_en`, `description`, `sort_order`, `is_published`)
SELECT `id`, 'professional-vocabulary', '专业词汇', 'Professional Vocabulary',
       '积累工作、技术和专业沟通常用的词汇与表达。', 20, 1
FROM `learning_module`
WHERE `module_code` = 'workplace'
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `title_en` = VALUES(`title_en`),
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_published` = VALUES(`is_published`);
