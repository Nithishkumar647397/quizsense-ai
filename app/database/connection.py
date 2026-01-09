"""
QuizSense AI - Database Connection (Stable)
Ensures DB file is always in project root folder.
"""

import aiosqlite
from typing import Optional
from pathlib import Path

# Determine absolute path to quizsense-ai root
BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "quizsense.db"

_database: Optional[aiosqlite.Connection] = None


async def get_database() -> aiosqlite.Connection:
    global _database
    if _database is None:
        print(f"📁 Using database at: {DATABASE_PATH}")
        _database = await aiosqlite.connect(str(DATABASE_PATH))
        _database.row_factory = aiosqlite.Row
    return _database


async def close_database():
    global _database
    if _database is not None:
        await _database.close()
        _database = None


async def init_database():
    print("📦 Initializing database...")
    db = await get_database()
    await db.execute("""
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
        )
    """)
    await db.execute("""
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
        )
    """)
    await db.execute("""
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
        )
    """)
    await db.execute("""
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
        )
    """)
    await db.execute("""
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
        )
    """)
    await db.execute("CREATE INDEX IF NOT EXISTS idx_quizzes_user ON quizzes (user_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_attempts_user ON quiz_attempts (user_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_attempts_date ON quiz_attempts (completed_at)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_performance_user ON topic_performance (user_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_reports_user ON weekly_reports (user_id)")
    await db.commit()
    print("✅ Database initialized successfully!")