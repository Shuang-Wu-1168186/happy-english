-- Run this once on an existing Happy English MySQL database before deploying
-- the login monitoring feature.
CREATE TABLE IF NOT EXISTS `login_audit` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '登录审计记录主键ID',
    `user_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '成功登录的用户ID；未知账号登录失败时为空',
    `username` VARCHAR(100) NOT NULL COMMENT '登录时输入的用户名',
    `full_name` VARCHAR(100) DEFAULT NULL COMMENT '成功登录时的姓名快照',
    `login_ip` VARCHAR(45) DEFAULT NULL COMMENT 'IPv4 或 IPv6 登录地址',
    `user_agent` VARCHAR(1000) DEFAULT NULL COMMENT '浏览器 User-Agent',
    `success` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否登录成功：0-失败，1-成功',
    `logged_in_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登录尝试时间',

    PRIMARY KEY (`id`),
    KEY `idx_login_audit_logged_in_at` (`logged_in_at`),
    KEY `idx_login_audit_user_logged_in_at` (`user_id`, `logged_in_at`),
    KEY `idx_login_audit_ip_logged_in_at` (`login_ip`, `logged_in_at`),
    CONSTRAINT `fk_login_audit_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户登录审计记录';
