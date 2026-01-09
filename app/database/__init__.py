"""
QuizSense AI - Database Package
"""

from app.database.connection import get_database, init_database

__all__ = [
    "get_database",
    "init_database"
]