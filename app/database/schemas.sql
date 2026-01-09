-- =============================================
-- QuizSense AI - Database Schema
-- =============================================
-- This file is for reference only.
-- Tables are created automatically by connection.py
-- =============================================

-- Users Table
-- Stores user account information
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    total_quizzes INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    last_quiz_date TEXT,
    is_active INTEGER DEFAULT 1
);

-- Quizzes Table
-- Stores generated quizzes
CREATE TABLE IF NOT EXISTS quizzes (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    questions TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_completed INTEGER DEFAULT 0,
    score INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Quiz Attempts Table
-- Stores user quiz submissions
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id TEXT PRIMARY KEY,
    quiz_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    answers TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    time_taken INTEGER DEFAULT 0,
    topic_breakdown TEXT,
    completed_at TEXT NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES quizzes (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Topic Performance Table
-- Tracks user performance per topic
CREATE TABLE IF NOT EXISTS topic_performance (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    total_questions INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    accuracy REAL DEFAULT 0,
    last_updated TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE (user_id, topic)
);

-- Weekly Reports Table
-- Stores generated weekly reports
CREATE TABLE IF NOT EXISTS weekly_reports (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    week_start TEXT NOT NULL,
    week_end TEXT NOT NULL,
    summary TEXT,
    overall_accuracy REAL,
    strong_topics TEXT,
    weak_topics TEXT,
    focus_topics TEXT,
    full_report TEXT,
    generated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- =============================================
-- Indexes for better performance
-- =============================================

CREATE INDEX IF NOT EXISTS idx_quizzes_user ON quizzes (user_id);
CREATE INDEX IF NOT EXISTS idx_attempts_user ON quiz_attempts (user_id);
CREATE INDEX IF NOT EXISTS idx_attempts_date ON quiz_attempts (completed_at);
CREATE INDEX IF NOT EXISTS idx_performance_user ON topic_performance (user_id);
CREATE INDEX IF NOT EXISTS idx_reports_user ON weekly_reports (user_id);

-- =============================================
-- Sample Queries (for reference)
-- =============================================

-- Get user's recent quizzes
-- SELECT * FROM quizzes WHERE user_id = ? ORDER BY created_at DESC LIMIT 10;

-- Get user's topic performance
-- SELECT * FROM topic_performance WHERE user_id = ? ORDER BY accuracy ASC;

-- Get user's weak topics (accuracy < 60%)
-- SELECT topic, accuracy FROM topic_performance WHERE user_id = ? AND accuracy < 60;

-- Get weekly quiz count
-- SELECT COUNT(*) FROM quiz_attempts WHERE user_id = ? AND completed_at >= date('now', '-7 days');