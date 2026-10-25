-- Server-authored app-shell contract and privacy-preserving analytics.
--
-- This migration is additive: existing Android API tables, routes, and data
-- stay untouched.  Deploy this migration before deploying the application
-- code that exposes /learning/app/bootstrap and /analytics/events:batch.

START TRANSACTION;

CREATE TABLE IF NOT EXISTS `app_presentation_config` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `target_type` VARCHAR(32) NOT NULL COMMENT 'module, topic, course, material, collection or placement',
    `target_key` VARCHAR(120) NOT NULL COMMENT 'stable public code, not a numeric primary key',
    `platform` VARCHAR(20) NOT NULL DEFAULT 'all' COMMENT 'all, android, ios, web or mini',
    `layout_code` VARCHAR(80) NOT NULL COMMENT 'registered client layout renderer',
    `presentation_json` TEXT NOT NULL COMMENT 'versioned display configuration JSON',
    `min_app_version` VARCHAR(40) DEFAULT NULL,
    `fallback_action_json` TEXT DEFAULT NULL COMMENT 'typed fallback action JSON',
    `status` VARCHAR(20) NOT NULL DEFAULT 'active',
    `sort_order` INT NOT NULL DEFAULT 0,
    `created_by` BIGINT UNSIGNED DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT UNSIGNED DEFAULT NULL,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_app_presentation_target` (`target_type`, `target_key`, `platform`),
    KEY `idx_app_presentation_active_target` (`status`, `target_type`, `target_key`, `platform`),
    CONSTRAINT `fk_app_presentation_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_app_presentation_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='App 首页、专题和集合的可发布展示配置';

CREATE TABLE IF NOT EXISTS `analytics_event_definition` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `event_name` VARCHAR(80) NOT NULL,
    `description` VARCHAR(500) DEFAULT NULL,
    `allowed_properties_json` TEXT NOT NULL COMMENT '允许上报的标量属性名',
    `sample_rate` INT NOT NULL DEFAULT 100,
    `status` VARCHAR(20) NOT NULL DEFAULT 'active',
    `created_by` BIGINT UNSIGNED DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT UNSIGNED DEFAULT NULL,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_analytics_event_definition_name` (`event_name`),
    KEY `idx_analytics_event_definition_status` (`status`, `event_name`),
    CONSTRAINT `fk_analytics_definition_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_analytics_definition_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='客户端埋点事件字典';

CREATE TABLE IF NOT EXISTS `analytics_event` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `event_id` VARCHAR(64) NOT NULL COMMENT '客户端生成的 UUID，用于幂等去重',
    `user_id` BIGINT UNSIGNED NOT NULL,
    `event_name` VARCHAR(80) NOT NULL,
    `occurred_at` DATETIME NOT NULL,
    `session_id` VARCHAR(120) DEFAULT NULL,
    `subject_type` VARCHAR(50) DEFAULT NULL,
    `subject_key` VARCHAR(500) DEFAULT NULL,
    `source_screen` VARCHAR(80) DEFAULT NULL,
    `source_placement` VARCHAR(120) DEFAULT NULL,
    `source_item_key` VARCHAR(500) DEFAULT NULL,
    `properties_json` TEXT NOT NULL COMMENT '受事件字典约束的标量属性 JSON',
    `context_json` TEXT NOT NULL COMMENT '平台、版本、配置 revision 和渲染器 JSON',
    `received_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_analytics_event_event_id` (`event_id`),
    KEY `idx_analytics_event_user_occurred` (`user_id`, `occurred_at`),
    KEY `idx_analytics_event_name_occurred` (`event_name`, `occurred_at`),
    CONSTRAINT `fk_analytics_event_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='去标识化学习和产品行为事件';

-- Android already ships renderers for the built-in template set.  This only
-- fixes the declared contract; it does not alter lesson content or access.
UPDATE `learning_template`
SET `supported_clients_json` = CASE
    WHEN `supported_clients_json` IS NULL OR TRIM(`supported_clients_json`) = ''
        THEN '["web","mini","android"]'
    WHEN JSON_VALID(`supported_clients_json`) = 1
         AND JSON_CONTAINS(`supported_clients_json`, JSON_QUOTE('android')) = 0
        THEN JSON_ARRAY_APPEND(`supported_clients_json`, '$', 'android')
    ELSE `supported_clients_json`
END
WHERE `template_code` IN (
    'standard', 'put-aside', 'dialogue', 'commute', 'textbook', 'cards',
    'phonics', 'interview', 'mind-map'
);

COMMIT;
