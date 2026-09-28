-- Membership and material-management migration for Happy English.
--
-- Target: Aliyun RDS for MySQL 5.7+ / MySQL 8.0+.
-- Prerequisite: run 20260925_add_learning_catalog.sql first, because this
-- migration requires learning_topic and learning_course.
--
-- Back up the database before running this file. It is safe to re-run for the
-- new tables and guarded ALTER operations, but it intentionally does not
-- fabricate materials for legacy learning_course direct-content records.
-- Migrate those records through the admin API or a reviewed data-import script.

CREATE TABLE IF NOT EXISTS `learning_material` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '教材主键ID',
    `topic_id` BIGINT UNSIGNED NOT NULL COMMENT '所属学习主题ID',
    `material_code` VARCHAR(120) NOT NULL COMMENT '主题内稳定教材编码',
    `title` VARCHAR(255) NOT NULL COMMENT '教材名称',
    `title_en` VARCHAR(255) DEFAULT NULL COMMENT '教材英文名称',
    `summary` TEXT DEFAULT NULL COMMENT '教材简介',
    `material_type` VARCHAR(50) NOT NULL COMMENT 'textbook、dialogue、note_collection、card_set、phonics、exam 等',
    `publisher` VARCHAR(200) DEFAULT NULL COMMENT '出版社、来源或作者',
    `version_name` VARCHAR(100) DEFAULT NULL COMMENT '版本、册别或级别',
    `cover_url` VARCHAR(500) DEFAULT NULL COMMENT '教材封面',
    `difficulty_code` VARCHAR(50) DEFAULT NULL COMMENT '难度编码',
    `estimated_minutes` INT UNSIGNED DEFAULT NULL COMMENT '整本教材预计学习分钟数',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '专题内排序',
    `is_published` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否对学习者可见',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_material_topic_code` (`topic_id`, `material_code`),
    KEY `idx_learning_material_topic_published_order` (`topic_id`, `is_published`, `sort_order`),
    CONSTRAINT `fk_learning_material_topic`
        FOREIGN KEY (`topic_id`) REFERENCES `learning_topic` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_learning_material_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_material_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习教材表';

CREATE TABLE IF NOT EXISTS `learning_material_lesson` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '教材课时主键ID',
    `material_id` BIGINT UNSIGNED NOT NULL COMMENT '所属教材ID',
    `lesson_code` VARCHAR(120) NOT NULL COMMENT '教材内稳定课时编码',
    `title` VARCHAR(255) NOT NULL COMMENT '课时标题',
    `title_en` VARCHAR(255) DEFAULT NULL COMMENT '课时英文标题',
    `summary` TEXT DEFAULT NULL COMMENT '课时简介',
    `source_resource` VARCHAR(80) DEFAULT NULL COMMENT '内容资源编码，例如 textbook、notes、dialogues',
    `source_reference_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '内容根记录ID',
    `content_json` LONGTEXT DEFAULT NULL COMMENT '无旧内容表时的自包含课时内容 JSON',
    `estimated_minutes` SMALLINT UNSIGNED DEFAULT NULL COMMENT '预计学习分钟数',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '教材内排序',
    `is_published` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否对学习者可见',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_material_lesson_code` (`material_id`, `lesson_code`),
    KEY `idx_learning_material_lesson_material_published_order`
        (`material_id`, `is_published`, `sort_order`),
    KEY `idx_learning_material_lesson_source` (`source_resource`, `source_reference_id`),
    CONSTRAINT `fk_learning_material_lesson_material`
        FOREIGN KEY (`material_id`) REFERENCES `learning_material` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_material_lesson_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_learning_material_lesson_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教材课时表';

-- Existing courses retain their direct content fields for compatibility.
-- material_id is retained as the first linked material for older clients;
-- new course-to-material writes use learning_course_material below.
SET @has_learning_course_material_id = (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_course'
      AND column_name = 'material_id'
);
SET @add_learning_course_material_id = IF(
    @has_learning_course_material_id = 0,
    'ALTER TABLE `learning_course` ADD COLUMN `material_id` BIGINT UNSIGNED DEFAULT NULL COMMENT ''课程关联的整本教材ID'' AFTER `topic_id`',
    'SELECT 1'
);
PREPARE add_learning_course_material_id FROM @add_learning_course_material_id;
EXECUTE add_learning_course_material_id;
DEALLOCATE PREPARE add_learning_course_material_id;

SET @has_learning_course_access_policy = (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_course'
      AND column_name = 'access_policy'
);
SET @add_learning_course_access_policy = IF(
    @has_learning_course_access_policy = 0,
    'ALTER TABLE `learning_course` ADD COLUMN `access_policy` VARCHAR(20) NOT NULL DEFAULT ''free'' COMMENT ''free、benefit；benefit 表示必须拥有课程访问权益'' AFTER `is_published`',
    'SELECT 1'
);
PREPARE add_learning_course_access_policy FROM @add_learning_course_access_policy;
EXECUTE add_learning_course_access_policy;
DEALLOCATE PREPARE add_learning_course_access_policy;

SET @has_learning_course_material_index = (
    SELECT COUNT(*)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_course'
      AND index_name = 'idx_learning_course_material'
);
SET @add_learning_course_material_index = IF(
    @has_learning_course_material_index = 0,
    'ALTER TABLE `learning_course` ADD KEY `idx_learning_course_material` (`material_id`)',
    'SELECT 1'
);
PREPARE add_learning_course_material_index FROM @add_learning_course_material_index;
EXECUTE add_learning_course_material_index;
DEALLOCATE PREPARE add_learning_course_material_index;

SET @has_learning_course_access_index = (
    SELECT COUNT(*)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_course'
      AND index_name = 'idx_learning_course_access_published'
);
SET @add_learning_course_access_index = IF(
    @has_learning_course_access_index = 0,
    'ALTER TABLE `learning_course` ADD KEY `idx_learning_course_access_published` (`access_policy`, `is_published`, `topic_id`)',
    'SELECT 1'
);
PREPARE add_learning_course_access_index FROM @add_learning_course_access_index;
EXECUTE add_learning_course_access_index;
DEALLOCATE PREPARE add_learning_course_access_index;

SET @has_learning_course_material_fk = (
    SELECT COUNT(*)
    FROM information_schema.table_constraints
    WHERE table_schema = DATABASE()
      AND table_name = 'learning_course'
      AND constraint_name = 'fk_learning_course_material'
      AND constraint_type = 'FOREIGN KEY'
);
SET @add_learning_course_material_fk = IF(
    @has_learning_course_material_fk = 0,
    'ALTER TABLE `learning_course` ADD CONSTRAINT `fk_learning_course_material` FOREIGN KEY (`material_id`) REFERENCES `learning_material` (`id`) ON DELETE RESTRICT',
    'SELECT 1'
);
PREPARE add_learning_course_material_fk FROM @add_learning_course_material_fk;
EXECUTE add_learning_course_material_fk;
DEALLOCATE PREPARE add_learning_course_material_fk;

-- A course can arrange several whole materials.  The mapping sort_order is
-- the learner-facing material sequence within that course.
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

-- Preserve every existing one-material course before the application starts
-- reading the mapping.  It is idempotent and does not overwrite a manually
-- adjusted mapping order on later runs.
INSERT INTO `learning_course_material`
    (`course_id`, `material_id`, `sort_order`, `created_by`, `updated_by`)
SELECT course.`id`, course.`material_id`, 10, course.`created_by`, course.`updated_by`
FROM `learning_course` course
WHERE course.`material_id` IS NOT NULL
ON DUPLICATE KEY UPDATE `course_id` = VALUES(`course_id`);

CREATE TABLE IF NOT EXISTS `membership_plan` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '会员等级主键ID',
    `plan_code` VARCHAR(64) NOT NULL COMMENT '稳定业务编码，例如 free、monthly、annual',
    `name` VARCHAR(100) NOT NULL COMMENT '会员名称',
    `name_en` VARCHAR(100) DEFAULT NULL COMMENT '会员英文名称',
    `description` VARCHAR(500) DEFAULT NULL COMMENT '会员说明',
    `tier_rank` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '等级优先级，数值越大等级越高',
    `billing_cycle` VARCHAR(20) NOT NULL DEFAULT 'manual' COMMENT 'free、manual、monthly、quarterly、yearly、lifetime',
    `duration_days` INT UNSIGNED DEFAULT NULL COMMENT '有效天数；终身会员为空',
    `price` DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '当前展示价格',
    `currency` CHAR(3) NOT NULL DEFAULT 'CNY' COMMENT '币种',
    `icon` VARCHAR(32) DEFAULT NULL COMMENT '展示图标',
    `badge_text` VARCHAR(50) DEFAULT NULL COMMENT '角标文案',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '列表排序，越小越靠前',
    `status` VARCHAR(20) NOT NULL DEFAULT 'draft' COMMENT 'draft、active、inactive、archived',
    `is_default` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否为默认会员',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_membership_plan_code` (`plan_code`),
    KEY `idx_membership_plan_status_sort` (`status`, `sort_order`),
    KEY `idx_membership_plan_rank` (`tier_rank`),
    CONSTRAINT `fk_membership_plan_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_membership_plan_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会员等级配置表';

CREATE TABLE IF NOT EXISTS `membership_benefit` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '权益主键ID',
    `benefit_code` VARCHAR(80) NOT NULL COMMENT '稳定业务编码',
    `name` VARCHAR(100) NOT NULL COMMENT '权益名称',
    `name_en` VARCHAR(100) DEFAULT NULL COMMENT '权益英文名称',
    `description` VARCHAR(500) DEFAULT NULL COMMENT '权益说明',
    `benefit_type` VARCHAR(30) NOT NULL COMMENT 'content_access、feature_access、quota、discount、service',
    `value_type` VARCHAR(20) NOT NULL COMMENT 'boolean、integer、decimal、string、json',
    `unit` VARCHAR(50) DEFAULT NULL COMMENT 'times/day、items/day、percent 等',
    `scope_json` LONGTEXT DEFAULT NULL COMMENT '适用范围 JSON',
    `default_value_json` LONGTEXT DEFAULT NULL COMMENT '默认权益值 JSON',
    `icon` VARCHAR(32) DEFAULT NULL COMMENT '展示图标',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '列表排序，越小越靠前',
    `status` VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT 'active、inactive、archived',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_membership_benefit_code` (`benefit_code`),
    KEY `idx_membership_benefit_status_sort` (`status`, `sort_order`),
    KEY `idx_membership_benefit_type` (`benefit_type`),
    CONSTRAINT `fk_membership_benefit_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_membership_benefit_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会员权益配置表';

CREATE TABLE IF NOT EXISTS `membership_plan_benefit` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '会员权益映射主键ID',
    `membership_plan_id` BIGINT UNSIGNED NOT NULL COMMENT '会员等级ID',
    `benefit_id` BIGINT UNSIGNED NOT NULL COMMENT '权益ID',
    `grant_value_json` LONGTEXT DEFAULT NULL COMMENT '该会员下的权益值 JSON；为空时使用默认权益值',
    `is_enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否对该会员生效',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '会员详情页展示排序',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_membership_plan_benefit` (`membership_plan_id`, `benefit_id`),
    KEY `idx_membership_plan_benefit_enabled_sort`
        (`membership_plan_id`, `is_enabled`, `sort_order`),
    KEY `idx_membership_plan_benefit_benefit` (`benefit_id`),
    CONSTRAINT `fk_membership_plan_benefit_plan`
        FOREIGN KEY (`membership_plan_id`) REFERENCES `membership_plan` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_membership_plan_benefit_benefit`
        FOREIGN KEY (`benefit_id`) REFERENCES `membership_benefit` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_membership_plan_benefit_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_membership_plan_benefit_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会员等级与权益映射表';

CREATE TABLE IF NOT EXISTS `user_membership` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户会员记录主键ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `membership_plan_id` BIGINT UNSIGNED NOT NULL COMMENT '会员等级ID',
    `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT 'pending、active、expired、cancelled、revoked',
    `source` VARCHAR(30) NOT NULL DEFAULT 'manual' COMMENT 'manual、purchase、trial、gift、migration、signup',
    `starts_at` DATETIME NOT NULL COMMENT '生效时间',
    `ends_at` DATETIME DEFAULT NULL COMMENT '到期时间；终身会员为空',
    `auto_renew` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否自动续费',
    `external_reference` VARCHAR(100) DEFAULT NULL COMMENT '支付单号或外部发放编号',
    `granted_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '发放管理员ID',
    `cancelled_at` DATETIME DEFAULT NULL COMMENT '取消时间',
    `cancel_reason` VARCHAR(500) DEFAULT NULL COMMENT '取消或撤销原因',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_membership_external_reference` (`external_reference`),
    KEY `idx_user_membership_user_status_time` (`user_id`, `status`, `starts_at`, `ends_at`),
    KEY `idx_user_membership_expiry` (`status`, `ends_at`),
    KEY `idx_user_membership_plan` (`membership_plan_id`),
    CONSTRAINT `fk_user_membership_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_membership_plan`
        FOREIGN KEY (`membership_plan_id`) REFERENCES `membership_plan` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_user_membership_granted_by`
        FOREIGN KEY (`granted_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户实际会员记录表';

CREATE TABLE IF NOT EXISTS `membership_benefit_course` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '权益课程映射主键ID',
    `benefit_id` BIGINT UNSIGNED NOT NULL COMMENT '权益ID',
    `course_id` BIGINT UNSIGNED NOT NULL COMMENT '课程ID',
    `access_action` VARCHAR(20) NOT NULL DEFAULT 'study' COMMENT 'study、download',
    `is_enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否生效',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '权益详情中的展示排序',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_membership_benefit_course_action` (`benefit_id`, `course_id`, `access_action`),
    KEY `idx_membership_benefit_course_course_enabled` (`course_id`, `is_enabled`),
    CONSTRAINT `fk_membership_benefit_course_benefit`
        FOREIGN KEY (`benefit_id`) REFERENCES `membership_benefit` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_membership_benefit_course_course`
        FOREIGN KEY (`course_id`) REFERENCES `learning_course` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_membership_benefit_course_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_membership_benefit_course_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会员权益与课程访问映射表';

CREATE TABLE IF NOT EXISTS `learning_user_course` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户课程主键ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `course_id` BIGINT UNSIGNED NOT NULL COMMENT '课程ID',
    `source` VARCHAR(30) NOT NULL DEFAULT 'self_added' COMMENT 'self_added、membership、purchase、gift、admin',
    `source_membership_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '首次加入时对应的用户会员记录ID，仅作来源审计',
    `status` VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT 'active、archived',
    `enrolled_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '加入我的课程时间',
    `last_opened_at` DATETIME DEFAULT NULL COMMENT '最近打开时间',
    `archived_at` DATETIME DEFAULT NULL COMMENT '归档时间',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_user_course` (`user_id`, `course_id`),
    KEY `idx_learning_user_course_user_status_opened` (`user_id`, `status`, `last_opened_at`),
    KEY `idx_learning_user_course_course` (`course_id`),
    CONSTRAINT `fk_learning_user_course_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_learning_user_course_course`
        FOREIGN KEY (`course_id`) REFERENCES `learning_course` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_learning_user_course_source_membership`
        FOREIGN KEY (`source_membership_id`) REFERENCES `user_membership` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户我的课程表';

-- Post-deployment check. All eight new tables should be present.
SELECT `table_name`
FROM information_schema.tables
WHERE table_schema = DATABASE()
  AND table_name IN (
      'learning_material',
      'learning_material_lesson',
      'membership_plan',
      'membership_benefit',
      'membership_plan_benefit',
      'user_membership',
      'membership_benefit_course',
      'learning_user_course'
  )
ORDER BY `table_name`;
