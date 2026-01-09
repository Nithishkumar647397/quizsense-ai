"""
QuizSense AI - Configuration Settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # App Info
    APP_NAME: str = os.getenv("APP_NAME", "QuizSense AI")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    VERSION: str = "1.0.0"
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_KEY: str = os.getenv("AZURE_OPENAI_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./quizsense.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    
    # Quiz Settings
    DEFAULT_QUESTIONS_PER_QUIZ: int = 5
    MAX_QUESTIONS_PER_QUIZ: int = 20
    MIN_QUESTIONS_PER_QUIZ: int = 3
    
    # Analysis Settings
    WEAK_TOPIC_THRESHOLD: float = 0.6  # Below 60% = weak
    STRONG_TOPIC_THRESHOLD: float = 0.8  # Above 80% = strong
    
    def validate(self) -> bool:
        """Check if all required settings are present"""
        required = [
            self.AZURE_OPENAI_KEY,
            self.AZURE_OPENAI_ENDPOINT,
            self.AZURE_OPENAI_DEPLOYMENT
        ]
        return all(required)
    
    def print_config(self):
        """Print current configuration (for debugging)"""
        print("=" * 50)
        print("QuizSense AI Configuration")
        print("=" * 50)
        print(f"App Name: {self.APP_NAME}")
        print(f"Debug Mode: {self.DEBUG}")
        print(f"Azure Endpoint: {self.AZURE_OPENAI_ENDPOINT[:30]}...")
        print(f"Database: {self.DATABASE_URL}")
        print("=" * 50)


# Create global settings instance
settings = Settings()