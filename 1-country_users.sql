-- Write a SQL script that creates a table users following these requirements:
-- If the table already exists, your script should not fail
-- Your script can be executed on any database

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL
);
