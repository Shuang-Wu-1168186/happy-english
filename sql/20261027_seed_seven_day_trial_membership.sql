-- Add a reusable seven-day trial membership with access to every course.
-- The existing all-courses-access benefit owns the course mappings, so this
-- plan automatically follows the platform-wide course entitlement setup.

START TRANSACTION;

INSERT INTO `membership_plan`
    (`plan_code`, `name`, `name_en`, `description`, `tier_rank`, `billing_cycle`,
     `duration_days`, `price`, `currency`, `icon`, `badge_text`, `sort_order`,
     `status`, `is_default`)
VALUES
    ('seven-day-trial', '7天体验会员', '7-Day Trial Membership',
     '开通后 7 天内可访问平台全部教材。', 5, 'free', 7, 0.00, 'CNY',
     '🎁', '7天体验', 5, 'active', 0)
ON DUPLICATE KEY UPDATE
    `name` = VALUES(`name`),
    `name_en` = VALUES(`name_en`),
    `description` = VALUES(`description`),
    `tier_rank` = VALUES(`tier_rank`),
    `billing_cycle` = VALUES(`billing_cycle`),
    `duration_days` = VALUES(`duration_days`),
    `price` = VALUES(`price`),
    `currency` = VALUES(`currency`),
    `icon` = VALUES(`icon`),
    `badge_text` = VALUES(`badge_text`),
    `sort_order` = VALUES(`sort_order`),
    `status` = VALUES(`status`),
    `is_default` = VALUES(`is_default`),
    `updated_at` = CURRENT_TIMESTAMP;

INSERT INTO `membership_plan_benefit`
    (`membership_plan_id`, `benefit_id`, `grant_value_json`, `is_enabled`, `sort_order`)
SELECT plan.`id`, benefit.`id`, NULL, 1, 10
FROM `membership_plan` AS plan
JOIN `membership_benefit` AS benefit
  ON benefit.`benefit_code` = 'all-courses-access'
WHERE plan.`plan_code` = 'seven-day-trial'
ON DUPLICATE KEY UPDATE
    `grant_value_json` = VALUES(`grant_value_json`),
    `is_enabled` = VALUES(`is_enabled`),
    `sort_order` = VALUES(`sort_order`),
    `updated_at` = CURRENT_TIMESTAMP;

-- Keep the shared all-course entitlement complete for newly published
-- courses as well as the trial plan.
INSERT INTO `membership_benefit_course`
    (`benefit_id`, `course_id`, `access_action`, `is_enabled`, `sort_order`)
SELECT benefit.`id`, course.`id`, 'study', 1, course.`sort_order`
FROM `membership_benefit` AS benefit
CROSS JOIN `learning_course` AS course
WHERE benefit.`benefit_code` = 'all-courses-access'
ON DUPLICATE KEY UPDATE
    `is_enabled` = VALUES(`is_enabled`),
    `sort_order` = VALUES(`sort_order`),
    `updated_at` = CURRENT_TIMESTAMP;

COMMIT;

SELECT
    plan.`plan_code`,
    plan.`name`,
    plan.`duration_days`,
    plan.`status`,
    benefit.`benefit_code`
FROM `membership_plan` AS plan
JOIN `membership_plan_benefit` AS mapping
  ON mapping.`membership_plan_id` = plan.`id`
 AND mapping.`is_enabled` = 1
JOIN `membership_benefit` AS benefit
  ON benefit.`id` = mapping.`benefit_id`
WHERE plan.`plan_code` = 'seven-day-trial';
