"""
QuizSense AI - User Models
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============================================
# User Base Model
# ============================================

class UserBase(BaseModel):
    """Base user fields"""
    email: str = Field(..., description="User email address")
    name: str = Field(..., description="User full name")


# ============================================
# User Create (Registration)
# ============================================

class UserCreate(UserBase):
    """Model for creating new user"""
    password: str = Field(..., min_length=6, description="User password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@example.com",
                "name": "John Doe",
                "password": "securepassword123"
            }
        }


# ============================================
# User Login
# ============================================

class UserLogin(BaseModel):
    """Model for user login"""
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@example.com",
                "password": "securepassword123"
            }
        }


# ============================================
# User Response (What API Returns)
# ============================================

class UserResponse(UserBase):
    """Model for user response (no password)"""
    id: str = Field(..., description="Unique user ID")
    created_at: datetime = Field(..., description="Account creation date")
    total_quizzes: int = Field(default=0, description="Total quizzes taken")
    current_streak: int = Field(default=0, description="Current daily streak")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "user_12345",
                "email": "student@example.com",
                "name": "John Doe",
                "created_at": "2024-01-15T10:30:00Z",
                "total_quizzes": 15,
                "current_streak": 5
            }
        }


# ============================================
# Full User Model (Database)
# ============================================

class User(UserBase):
    """Complete user model for database"""
    id: str
    password_hash: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    total_quizzes: int = 0
    current_streak: int = 0
    last_quiz_date: Optional[datetime] = None
    is_active: bool = True
    
    class Config:
        from_attributes = True


# ============================================
# Token Models (Authentication)
# ============================================

class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Data stored in JWT token"""
    user_id: str
    email: str