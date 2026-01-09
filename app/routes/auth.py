"""
QuizSense AI - Authentication Routes (JWT Based)
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime, timedelta
import hashlib
import secrets

from jose import JWTError, jwt

from app.models.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token
)
from app.database.connection import get_database
from app.config import settings

# ============================================
# JWT CONFIG
# ============================================

ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY or "quizsense-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

router = APIRouter()
security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Hash password using SHA256 (simple for demo)"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Get current user from JWT token.
    Stateless; survives server restarts.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    db = await get_database()
    async with db.execute(
        """
        SELECT id, email, name, created_at, total_quizzes, current_streak
        FROM users WHERE id = ?
        """,
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return {
        "user_id": row[0],
        "email": row[1],
        "name": row[2]
    }


# ============================================
# ROUTES
# ============================================

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user.
    """

    db = await get_database()

    async with db.execute(
        "SELECT id FROM users WHERE email = ?",
        (user_data.email,)
    ) as cursor:
        existing = await cursor.fetchone()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_id = f"user_{secrets.token_hex(8)}"
    password_hash = hash_password(user_data.password)
    created_at = datetime.utcnow().isoformat()

    await db.execute(
        """
        INSERT INTO users (id, email, name, password_hash, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, user_data.email, user_data.name, password_hash, created_at)
    )
    await db.commit()

    access_token = create_access_token(
        data={"sub": user_id, "email": user_data.email}
    )

    user_response = UserResponse(
        id=user_id,
        email=user_data.email,
        name=user_data.name,
        created_at=datetime.utcnow(),
        total_quizzes=0,
        current_streak=0
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login user.
    """

    db = await get_database()

    async with db.execute(
        """
        SELECT id, email, name, password_hash, created_at, total_quizzes, current_streak
        FROM users WHERE email = ?
        """,
        (credentials.email,)
    ) as cursor:
        user = await cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(credentials.password, user[3]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": user[0], "email": user[1]}
    )

    user_response = UserResponse(
        id=user[0],
        email=user[1],
        name=user[2],
        created_at=datetime.fromisoformat(user[4]),
        total_quizzes=user[5] or 0,
        current_streak=user[6] or 0
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout current user.

    With JWT, logout is handled on the client by deleting the token.
    """
    return {"message": "Logged out successfully. Please clear the token on the client."}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""

    db = await get_database()

    async with db.execute(
        """
        SELECT id, email, name, created_at, total_quizzes, current_streak
        FROM users WHERE id = ?
        """,
        (current_user["user_id"],)
    ) as cursor:
        user = await cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user[0],
        email=user[1],
        name=user[2],
        created_at=datetime.fromisoformat(user[3]),
        total_quizzes=user[4] or 0,
        current_streak=user[5] or 0
    )


@router.get("/test")
async def test_auth():
    """Test endpoint"""
    return {
        "message": "Auth routes working (JWT)!",
        "endpoints": [
            "POST /auth/register",
            "POST /auth/login",
            "POST /auth/logout",
            "GET /auth/me"
        ]
    }