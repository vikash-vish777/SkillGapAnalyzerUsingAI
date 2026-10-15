-- Skill Gap Analyzer Using Artificial Intelligence (AI)
-- Database: MySQL 8.0 DDL Schema Specification

CREATE DATABASE IF NOT EXISTS `skill_gap_db`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `skill_gap_db`;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS `users` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `full_name` VARCHAR(120) NOT NULL,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Job Roles Table
CREATE TABLE IF NOT EXISTS `job_roles` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(150) NOT NULL UNIQUE,
  `description` TEXT NULL,
  `category` VARCHAR(100) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_job_roles_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Skills Master Catalog Table
CREATE TABLE IF NOT EXISTS `skills` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL UNIQUE,
  `normalized_name` VARCHAR(100) NOT NULL UNIQUE,
  `category` VARCHAR(80) NOT NULL,
  `description` TEXT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_skills_normalized` (`normalized_name`),
  INDEX `idx_skills_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Job Required Skills Associative Table
CREATE TABLE IF NOT EXISTS `job_required_skills` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `job_role_id` BIGINT NOT NULL,
  `skill_id` BIGINT NOT NULL,
  `importance_weight` DECIMAL(3, 2) NOT NULL DEFAULT 1.00,
  `requirement_type` ENUM('essential', 'preferred') NOT NULL DEFAULT 'essential',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_jrs_job_role` FOREIGN KEY (`job_role_id`) REFERENCES `job_roles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_jrs_skill` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE,
  CONSTRAINT `uq_job_role_skill` UNIQUE (`job_role_id`, `skill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Resumes Metadata Table
CREATE TABLE IF NOT EXISTS `resumes` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `user_id` BIGINT NOT NULL,
  `original_filename` VARCHAR(255) NOT NULL,
  `file_type` VARCHAR(20) NOT NULL,
  `processing_status` ENUM('pending', 'completed', 'failed') NOT NULL DEFAULT 'completed',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_resumes_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  INDEX `idx_resumes_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Analyses Historical Table
CREATE TABLE IF NOT EXISTS `analyses` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `user_id` BIGINT NOT NULL,
  `resume_id` BIGINT NULL,
  `job_role_id` BIGINT NOT NULL,
  `match_percentage` DECIMAL(5, 2) NOT NULL,
  `weighted_match_percentage` DECIMAL(5, 2) NOT NULL,
  `analysis_status` ENUM('completed', 'failed', 'archived') NOT NULL DEFAULT 'completed',
  `algorithm_version` VARCHAR(20) NOT NULL DEFAULT 'v1.0',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_analyses_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_analyses_resume` FOREIGN KEY (`resume_id`) REFERENCES `resumes` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_analyses_job_role` FOREIGN KEY (`job_role_id`) REFERENCES `job_roles` (`id`) ON DELETE RESTRICT,
  INDEX `idx_analyses_user_date` (`user_id`, `created_at` DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Analysis Skills Granular Table
CREATE TABLE IF NOT EXISTS `analysis_skills` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `analysis_id` BIGINT NOT NULL,
  `skill_id` BIGINT NOT NULL,
  `match_status` ENUM('matched', 'missing', 'additional') NOT NULL,
  `importance_weight` DECIMAL(3, 2) NOT NULL DEFAULT 1.00,
  `evidence` TEXT NULL,
  `confidence_score` DECIMAL(4, 3) NOT NULL DEFAULT 1.000,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_as_analysis` FOREIGN KEY (`analysis_id`) REFERENCES `analyses` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_as_skill` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE RESTRICT,
  INDEX `idx_as_analysis_status` (`analysis_id`, `match_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Learning Resources Table
CREATE TABLE IF NOT EXISTS `learning_resources` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `skill_id` BIGINT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NULL,
  `resource_url` VARCHAR(500) NOT NULL,
  `resource_type` ENUM('documentation', 'course', 'tutorial', 'book', 'project') NOT NULL,
  `difficulty_level` ENUM('beginner', 'intermediate', 'advanced') NOT NULL DEFAULT 'beginner',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_lr_skill` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE,
  INDEX `idx_lr_skill` (`skill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Recommendations Table
CREATE TABLE IF NOT EXISTS `recommendations` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `analysis_id` BIGINT NOT NULL,
  `skill_id` BIGINT NOT NULL,
  `priority` INT NOT NULL DEFAULT 1,
  `recommendation_text` TEXT NOT NULL,
  `completion_status` ENUM('pending', 'in_progress', 'completed') NOT NULL DEFAULT 'pending',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_rec_analysis` FOREIGN KEY (`analysis_id`) REFERENCES `analyses` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_rec_skill` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE RESTRICT,
  INDEX `idx_rec_analysis` (`analysis_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
