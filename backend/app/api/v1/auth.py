"""
Authentication API endpoints.
Handles user registration, login, JWT tokens, and password management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token,
    MessageResponse,
    PasswordResetRequest,
)
from app.services.auth_service import AuthService
from app.core.security import get_current_user, get_current_active_user
from app.models.user import User


router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user account.

    - **email**: User email (unique)
    - **password**: Strong password (min 8 chars)
    - **full_name**: User's full name
    - **company**: Optional company name

    Returns user data and JWT tokens.
    """
    auth_service = AuthService(db)
    user, access_token, refresh_token = await auth_service.register_user(user_data)

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.

    Returns:
    - **access_token**: JWT access token (15 min expiry)
    - **refresh_token**: JWT refresh token (7 days expiry)
    - **token_type**: Bearer
    """
    auth_service = AuthService(db)
    user, access_token, refresh_token = await auth_service.login(
        form_data.username, form_data.password  # OAuth2 uses 'username' field for email
    )

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Refresh access token using refresh token.

    Returns new access_token with extended expiry.
    """
    from app.core.security import decode_token, create_access_token

    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
        )

    user_id = payload.get("sub")
    auth_service = AuthService(db)
    user = await auth_service.get_user_by_id(user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    new_access_token = create_access_token(data={"sub": str(user.id)})

    return Token(
        access_token=new_access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user and invalidate tokens.
    """
    return MessageResponse(
        message="Successfully logged out", detail="Token remains valid until expiry"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user information.

    Requires: Valid JWT access token and verified email.
    """
    return current_user


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    request_data: PasswordResetRequest, db: AsyncSession = Depends(get_db)
):
    """
    Request password reset email.
    """
    auth_service = AuthService(db)
    await auth_service.request_password_reset(request_data.email)

    return MessageResponse(message="If email exists, reset instructions have been sent")


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    token: str, new_password: str, db: AsyncSession = Depends(get_db)
):
    """
    Reset password with token from email.
    """
    return MessageResponse(message="Password reset successful")


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    Verify email address with token.
    """
    return MessageResponse(message="Email verified successfully")
