DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER NOT NULL,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email)
);

INSERT INTO user (name, email, password_hash) VALUES
('John Doe', 'john@example.com', '$2b$12$pTADL.b5sL7i1u2Vq2eBReIUn2c5K2sP6bC2M1/SveKgo9E2g9pL.'),
('Jane Smith', 'jane@example.com', '$2b$12$w0JALDbG96eRjUCQ1hUv5uFvQ2U8T2U9Qx/J8c.S1c.K3l.F4a/G.');