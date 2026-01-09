"""
QuizSense AI - Quiz Routes
Manual & AI-driven quiz generation with 24-hour limit
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import secrets

from app.models.quiz import (
    QuizRequest,
    QuizResponse,
    QuizQuestion,
    AnswerSubmission,
    QuizResult,
    QuestionResult,
    Difficulty
)
from app.routes.auth import get_current_user
from app.services.ai_agent import QuizAgent
from app.services.quiz_service import QuizService
from app.services.analysis_service import AnalysisService
from app.services.learning_agent import learning_agent
from app.database.connection import get_database

router = APIRouter()

quiz_agent = QuizAgent()
quiz_service = QuizService()
analysis_service = AnalysisService()


class AutoQuizRequest(BaseModel):
    domain: str
    num_questions: int = 5


async def check_daily_limit(user_id: str) -> bool:
    """Check if user has already taken a quiz today"""
    db = await get_database()
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    async with db.execute(
        "SELECT COUNT(*) FROM quizzes WHERE user_id = ? AND created_at >= ? AND is_completed = 1",
        (user_id, today_start.isoformat())
    ) as cursor:
        count = (await cursor.fetchone())[0]
    
    return count > 0


async def get_next_quiz_time(user_id: str) -> Optional[str]:
    """Get when user can take next quiz"""
    db = await get_database()
    
    async with db.execute(
        "SELECT created_at FROM quizzes WHERE user_id = ? AND is_completed = 1 ORDER BY created_at DESC LIMIT 1",
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()
    
    if row:
        last_quiz_time = datetime.fromisoformat(row[0])
        next_quiz_time = last_quiz_time + timedelta(hours=24)
        if next_quiz_time > datetime.utcnow():
            return next_quiz_time.isoformat()
    
    return None


@router.get("/can-take-quiz")
async def can_take_quiz(current_user: dict = Depends(get_current_user)):
    """Check if user can take a quiz today"""
    user_id = current_user["user_id"]
    has_taken = await check_daily_limit(user_id)
    next_time = await get_next_quiz_time(user_id)
    
    return {
        "can_take_quiz": not has_taken,
        "has_taken_today": has_taken,
        "next_quiz_available": next_time,
        "message": "You can only take 1 quiz per day!" if has_taken else "You can take a quiz now!"
    }

# =========================
# NEW: AI-DRIVEN QUIZ
# =========================

@router.post("/auto", response_model=QuizResponse)
async def generate_auto_quiz(
    request: AutoQuizRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    AI-driven quiz:
    - User chooses only DOMAIN (e.g., Python Programming)
    - Agent decides topic + difficulty based on history
    - 1 quiz per day limit
    """
    
    user_id = current_user["user_id"]
    
    # 24-hour limit
    has_taken = await check_daily_limit(user_id)
    if has_taken:
        next_time = await get_next_quiz_time(user_id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "You have already taken a quiz today!",
                "next_quiz_available": next_time,
                "wait_message": "Please come back tomorrow for your next quiz."
            }
        )
    
    # Get performance over last 30 days
    perf_data = await analysis_service.get_performance(user_id=user_id, days=30)
    
    if not perf_data:
        user_perf = {"total_quizzes": 0, "overall_accuracy": 0}
        topic_perf = {}
    else:
        user_perf = {
            "total_quizzes": perf_data["total_quizzes"],
            "overall_accuracy": perf_data["overall_accuracy"],
        }
        topic_perf = {}
        for topic_name, data in perf_data.get("topics", {}).items():
            total_q = data["total"]
            correct_q = data["correct"]
            acc = (correct_q / total_q * 100) if total_q > 0 else 0
            topic_perf[topic_name] = {
                "accuracy": acc,
                "attempts": total_q
            }
    
    # Let LearningAgent decide topic & difficulty
    plan = learning_agent.generate_personalized_quiz(
        domain=request.domain,
        user_performance=user_perf,
        topic_performance=topic_perf,
        num_questions=request.num_questions
    )
    
    chosen_topic = plan["topic"]
    difficulty_str = plan["difficulty"]
    
    # Avoid repeating same questions for that topic
    previous_questions = await quiz_service.get_previous_questions(
        user_id=user_id,
        topic=chosen_topic,
        limit=50
    )
    
    # Generate quiz questions using QuizAgent
    try:
        quiz_data = await quiz_agent.generate_quiz(
            subject=request.domain,
            topic=chosen_topic,
            difficulty=difficulty_str,
            num_questions=plan["num_questions"],
            previous_questions=previous_questions
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quiz: {str(e)}"
        )
    
    # Save quiz to DB
    quiz_id = f"quiz_{secrets.token_hex(8)}"
    created_at = datetime.utcnow()
    
    await quiz_service.save_quiz(
        quiz_id=quiz_id,
        user_id=user_id,
        subject=request.domain,
        topic=chosen_topic,
        difficulty=difficulty_str,
        questions=quiz_data["questions"],
        created_at=created_at
    )
    
    # Build response (hide correct answers)
    questions = []
    for q in quiz_data["questions"]:
        questions.append(QuizQuestion(
            q_id=q["q_id"],
            question=q["question"],
            options=q["options"],
            correct_answer="hidden",
            topic=q.get("topic", chosen_topic),
            sub_topic=q.get("sub_topic", chosen_topic),
            difficulty=Difficulty(difficulty_str),
            explanation=None
        ))
    
    return QuizResponse(
        quiz_id=quiz_id,
        subject=request.domain,
        topic=chosen_topic,
        difficulty=Difficulty(difficulty_str),
        questions=questions,
        total_questions=len(questions),
        time_limit_minutes=plan["num_questions"] * 2,
        created_at=created_at
    )

# =========================
# EXISTING MANUAL QUIZ (OPTIONAL)
# =========================

@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(
    request: QuizRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Manual quiz generation:
    - User chooses subject + topic + difficulty
    - 1 quiz per day limit
    """
    
    user_id = current_user["user_id"]
    
    # Check daily limit
    has_taken = await check_daily_limit(user_id)
    if has_taken:
        next_time = await get_next_quiz_time(user_id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "You have already taken a quiz today!",
                "next_quiz_available": next_time,
                "wait_message": "Please come back tomorrow for your next quiz."
            }
        )
    
    previous_questions = await quiz_service.get_previous_questions(
        user_id=user_id,
        topic=request.topic,
        limit=50
    )
    
    try:
        quiz_data = await quiz_agent.generate_quiz(
            subject=request.subject,
            topic=request.topic,
            difficulty=request.difficulty.value,
            num_questions=request.num_questions,
            previous_questions=previous_questions
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quiz: {str(e)}"
        )
    
    quiz_id = f"quiz_{secrets.token_hex(8)}"
    created_at = datetime.utcnow()
    
    await quiz_service.save_quiz(
        quiz_id=quiz_id,
        user_id=user_id,
        subject=request.subject,
        topic=request.topic,
        difficulty=request.difficulty.value,
        questions=quiz_data["questions"],
        created_at=created_at
    )
    
    questions = []
    for q in quiz_data["questions"]:
        questions.append(QuizQuestion(
            q_id=q["q_id"],
            question=q["question"],
            options=q["options"],
            correct_answer="hidden",
            topic=q.get("topic", request.topic),
            sub_topic=q.get("sub_topic"),
            difficulty=Difficulty(q.get("difficulty", request.difficulty.value)),
            explanation=None
        ))
    
    return QuizResponse(
        quiz_id=quiz_id,
        subject=request.subject,
        topic=request.topic,
        difficulty=request.difficulty,
        questions=questions,
        total_questions=len(questions),
        time_limit_minutes=request.num_questions * 2,
        created_at=created_at
    )


@router.post("/submit", response_model=QuizResult)
async def submit_quiz(
    submission: AnswerSubmission,
    current_user: dict = Depends(get_current_user)
):
    """Submit quiz answers and get results"""
    
    user_id = current_user["user_id"]
    
    quiz = await quiz_service.get_quiz(submission.quiz_id)
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    if quiz["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    if quiz.get("is_completed"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz already submitted"
        )
    
    questions = quiz["questions"]
    results = []
    correct_count = 0
    topic_breakdown = {}
    
    answer_lookup = {a.q_id: a for a in submission.answers}
    
    for q in questions:
        q_id = q["q_id"]
        topic = q.get("topic", quiz["topic"])
        correct_answer = q["correct_answer"]
        
        user_answer = answer_lookup.get(q_id)
        selected = user_answer.selected_option if user_answer else "none"
        
        is_correct = selected.upper() == correct_answer.upper()
        if is_correct:
            correct_count += 1
        
        if topic not in topic_breakdown:
            topic_breakdown[topic] = {"correct": 0, "total": 0}
        topic_breakdown[topic]["total"] += 1
        if is_correct:
            topic_breakdown[topic]["correct"] += 1
        
        results.append(QuestionResult(
            q_id=q_id,
            question=q["question"],
            selected_option=selected,
            correct_option=correct_answer,
            is_correct=is_correct,
            topic=topic,
            explanation=q.get("explanation")
        ))
    
    total = len(questions)
    percentage = (correct_count / total * 100) if total > 0 else 0
    completed_at = datetime.utcnow()
    
    await quiz_service.save_attempt(
        quiz_id=submission.quiz_id,
        user_id=user_id,
        answers=submission.answers,
        score=correct_count,
        total=total,
        time_taken=submission.total_time_seconds,
        topic_breakdown=topic_breakdown,
        completed_at=completed_at
    )
    
    await quiz_service.update_user_stats(user_id)
    
    return QuizResult(
        quiz_id=submission.quiz_id,
        user_id=user_id,
        score=correct_count,
        total=total,
        percentage=round(percentage, 1),
        time_taken_seconds=submission.total_time_seconds,
        results=results,
        topic_breakdown=topic_breakdown,
        completed_at=completed_at
    )


@router.get("/history")
async def get_quiz_history(
    current_user: dict = Depends(get_current_user),
    days: int = Query(default=7, ge=1, le=30),
    limit: int = Query(default=10, ge=1, le=50)
):
    """Get user's quiz history"""
    user_id = current_user["user_id"]
    history = await quiz_service.get_user_history(user_id=user_id, days=days, limit=limit)
    
    return {
        "user_id": user_id,
        "period_days": days,
        "total_quizzes": len(history),
        "quizzes": history
    }


@router.get("/topics")
async def get_available_topics(subject: Optional[str] = Query(default=None)):
    """Get available topics (manual mode only)"""
    
    topics = {
        "Python Programming": [
            "Variables and Data Types", "Operators", "Control Flow", "Loops",
            "Strings", "Lists and Tuples", "Dictionaries", "Functions",
            "File Handling", "Exception Handling", "OOP Basics", "Recursion"
        ],
        "Data Structures": [
            "Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs", "Hash Tables"
        ],
        "Algorithms": [
            "Sorting", "Searching", "Recursion", "Dynamic Programming", "Greedy Algorithms"
        ],
        "Web Development": [
            "HTML Basics", "CSS Fundamentals", "JavaScript Basics", "DOM Manipulation", "APIs and REST"
        ]
    }
    
    if subject and subject in topics:
        return {"subject": subject, "topics": topics[subject]}
    
    return {"subjects": list(topics.keys()), "topics_by_subject": topics}


@router.get("/test")
async def test_quiz():
    """Test endpoint"""
    return {
        "message": "Quiz routes working!",
        "daily_limit": "1 quiz per 24 hours",
        "ai_mode": "/quiz/auto"
    }