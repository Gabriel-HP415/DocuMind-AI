-- ============================================================
-- DocuMind AI - Database Schema (MySQL 8.x)
-- ============================================================

CREATE DATABASE IF NOT EXISTS documind_ai
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE documind_ai;

-- ============================================================
-- Table: users
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_users_email (email),
    INDEX idx_users_role (role),
    INDEX idx_users_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Table: pdf_documents
-- ============================================================
CREATE TABLE IF NOT EXISTS pdf_documents (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    file_name VARCHAR(512) NOT NULL,
    file_path VARCHAR(1024) NOT NULL,
    file_size BIGINT UNSIGNED DEFAULT 0,
    upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_pages INT UNSIGNED DEFAULT 0,
    is_indexed TINYINT(1) NOT NULL DEFAULT 0,
    faiss_index_path VARCHAR(1024) NULL,
    chunk_count INT UNSIGNED DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_pdf_documents_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_pdf_documents_user_id (user_id),
    INDEX idx_pdf_documents_upload_date (upload_date),
    INDEX idx_pdf_documents_is_indexed (is_indexed)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Table: chat_sessions
-- ============================================================
CREATE TABLE IF NOT EXISTS chat_sessions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    document_id BIGINT UNSIGNED NOT NULL,
    title VARCHAR(512) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_chat_sessions_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_chat_sessions_document
        FOREIGN KEY (document_id) REFERENCES pdf_documents(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_chat_sessions_user_id (user_id),
    INDEX idx_chat_sessions_document_id (document_id),
    INDEX idx_chat_sessions_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Table: chat_messages
-- ============================================================
CREATE TABLE IF NOT EXISTS chat_messages (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_id BIGINT UNSIGNED NOT NULL,
    sender ENUM('user', 'assistant', 'system') NOT NULL DEFAULT 'user',
    message TEXT NOT NULL,
    meta_json JSON NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_chat_messages_session
        FOREIGN KEY (session_id) REFERENCES chat_sessions(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_chat_messages_session_id (session_id),
    INDEX idx_chat_messages_created_at (created_at),
    FULLTEXT INDEX idx_chat_messages_message_fulltext (message)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Seed: tạo tài khoản admin mặc định
-- Mật khẩu: Admin@123 (đã hash bcrypt)
-- Hash được tạo từ passlib.context.bcrypt với cost 12
-- ============================================================
-- Lưu ý: Bạn cần chạy script seed sau khi tạo bảng:
--   python backend/scripts/seed_admin.py
-- hoặc đổi mật khẩu ngay sau lần đăng nhập đầu tiên.
