-- Exported user record for the HappyEnglish `user` table.
-- The password is stored as a bcrypt hash, matching the application format.
INSERT INTO `user`
    (username, password_hash, full_name, email, contact_number, home_address, role, status)
VALUES
    ('jingjing', '$2b$12$hxFeS4Rh0HPrJQESkV275.fnFUJxbE4MqX28v.JRSYtziHj7n3drm', 'jingjing', NULL, NULL, NULL, 'learner', 'active');
