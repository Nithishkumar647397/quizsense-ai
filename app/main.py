"""
QuizSense AI - Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import auth, quiz, reports
from app.database.connection import init_database

# ============================================
# Create FastAPI Application
# ============================================

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered adaptive learning platform that generates quizzes, tracks performance, and provides personalized learning insights.",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============================================
# CORS Middleware (Allow Frontend to Connect)
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Include Route Modules
# ============================================

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    quiz.router,
    prefix="/quiz",
    tags=["Quiz"]
)

app.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"]
)

# ============================================
# Startup Event
# ============================================

@app.on_event("startup")
async def startup_event():
    """Initialize database and print config on startup"""
    print("\n🚀 Starting QuizSense AI Server...")
    
    # Print configuration
    settings.print_config()
    
    # Initialize database
    await init_database()
    
    print("✅ Server started successfully!\n")

# ============================================
# Health Check Endpoints
# ============================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API welcome message"""
    return {
        "message": "Welcome to QuizSense AI! 🧠",
        "version": settings.VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION
    }


@app.get("/config/check", tags=["Health"])
async def config_check():
    """Check if configuration is valid"""
    is_valid = settings.validate()
    return {
        "config_valid": is_valid,
        "azure_configured": bool(settings.AZURE_OPENAI_KEY),
        "database_configured": bool(settings.DATABASE_URL),
        "message": "All systems ready!" if is_valid else "Missing configuration. Check .env file."
    }


# ============================================
# Run with: uvicorn app.main:app --reload
# ============================================