CREATE DATABASE IF NOT EXISTS wedding_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE wedding_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  phone VARCHAR(20),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS templates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  style VARCHAR(50),
  preview_url TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invitations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  template_id INT,
  groom_name VARCHAR(100),
  groom_email VARCHAR(150),
  groom_phone VARCHAR(20),
  bride_name VARCHAR(100),
  bride_email VARCHAR(150),
  bride_phone VARCHAR(20),
  event_date DATE,
  event_location VARCHAR(255),
  custom_message TEXT,
  pdf_path TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS guests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  invitation_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150),
  phone VARCHAR(20),
  is_sent BOOLEAN DEFAULT FALSE,
  responded BOOLEAN DEFAULT FALSE,
  responded_at DATETIME,
  FOREIGN KEY (invitation_id) REFERENCES invitations(id) ON DELETE CASCADE
);
