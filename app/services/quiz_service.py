"""
QuizSense AI - Quiz Service
Handles quiz storage, retrieval, and scoring
"""

import json
import secrets
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from app.database.connection import get_database


class QuizService:
    """Service for managing quizzes"""
    
    
    async def save_quiz(
        self,
        quiz_id: str,
        user_id: str,
        subject: str,
        topic: str,
        difficulty: str,
        questions: List[Dict],
        created_at: datetime
    ) -> bool:
        """Save a generated quiz to database"""
        
        db = await get_database()
        
        try:
            await db.execute(
                """
                INSERT INTO quizzes (id, user_id, subject, topic, difficulty, questions, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    quiz_id,
                    user_id,
                    subject,
                    topic,
                    difficulty,
                    json.dumps(questions),
                    created_at.isoformat()
                )
            )
            await db.commit()
            return True
            
        except Exception as e:
            print(f"Error saving quiz: {e}")
            return False
    
    
    async def get_quiz(self, quiz_id: str) -> Optional[Dict]:
        """Get quiz by ID"""
        
        db = await get_database()
        
        async with db.execute(
            """
            SELECT id, user_id, subject, topic, difficulty, questions, 
                   created_at, is_completed, score
            FROM quizzes WHERE id = ?
            """,
            (quiz_id,)
        ) as cursor:
            row = await cursor.fetchone()
        
        if not row:
            return None
        
        return {
            "id": row[0],
            "user_id": row[1],
            "subject": row[2],
            "topic": row[3],
            "difficulty": row[4],
            "questions": json.loads(row[5]),
            "created_at": row[6],
            "is_completed": bool(row[7]),
            "score": row[8]
        }
    
    
    async def get_previous_questions(
        self,
        user_id: str,
        topic: str,
        limit: int = 50
    ) -> List[str]:
        """Get previously asked question IDs for a topic"""
        
        db = await get_database()
        
        async with db.execute(
            """
            SELECT questions FROM quizzes 
            WHERE user_id = ? AND topic = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, topic, limit)
        ) as cursor:
            rows = await cursor.fetchall()
        
        question_ids = []
        for row in rows:
            questions = json.loads(row[0])
            for q in questions:
                question_ids.append(q.get("q_id", ""))
        
        return question_ids
    
    
    async def save_attempt(
        self,
        quiz_id: str,
        user_id: str,
        answers: List,
        score: int,
        total: int,
        time_taken: int,
        topic_breakdown: Dict,
        completed_at: datetime
    ) -> bool:
        """Save quiz attempt to database"""
        
        db = await get_database()
        
        try:
            attempt_id = f"attempt_{quiz_id}"
            
            await db.execute(
                """
                INSERT INTO quiz_attempts 
                (id, quiz_id, user_id, answers, score, total, time_taken, topic_breakdown, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    attempt_id,
                    quiz_id,
                    user_id,
                    json.dumps([a.dict() for a in answers]),
                    score,
                    total,
                    time_taken,
                    json.dumps(topic_breakdown),
                    completed_at.isoformat()
                )
            )
            
            # Mark quiz as completed
            await db.execute(
                """
                UPDATE quizzes SET is_completed = 1, score = ? WHERE id = ?
                """,
                (score, quiz_id)
            )
            
            # Update topic performance
            await self._update_topic_performance(user_id, topic_breakdown)
            
            await db.commit()
            return True
            
        except Exception as e:
            print(f"Error saving attempt: {e}")
            return False
    
    
    async def _update_topic_performance(
        self,
        user_id: str,
        topic_breakdown: Dict
    ):
        """Update topic-wise performance tracking"""
        
        db = await get_database()
        
        for topic, data in topic_breakdown.items():
            
            # Check if topic record exists
            async with db.execute(
                "SELECT id, total_questions, correct_answers FROM topic_performance WHERE user_id = ? AND topic = ?",
                (user_id, topic)
            ) as cursor:
                existing = await cursor.fetchone()
            
            if existing:
                # Update existing record
                new_total = existing[1] + data["total"]
                new_correct = existing[2] + data["correct"]
                accuracy = (new_correct / new_total * 100) if new_total > 0 else 0
                
                await db.execute(
                    """
                    UPDATE topic_performance 
                    SET total_questions = ?, correct_answers = ?, accuracy = ?, last_updated = ?
                    WHERE id = ?
                    """,
                    (new_total, new_correct, accuracy, datetime.utcnow().isoformat(), existing[0])
                )
            else:
                # Create new record
                record_id = f"tp_{secrets.token_hex(8)}"
                accuracy = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
                
                await db.execute(
                    """
                    INSERT INTO topic_performance 
                    (id, user_id, topic, total_questions, correct_answers, accuracy, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record_id,
                        user_id,
                        topic,
                        data["total"],
                        data["correct"],
                        accuracy,
                        datetime.utcnow().isoformat()
                    )
                )
    
    
    async def update_user_stats(self, user_id: str):
        """Update user statistics after quiz completion"""
        
        db = await get_database()
        
        # Get total quizzes
        async with db.execute(
            "SELECT COUNT(*) FROM quizzes WHERE user_id = ? AND is_completed = 1",
            (user_id,)
        ) as cursor:
            total_quizzes = (await cursor.fetchone())[0]
        
        # Calculate streak (simplified)
        async with db.execute(
            """
            SELECT DATE(completed_at) as quiz_date 
            FROM quiz_attempts 
            WHERE user_id = ? 
            ORDER BY completed_at DESC 
            LIMIT 30
            """,
            (user_id,)
        ) as cursor:
            dates = [row[0] for row in await cursor.fetchall()]
        
        streak = 1 if dates else 0
        
        # Update user
        await db.execute(
            """
            UPDATE users SET total_quizzes = ?, current_streak = ?, last_quiz_date = ?
            WHERE id = ?
            """,
            (total_quizzes, streak, datetime.utcnow().isoformat(), user_id)
        )
        await db.commit()
    
    
    async def get_user_history(
        self,
        user_id: str,
        days: int = 7,
        limit: int = 10
    ) -> List[Dict]:
        """Get user's quiz history"""
        
        db = await get_database()
        
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        async with db.execute(
            """
            SELECT q.id, q.subject, q.topic, q.difficulty, q.created_at, q.score,
                   a.total, a.time_taken, a.completed_at
            FROM quizzes q
            LEFT JOIN quiz_attempts a ON q.id = a.quiz_id
            WHERE q.user_id = ? AND q.created_at >= ?
            ORDER BY q.created_at DESC
            LIMIT ?
            """,
            (user_id, cutoff_date, limit)
        ) as cursor:
            rows = await cursor.fetchall()
        
        history = []
        for row in rows:
            score = row[5] or 0
            total = row[6] or 0
            percentage = (score / total * 100) if total > 0 else 0
            
            history.append({
                "quiz_id": row[0],
                "subject": row[1],
                "topic": row[2],
                "difficulty": row[3],
                "created_at": row[4],
                "score": score,
                "total": total,
                "percentage": round(percentage, 1),
                "time_taken": row[7] or 0,
                "completed_at": row[8]
            })
        
        return history