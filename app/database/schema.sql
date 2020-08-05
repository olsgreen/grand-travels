DROP TABLE IF EXISTS `gps_data`;
CREATE TABLE `gps_data` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `latitude` DECIMAL(10,8) NOT NULL,
    `longitude` DECIMAL(11,8) NOT NULL,
    `heading` DECIMAl(3,2),
    `ground_speed` DECIMAL(3,2),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);