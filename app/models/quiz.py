"""
QuizSense AI - Quiz Models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


# ============================================
# Enums
# ============================================

class Difficulty(str, Enum):
    """Quiz difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionType(str, Enum):
    """Types of questions"""
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    CONCEPTUAL = "conceptual"


# ============================================
# Quiz Question Model
# ============================================

class QuizQuestion(BaseModel):
    """Single quiz question"""
    q_id: str = Field(..., description="Question ID")
    question: str = Field(..., description="Question text")
    options: Dict[str, str] = Field(..., description="Answer options A, B, C, D")
    correct_answer: str = Field(..., description="Correct option key")
    topic: str = Field(..., description="Topic this question belongs to")
    sub_topic: Optional[str] = Field(None, description="Sub-topic")
    difficulty: Difficulty = Field(..., description="Question difficulty")
    explanation: Optional[str] = Field(None, description="Answer explanation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "q_id": "q1",
                "question": "What is the output of print(2 ** 3)?",
                "options": {
                    "A": "6",
                    "B": "8",
                    "C": "9",
                    "D": "5"
                },
                "correct_answer": "B",
                "topic": "Python Basics",
                "sub_topic": "Operators",
                "difficulty": "easy",
                "explanation": "** is the exponentiation operator. 2^3 = 8"
            }
        }


# ============================================
# Quiz Request (Generate Quiz)
# ============================================

class QuizRequest(BaseModel):
    """Request to generate a new quiz"""
    subject: str = Field(..., description="Subject name")
    topic: str = Field(..., description="Topic to quiz on")
    difficulty: Difficulty = Field(default=Difficulty.MEDIUM, description="Quiz difficulty")
    num_questions: int = Field(default=5, ge=3, le=20, description="Number of questions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Python Programming",
                "topic": "Functions",
                "difficulty": "medium",
                "num_questions": 5
            }
        }


# ============================================
# Quiz Response (Generated Quiz)
# ============================================

class QuizResponse(BaseModel):
    """Generated quiz response"""
    quiz_id: str = Field(..., description="Unique quiz ID")
    subject: str = Field(..., description="Subject name")
    topic: str = Field(..., description="Topic name")
    difficulty: Difficulty = Field(..., description="Quiz difficulty")
    questions: List[QuizQuestion] = Field(..., description="List of questions")
    total_questions: int = Field(..., description="Total number of questions")
    time_limit_minutes: int = Field(default=10, description="Time limit in minutes")
    created_at: datetime = Field(..., description="Quiz creation time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": "quiz_abc123",
                "subject": "Python Programming",
                "topic": "Functions",
                "difficulty": "medium",
                "questions": [],
                "total_questions": 5,
                "time_limit_minutes": 10,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


# ============================================
# Answer Submission
# ============================================

class SingleAnswer(BaseModel):
    """Single question answer"""
    q_id: str = Field(..., description="Question ID")
    selected_option: str = Field(..., description="Selected option (A/B/C/D)")
    time_taken_seconds: int = Field(default=0, description="Time taken for this question")


class AnswerSubmission(BaseModel):
    """Submit quiz answers"""
    quiz_id: str = Field(..., description="Quiz ID")
    answers: List[SingleAnswer] = Field(..., description="List of answers")
    total_time_seconds: int = Field(default=0, description="Total time taken")
    
    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": "quiz_abc123",
                "answers": [
                    {"q_id": "q1", "selected_option": "B", "time_taken_seconds": 30},
                    {"q_id": "q2", "selected_option": "A", "time_taken_seconds": 45}
                ],
                "total_time_seconds": 180
            }
        }


# ============================================
# Quiz Result
# ============================================

class QuestionResult(BaseModel):
    """Result for single question"""
    q_id: str
    question: str
    selected_option: str
    correct_option: str
    is_correct: bool
    topic: str
    explanation: Optional[str] = None


class QuizResult(BaseModel):
    """Complete quiz result"""
    quiz_id: str
    user_id: str
    score: int = Field(..., description="Number of correct answers")
    total: int = Field(..., description="Total questions")
    percentage: float = Field(..., description="Score percentage")
    time_taken_seconds: int
    results: List[QuestionResult] = Field(..., description="Individual question results")
    topic_breakdown: Dict[str, Dict[str, int]] = Field(..., description="Performance by topic")
    completed_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": "quiz_abc123",
                "user_id": "user_12345",
                "score": 4,
                "total": 5,
                "percentage": 80.0,
                "time_taken_seconds": 180,
                "results": [],
                "topic_breakdown": {
                    "Functions": {"correct": 3, "total": 4},
                    "Variables": {"correct": 1, "total": 1}
                },
                "completed_at": "2024-01-15T10:45:00Z"
            }
        }


# ============================================
# Quiz (Database Model)
# ============================================

class Quiz(BaseModel):
    """Complete quiz model for database"""
    id: str
    user_id: str
    subject: str
    topic: str
    difficulty: Difficulty
    questions: List[QuizQuestion]
    created_at: datetime
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    score: Optional[int] = None
    
    class Config:
        from_attributes = True