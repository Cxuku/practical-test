-- Run this once to create the customers table
CREATE TABLE IF NOT EXISTS customers (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Optional: seed data for testing
INSERT IGNORE INTO customers (name, email) VALUES
    ('Alice Dlamini',  'alice@example.com'),
    ('Bob Mokoena',    'bob@example.com'),
    ('Carol Nkosi',    'carol@example.com');
