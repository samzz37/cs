-- Certificate Management System Database Schema
-- Database: CS

CREATE DATABASE IF NOT EXISTS CS;
USE CS;

-- Users Table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff', 'student') DEFAULT 'student',
    department VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX (role),
    INDEX (email)
);

-- Templates Table
CREATE TABLE templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by INT NOT NULL,
    orientation ENUM('portrait', 'landscape') DEFAULT 'landscape',
    width DECIMAL(10, 2),
    height DECIMAL(10, 2),
    background_image LONGBLOB,
    background_filename VARCHAR(255),
    template_json LONGTEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX (created_by)
);

-- Certificates Table
CREATE TABLE certificates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    certificate_number VARCHAR(50) UNIQUE NOT NULL,
    template_id INT NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    student_id VARCHAR(100),
    student_email VARCHAR(255),
    department VARCHAR(255),
    course VARCHAR(255),
    marks DECIMAL(10, 2),
    grade VARCHAR(10),
    achievement_title VARCHAR(255),
    issue_date DATE,
    expiry_date DATE,
    qr_code VARCHAR(500),
    certificate_path VARCHAR(500),
    certificate_data LONGBLOB,
    status ENUM('draft', 'generated', 'issued', 'downloaded') DEFAULT 'draft',
    generated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (template_id) REFERENCES templates(id),
    FOREIGN KEY (generated_by) REFERENCES users(id),
    INDEX (student_email),
    INDEX (status),
    INDEX (created_at)
);

-- Rankings Table
CREATE TABLE rankings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    student_name VARCHAR(255) NOT NULL,
    student_email VARCHAR(255),
    department VARCHAR(255),
    event VARCHAR(255),
    academic_year VARCHAR(10),
    marks DECIMAL(10, 2) NOT NULL,
    rank_position INT,
    grade VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX (marks),
    INDEX (rank_position),
    INDEX (department),
    INDEX (event),
    INDEX (academic_year)
);

-- Activity Logs Table
CREATE TABLE activity_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    module VARCHAR(100),
    description TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    status ENUM('success', 'failure', 'warning') DEFAULT 'success',
    affected_record VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX (user_id),
    INDEX (created_at),
    INDEX (action)
);

-- System Logs Table
CREATE TABLE system_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    log_level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') DEFAULT 'INFO',
    module VARCHAR(100),
    message TEXT NOT NULL,
    error_details LONGTEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (log_level),
    INDEX (timestamp),
    INDEX (module)
);

-- Alerts Table
CREATE TABLE alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    alert_type ENUM('error', 'warning', 'info', 'success') DEFAULT 'warning',
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    phone_numbers VARCHAR(500),
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (alert_type),
    INDEX (created_at)
);

-- Settings Table
CREATE TABLE settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value LONGTEXT,
    description TEXT,
    data_type ENUM('string', 'integer', 'boolean', 'json') DEFAULT 'string',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Online Users Table (for real-time monitoring)
CREATE TABLE online_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    current_page VARCHAR(500),
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX (user_id),
    INDEX (login_time)
);

-- Bulk Upload Jobs Table
CREATE TABLE bulk_upload_jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    job_id VARCHAR(100) UNIQUE NOT NULL,
    uploaded_by INT NOT NULL,
    template_id INT NOT NULL,
    file_name VARCHAR(255),
    total_records INT,
    processed_records INT,
    successful_records INT,
    failed_records INT,
    status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    error_message LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    FOREIGN KEY (template_id) REFERENCES templates(id),
    INDEX (status),
    INDEX (created_at)
);

-- Create default settings
INSERT INTO settings (setting_key, setting_value, description, data_type) VALUES
('sms_alert_numbers', '[]', 'Phone numbers for SMS alerts', 'json'),
('theme_mode', 'light', 'Application theme (light/dark)', 'string'),
('default_template_id', '1', 'Default certificate template', 'integer'),
('enable_sms_alerts', 'true', 'Enable/disable SMS alerts', 'boolean'),
('max_upload_size_mb', '100', 'Maximum file upload size', 'integer'),
('session_timeout_minutes', '30', 'Session timeout in minutes', 'integer'),
('certificate_expiry_days', '365', 'Certificate expiry period in days', 'integer');

-- Additional performance indexes
CREATE INDEX idx_rankings_email ON rankings(student_email);
CREATE INDEX idx_online_users_session ON online_users(session_id);
