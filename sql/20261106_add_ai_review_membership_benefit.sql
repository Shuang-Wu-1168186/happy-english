-- AI-selected review questions are a separately configurable membership
-- feature.  Every plan that already grants the platform-wide course benefit
-- receives it by default; administrators may later disable it per plan.

START TRANSACTION;

INSERT INTO `membership_benefit`
    (`benefit_code`, `name`, `name_en`, `description`, `benefit_type`, `value_type`,
     `scope_json`, `default_value_json`, `icon`, `sort_order`, `status`)
VALUES
    ('ai-review-generation', 'AI 智能复习出题', 'AI Review Generation',
     '根据近期学习内容智能选择复习题，并提供等价答案和简短解析。',
     'feature_access', 'boolean',
     '{"feature":"learning_review_ai"}', 'true', '✨', 20, 'active')
ON DUPLICATE KEY UPDATE
    `name` = VALUES(`name`),
    `name_en` = VALUES(`name_en`),
    `description` = VALUES(`description`),
    `benefit_type` = VALUES(`benefit_type`),
    `value_type` = VALUES(`value_type`),
    `scope_json` = VALUES(`scope_json`),
    `default_value_json` = VALUES(`default_value_json`),
    `icon` = VALUES(`icon`),
    `sort_order` = VALUES(`sort_order`),
    `status` = VALUES(`status`),
    `updated_at` = CURRENT_TIMESTAMP;

-- Preserve a plan owner's explicit configuration on reruns.  New mappings
-- inherit the enabled all-course plans, including the seven-day trial plan.
INSERT INTO `membership_plan_benefit`
    (`membership_plan_id`, `benefit_id`, `grant_value_json`, `is_enabled`, `sort_order`)
SELECT plan.`id`, ai_benefit.`id`, 'true', 1, 20
FROM `membership_plan` AS plan
JOIN `membership_plan_benefit` AS course_grant
  ON course_grant.`membership_plan_id` = plan.`id`
 AND course_grant.`is_enabled` = 1
JOIN `membership_benefit` AS course_benefit
  ON course_benefit.`id` = course_grant.`benefit_id`
 AND course_benefit.`benefit_code` = 'all-courses-access'
JOIN `membership_benefit` AS ai_benefit
  ON ai_benefit.`benefit_code` = 'ai-review-generation'
ON DUPLICATE KEY UPDATE
    `updated_at` = CURRENT_TIMESTAMP;

COMMIT;
