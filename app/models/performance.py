"""
QuizSense AI - Performance & Report Models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum


# ============================================
# Enums
# ============================================

class TopicStatus(str, Enum):
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"


class Trend(str, Enum):
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"


# ============================================
# Topic Performance
# ============================================

class TopicPerformance(BaseModel):
    topic: str = Field(..., description="Topic name")
    total_questions: int = Field(..., description="Total questions attempted")
    correct_answers: int = Field(..., description="Correct answers")
    accuracy: float = Field(..., description="Accuracy percentage")
    status: TopicStatus = Field(..., description="Weak/Moderate/Strong")
    trend: Trend = Field(default=Trend.STABLE, description="Performance trend")
    last_attempted: datetime = Field(..., description="Last attempt date")
    weak_subtopics: List[str] = Field(default=[], description="Weak sub-topics")


# ============================================
# Overall Performance
# ============================================

class Performance(BaseModel):
    user_id: str = Field(..., description="User ID")
    period: str = Field(default="last_7_days", description="Analysis period")
    total_quizzes: int = Field(..., description="Total quizzes taken")
    total_questions: int = Field(..., description="Total questions attempted")
    overall_accuracy: float = Field(..., description="Overall accuracy percentage")
    current_streak: int = Field(default=0, description="Current daily streak")
    best_streak: int = Field(default=0, description="Best daily streak")
    topics: List[TopicPerformance] = Field(..., description="Performance by topic")
    strong_topics: List[str] = Field(default=[], description="Strong topics")
    weak_topics: List[str] = Field(default=[], description="Weak topics")
    analyzed_at: datetime = Field(..., description="Analysis timestamp")


# ============================================
# Pattern Detection
# ============================================

class DetectedPattern(BaseModel):
    pattern_type: str = Field(..., description="Type of pattern")
    description: str = Field(..., description="Pattern description")
    evidence: str = Field(..., description="Evidence for this pattern")
    recommendation: str = Field(..., description="Recommended action")


# ============================================
# Weekly Report
# ============================================

class WeeklyReport(BaseModel):
    report_id: str = Field(..., description="Report ID")
    user_id: str = Field(..., description="User ID")
    week_start: date = Field(..., description="Week start date")
    week_end: date = Field(..., description="Week end date")
    summary: str = Field(..., description="Overall summary")
    overall_accuracy: float = Field(..., description="Week's overall accuracy")
    quizzes_completed: int = Field(..., description="Quizzes completed this week")
    strong_topics: List[str] = Field(default=[], description="Topics doing well")
    weak_topics: List[str] = Field(default=[], description="Topics needing work")
    improved_topics: List[str] = Field(default=[], description="Topics that improved")
    declined_topics: List[str] = Field(default=[], description="Topics that declined")
    patterns: List[DetectedPattern] = Field(default=[], description="Detected patterns")
    focus_topics: List[str] = Field(..., description="Topics to focus next week")
    study_recommendations: List[str] = Field(default=[], description="Study tips")
    full_report: str = Field(..., description="Complete AI-generated report")
    generated_at: datetime = Field(..., description="Report generation time")


# ============================================
# Dashboard Data
# ============================================

class DailyAccuracy(BaseModel):
    date: str
    accuracy: float


class TopicPerformanceItem(BaseModel):
    topic: str
    accuracy: float


class RecentQuizItem(BaseModel):
    topic: str
    difficulty: str
    score: int
    total: int
    percentage: float
    completed_at: str


class DashboardData(BaseModel):
    user_id: str
    user_name: str
    total_quizzes: int
    current_streak: int
    overall_accuracy: float
    quizzes_this_week: int
    weekly_accuracy: List[DailyAccuracy] = Field(default=[], description="Daily accuracy for chart")
    topic_performance: List[TopicPerformanceItem] = Field(default=[], description="Topic-wise performance")
    recent_quizzes: List[RecentQuizItem] = Field(default=[], description="Recent quiz summaries")
    recommended_topics: List[str] = Field(default=[], description="Topics to practice today")