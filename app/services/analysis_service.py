"""
QuizSense AI - Analysis Service
Handles performance analysis and report generation
"""

import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta, date

from app.database.connection import get_database
from app.config import settings


class AnalysisService:
    """Service for analyzing user performance"""
    
    
    async def get_weekly_performance(self, user_id: str) -> Optional[Dict]:
        """Get performance data for the last 7 days"""
        
        db = await get_database()
        cutoff_date = (datetime.utcnow() - timedelta(days=7)).isoformat()
        
        # Get quiz attempts
        async with db.execute(
            """
            SELECT a.score, a.total, a.topic_breakdown, a.completed_at
            FROM quiz_attempts a
            WHERE a.user_id = ? AND a.completed_at >= ?
            ORDER BY a.completed_at DESC
            """,
            (user_id, cutoff_date)
        ) as cursor:
            attempts = await cursor.fetchall()
        
        if not attempts:
            return None
        
        # Calculate overall stats
        total_score = 0
        total_questions = 0
        topics = {}
        
        for attempt in attempts:
            total_score += attempt[0]
            total_questions += attempt[1]
            
            breakdown = json.loads(attempt[2]) if attempt[2] else {}
            for topic, data in breakdown.items():
                if topic not in topics:
                    topics[topic] = {"correct": 0, "total": 0}
                topics[topic]["correct"] += data["correct"]
                topics[topic]["total"] += data["total"]
        
        overall_accuracy = (total_score / total_questions * 100) if total_questions > 0 else 0
        
        # Calculate topic accuracies
        topic_accuracies = {}
        for topic, data in topics.items():
            acc = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
            topic_accuracies[topic] = round(acc, 1)
        
        # Identify weak and strong topics
        weak_topics = [t for t, a in topic_accuracies.items() if a < settings.WEAK_TOPIC_THRESHOLD * 100]
        strong_topics = [t for t, a in topic_accuracies.items() if a >= settings.STRONG_TOPIC_THRESHOLD * 100]
        
        return {
            "total_quizzes": len(attempts),
            "total_questions": total_questions,
            "total_correct": total_score,
            "overall_accuracy": round(overall_accuracy, 1),
            "topics": topics,
            "topic_accuracies": topic_accuracies,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "period": "last_7_days"
        }
    
    
    async def get_performance(
        self,
        user_id: str,
        days: int = 7
    ) -> Optional[Dict]:
        """Get performance data for specified period"""
        
        db = await get_database()
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        # Get quiz attempts
        async with db.execute(
            """
            SELECT a.score, a.total, a.topic_breakdown, a.completed_at
            FROM quiz_attempts a
            WHERE a.user_id = ? AND a.completed_at >= ?
            """,
            (user_id, cutoff_date)
        ) as cursor:
            attempts = await cursor.fetchall()
        
        if not attempts:
            return None
        
        total_score = sum(a[0] for a in attempts)
        total_questions = sum(a[1] for a in attempts)
        overall_accuracy = (total_score / total_questions * 100) if total_questions > 0 else 0
        
        # Aggregate topics
        topics = {}
        for attempt in attempts:
            breakdown = json.loads(attempt[2]) if attempt[2] else {}
            for topic, data in breakdown.items():
                if topic not in topics:
                    topics[topic] = {"correct": 0, "total": 0}
                topics[topic]["correct"] += data["correct"]
                topics[topic]["total"] += data["total"]
        
        # Get user streak
        async with db.execute(
            "SELECT current_streak FROM users WHERE id = ?",
            (user_id,)
        ) as cursor:
            user_row = await cursor.fetchone()
        
        current_streak = user_row[0] if user_row else 0
        
        return {
            "total_quizzes": len(attempts),
            "total_questions": total_questions,
            "overall_accuracy": round(overall_accuracy, 1),
            "topics": topics,
            "current_streak": current_streak,
            "best_streak": current_streak
        }
    
    
    async def get_dashboard_data(self, user_id: str) -> Dict:
        """Get data for dashboard display"""
        
        db = await get_database()
        
        # Get user info
        async with db.execute(
            "SELECT total_quizzes, current_streak FROM users WHERE id = ?",
            (user_id,)
        ) as cursor:
            user_row = await cursor.fetchone()
        
        total_quizzes = user_row[0] if user_row else 0
        current_streak = user_row[1] if user_row else 0
        
        # Get this week's quizzes
        week_start = (datetime.utcnow() - timedelta(days=7)).isoformat()
        
        async with db.execute(
            """
            SELECT a.score, a.total, DATE(a.completed_at) as quiz_date
            FROM quiz_attempts a
            WHERE a.user_id = ? AND a.completed_at >= ?
            ORDER BY a.completed_at
            """,
            (user_id, week_start)
        ) as cursor:
            week_attempts = await cursor.fetchall()
        
        # Calculate weekly accuracy by day
        daily_data = {}
        for attempt in week_attempts:
            quiz_date = attempt[2]
            if quiz_date not in daily_data:
                daily_data[quiz_date] = {"score": 0, "total": 0}
            daily_data[quiz_date]["score"] += attempt[0]
            daily_data[quiz_date]["total"] += attempt[1]
        
        weekly_accuracy = []
        for date_str, data in daily_data.items():
            acc = (data["score"] / data["total"] * 100) if data["total"] > 0 else 0
            weekly_accuracy.append({
                "date": date_str,
                "accuracy": round(acc, 1)
            })
        
        # Calculate overall accuracy
        total_score = sum(a[0] for a in week_attempts)
        total_questions = sum(a[1] for a in week_attempts)
        overall_accuracy = (total_score / total_questions * 100) if total_questions > 0 else 0
        
        # Get topic performance
        async with db.execute(
            """
            SELECT topic, accuracy FROM topic_performance
            WHERE user_id = ?
            ORDER BY accuracy ASC
            LIMIT 10
            """,
            (user_id,)
        ) as cursor:
            topic_rows = await cursor.fetchall()
        
        topic_performance = [
            {"topic": row[0], "accuracy": round(row[1], 1)}
            for row in topic_rows
        ]
        
        # Get recommended topics (weak ones)
        recommended_topics = [
            row[0] for row in topic_rows 
            if row[1] < settings.WEAK_TOPIC_THRESHOLD * 100
        ][:3]
        
        # Get recent quizzes
        async with db.execute(
            """
            SELECT q.topic, q.difficulty, a.score, a.total, a.completed_at
            FROM quizzes q
            JOIN quiz_attempts a ON q.id = a.quiz_id
            WHERE q.user_id = ?
            ORDER BY a.completed_at DESC
            LIMIT 5
            """,
            (user_id,)
        ) as cursor:
            recent_rows = await cursor.fetchall()
        
        recent_quizzes = [
            {
                "topic": row[0],
                "difficulty": row[1],
                "score": row[2],
                "total": row[3],
                "percentage": round(row[2] / row[3] * 100, 1) if row[3] > 0 else 0,
                "completed_at": row[4]
            }
            for row in recent_rows
        ]
        
        return {
            "total_quizzes": total_quizzes,
            "current_streak": current_streak,
            "overall_accuracy": round(overall_accuracy, 1),
            "quizzes_this_week": len(week_attempts),
            "weekly_accuracy": weekly_accuracy,
            "topic_performance": topic_performance,
            "recent_quizzes": recent_quizzes,
            "recommended_topics": recommended_topics
        }
    
    
    async def save_weekly_report(self, report) -> bool:
        """Save weekly report to database"""
        
        db = await get_database()
        
        try:
            await db.execute(
                """
                INSERT INTO weekly_reports 
                (id, user_id, week_start, week_end, summary, overall_accuracy,
                 strong_topics, weak_topics, focus_topics, full_report, generated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    report.report_id,
                    report.user_id,
                    report.week_start.isoformat(),
                    report.week_end.isoformat(),
                    report.summary,
                    report.overall_accuracy,
                    json.dumps(report.strong_topics),
                    json.dumps(report.weak_topics),
                    json.dumps(report.focus_topics),
                    report.full_report,
                    report.generated_at.isoformat()
                )
            )
            await db.commit()
            return True
            
        except Exception as e:
            print(f"Error saving report: {e}")
            return False
    
    
    async def get_report_history(
        self,
        user_id: str,
        limit: int = 4
    ) -> List[Dict]:
        """Get past weekly reports"""
        
        db = await get_database()
        
        async with db.execute(
            """
            SELECT id, week_start, week_end, summary, overall_accuracy, generated_at
            FROM weekly_reports
            WHERE user_id = ?
            ORDER BY generated_at DESC
            LIMIT ?
            """,
            (user_id, limit)
        ) as cursor:
            rows = await cursor.fetchall()
        
        return [
            {
                "report_id": row[0],
                "week_start": row[1],
                "week_end": row[2],
                "summary": row[3],
                "overall_accuracy": row[4],
                "generated_at": row[5]
            }
            for row in rows
        ]
    
    
    async def get_weak_topics(self, user_id: str) -> List[Dict]:
        """Get list of weak topics"""
        
        db = await get_database()
        
        threshold = settings.WEAK_TOPIC_THRESHOLD * 100
        
        async with db.execute(
            """
            SELECT topic, total_questions, correct_answers, accuracy
            FROM topic_performance
            WHERE user_id = ? AND accuracy < ?
            ORDER BY accuracy ASC
            """,
            (user_id, threshold)
        ) as cursor:
            rows = await cursor.fetchall()
        
        return [
            {
                "topic": row[0],
                "total_questions": row[1],
                "correct_answers": row[2],
                "accuracy": round(row[3], 1),
                "status": "weak"
            }
            for row in rows
        ]