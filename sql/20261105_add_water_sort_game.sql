-- Additive migration; existing accounts, lessons and learning records are untouched.
CREATE TABLE IF NOT EXISTS game_water_sort_progress (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL UNIQUE,
    state_json MEDIUMTEXT NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS game_water_sort_attempt (
    id VARCHAR(36) NOT NULL PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    level_number INT NOT NULL,
    state_json MEDIUMTEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_game_water_sort_attempt_user (user_id, created_at),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
