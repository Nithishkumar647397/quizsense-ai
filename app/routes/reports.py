"""
QuizSense AI - Reports Routes
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional
from datetime import datetime, date, timedelta
import secrets

from app.models.performance import (
    Performance,
    TopicPerformance,
    WeeklyReport,
    DashboardData,
    DetectedPattern,
    TopicStatus,
    Trend
)
from app.routes.auth import get_current_user
from app.services.ai_agent import QuizAgent
from app.services.analysis_service import AnalysisService
from app.database.connection import get_database

# ============================================
# Router Setup
# ============================================

router = APIRouter()

# Initialize services
quiz_agent = QuizAgent()
analysis_service = AnalysisService()

# ============================================
# Routes
# ============================================

@router.get("/weekly", response_model=WeeklyReport)
async def get_weekly_report(
    current_user: dict = Depends(get_current_user)
):
    """
    Generate and return weekly weakness report
    
    This analyzes the past 7 days of quiz performance
    and generates AI-powered insights.
    """
    
    user_id = current_user["user_id"]
    user_name = current_user.get("name", "Learner")
    
    # Get performance data for last 7 days
    performance_data = await analysis_service.get_weekly_performance(user_id)
    
    if not performance_data or performance_data["total_quizzes"] == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No quiz data found for this week. Take some quizzes first!"
        )
    
    # Generate AI analysis and report
    try:
        report_data = await quiz_agent.generate_weekly_report(
            user_name=user_name,
            performance_data=performance_data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )
    
    # Calculate week dates
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Build patterns list
    patterns = [
        DetectedPattern(
            pattern_type=p["type"],
            description=p["description"],
            evidence=p["evidence"],
            recommendation=p["recommendation"]
        )
        for p in report_data.get("patterns", [])
    ]
    
    # Create report
    report = WeeklyReport(
        report_id=f"report_{secrets.token_hex(8)}",
        user_id=user_id,
        week_start=week_start,
        week_end=week_end,
        summary=report_data["summary"],
        overall_accuracy=performance_data["overall_accuracy"],
        quizzes_completed=performance_data["total_quizzes"],
        strong_topics=report_data.get("strong_topics", []),
        weak_topics=report_data.get("weak_topics", []),
        improved_topics=report_data.get("improved_topics", []),
        declined_topics=report_data.get("declined_topics", []),
        patterns=patterns,
        focus_topics=report_data.get("focus_topics", []),
        study_recommendations=report_data.get("recommendations", []),
        full_report=report_data["full_report"],
        generated_at=datetime.utcnow()
    )
    
    # Save report to database
    await analysis_service.save_weekly_report(report)
    
    return report


@router.get("/performance")
async def get_performance(
    current_user: dict = Depends(get_current_user),
    days: int = Query(default=7, ge=1, le=30, description="Analysis period in days")
):
    """
    Get detailed performance analysis
    
    - **days**: Number of days to analyze (1-30)
    """
    
    user_id = current_user["user_id"]
    
    # Get performance data
    performance_data = await analysis_service.get_performance(
        user_id=user_id,
        days=days
    )
    
    if not performance_data:
        return {
            "user_id": user_id,
            "period": f"last_{days}_days",
            "message": "No quiz data found",
            "total_quizzes": 0
        }
    
    # Build topic performance list
    topic_performances = []
    for topic, data in performance_data.get("topics", {}).items():
        accuracy = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
        
        # Determine status
        if accuracy >= 80:
            status = TopicStatus.STRONG
        elif accuracy >= 60:
            status = TopicStatus.MODERATE
        else:
            status = TopicStatus.WEAK
        
        topic_performances.append(TopicPerformance(
            topic=topic,
            total_questions=data["total"],
            correct_answers=data["correct"],
            accuracy=round(accuracy, 1),
            status=status,
            trend=Trend.STABLE,  # Can be calculated with more data
            last_attempted=datetime.utcnow(),
            weak_subtopics=data.get("weak_subtopics", [])
        ))
    
    # Identify strong and weak topics
    strong_topics = [tp.topic for tp in topic_performances if tp.status == TopicStatus.STRONG]
    weak_topics = [tp.topic for tp in topic_performances if tp.status == TopicStatus.WEAK]
    
    return Performance(
        user_id=user_id,
        period=f"last_{days}_days",
        total_quizzes=performance_data["total_quizzes"],
        total_questions=performance_data["total_questions"],
        overall_accuracy=performance_data["overall_accuracy"],
        current_streak=performance_data.get("current_streak", 0),
        best_streak=performance_data.get("best_streak", 0),
        topics=topic_performances,
        strong_topics=strong_topics,
        weak_topics=weak_topics,
        analyzed_at=datetime.utcnow()
    )


@router.get("/dashboard", response_model=DashboardData)
async def get_dashboard(
    current_user: dict = Depends(get_current_user)
):
    """
    Get dashboard data for frontend charts
    """
    
    user_id = current_user["user_id"]
    user_name = current_user.get("name", "Learner")
    
    # Get dashboard data
    dashboard_data = await analysis_service.get_dashboard_data(user_id)
    
    return DashboardData(
        user_id=user_id,
        user_name=user_name,
        total_quizzes=dashboard_data.get("total_quizzes", 0),
        current_streak=dashboard_data.get("current_streak", 0),
        overall_accuracy=dashboard_data.get("overall_accuracy", 0),
        quizzes_this_week=dashboard_data.get("quizzes_this_week", 0),
        weekly_accuracy=dashboard_data.get("weekly_accuracy", []),
        topic_performance=dashboard_data.get("topic_performance", []),
        recent_quizzes=dashboard_data.get("recent_quizzes", []),
        recommended_topics=dashboard_data.get("recommended_topics", [])
    )


@router.get("/history")
async def get_report_history(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(default=4, ge=1, le=12, description="Number of reports")
):
    """
    Get past weekly reports
    
    - **limit**: Number of reports to return
    """
    
    user_id = current_user["user_id"]
    
    reports = await analysis_service.get_report_history(
        user_id=user_id,
        limit=limit
    )
    
    return {
        "user_id": user_id,
        "total_reports": len(reports),
        "reports": reports
    }


@router.get("/topics/weak")
async def get_weak_topics(
    current_user: dict = Depends(get_current_user)
):
    """
    Get list of weak topics that need improvement
    """
    
    user_id = current_user["user_id"]
    
    weak_topics = await analysis_service.get_weak_topics(user_id)
    
    return {
        "user_id": user_id,
        "weak_topics": weak_topics,
        "message": "Focus on these topics to improve!" if weak_topics else "Great job! No weak topics found."
    }


@router.get("/test")
async def test_reports():
    """Test endpoint - no auth required"""
    return {
        "message": "Reports routes working!",
        "endpoints": [
            "GET /reports/weekly",
            "GET /reports/performance",
            "GET /reports/dashboard",
            "GET /reports/history",
            "GET /reports/topics/weak"
        ]
    }