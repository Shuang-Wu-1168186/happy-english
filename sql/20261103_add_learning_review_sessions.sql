-- Server-owned active-recall review sessions.
--
-- Answers are retained in learning_review_question and intentionally omitted
-- from the session payload until the learner submits an answer.

CREATE TABLE IF NOT EXISTS `learning_review_session` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '复习会话主键ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '学习用户ID',
    `source_window_days` INT UNSIGNED NOT NULL DEFAULT 7 COMMENT '本轮题目回看天数',
    `source_types_json` VARCHAR(80) NOT NULL DEFAULT '["notes","textbooks"]' COMMENT '本轮选择的来源类型JSON',
    `generator_provider` VARCHAR(50) NOT NULL DEFAULT 'deterministic' COMMENT '出题方式：deepseek 或 deterministic',
    `generator_model` VARCHAR(100) DEFAULT NULL COMMENT '本次出题使用的模型名称',
    `question_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '本轮实际题数',
    `completed_at` DATETIME DEFAULT NULL COMMENT '本轮完成时间',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    KEY `idx_learning_review_session_user_created` (`user_id`, `created_at`),
    CONSTRAINT `fk_learning_review_session_user`
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='用户主动回忆复习会话表';

CREATE TABLE IF NOT EXISTS `learning_review_question` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '复习题主键ID',
    `session_id` BIGINT UNSIGNED NOT NULL COMMENT '所属复习会话ID',
    `source_type` VARCHAR(50) NOT NULL COMMENT '来源类型，例如 english_note_item、material_lesson',
    `source_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '来源内容ID',
    `source_parent_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '来源父级ID，例如笔记或课程',
    `source_label` VARCHAR(255) NOT NULL COMMENT '仅用于学习者展示的来源标签',
    `source_locator` VARCHAR(255) DEFAULT NULL COMMENT '内容内例句定位符',
    `question_type` VARCHAR(50) NOT NULL DEFAULT 'translate_to_english',
    `answer_mode` VARCHAR(50) NOT NULL DEFAULT 'normalized_exact',
    `prompt` TEXT NOT NULL COMMENT '不包含标准答案的题干',
    `context_text` TEXT DEFAULT NULL,
    `reference_answer` TEXT NOT NULL COMMENT '提交后才返回的标准答案',
    `accepted_answers_json` TEXT NOT NULL COMMENT '服务端判题的可接受答案列表',
    `explanation` TEXT DEFAULT NULL,
    `question_order` INT UNSIGNED NOT NULL,
    `attempt_count` INT UNSIGNED NOT NULL DEFAULT 0,
    `submitted_answer` TEXT DEFAULT NULL,
    `is_correct` TINYINT(1) DEFAULT NULL,
    `answered_at` DATETIME DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_learning_review_question_session_order` (`session_id`, `question_order`),
    CONSTRAINT `fk_learning_review_question_session`
        FOREIGN KEY (`session_id`) REFERENCES `learning_review_session` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='用户复习会话题目与服务端判题状态表';
