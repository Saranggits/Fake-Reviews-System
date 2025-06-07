CREATE DATABASE fake_review_db;
USE fake_review_db;

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    review_text TEXT,
    result VARCHAR(10)
);