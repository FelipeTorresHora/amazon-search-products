"""
Authentication API endpoints.
Handles user registration, login, JWT tokens, and OAuth.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register():
    """
    Register a new user account.

    - **email**: User email (unique)
    - **password**: Strong password (min 8 chars)
    - **full_name**: User's full name
    - **company**: Optional company name

    Returns user data and confirmation email sent.
    """
    # TODO: Implement user registration
    return {"message": "User registration endpoint - TODO"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login with email and password.

    Returns:
    - **access_token**: JWT access token (15 min expiry)
    - **refresh_token**: JWT refresh token (7 days expiry)
    - **token_type**: Bearer
    """
    # TODO: Implement login logic
    # TODO: Verify credentials
    # TODO: Generate JWT tokens
    return {
        "access_token": "todo_generate_token",
        "refresh_token": "todo_generate_refresh_token",
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_token():
    """
    Refresh access token using refresh token.

    Returns new access_token with extended expiry.
    """
    # TODO: Implement token refresh
    return {"access_token": "new_token", "token_type": "bearer"}


@router.post("/logout")
async def logout():
    """
    Logout user and invalidate tokens.
    """
    # TODO: Blacklist token
    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_current_user():
    """
    Get current authenticated user information.

    Requires: Valid JWT access token
    """
    # TODO: Get user from token
    return {"user": "current_user_data"}


@router.post("/forgot-password")
async def forgot_password():
    """
    Request password reset email.
    """
    # TODO: Send password reset email
    return {"message": "Password reset email sent"}


@router.post("/reset-password")
async def reset_password():
    """
    Reset password with token from email.
    """
    # TODO: Verify token and update password
    return {"message": "Password reset successful"}


@router.post("/verify-email")
async def verify_email():
    """
    Verify email address with token.
    """
    # TODO: Verify email token
    return {"message": "Email verified"}
