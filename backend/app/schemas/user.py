"""User Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator


# =============================================================================
# USER SCHEMAS
# =============================================================================


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    company: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets requirements."""
        from app.core.security import validate_password

        is_valid, error_msg = validate_password(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None


class UserUpdatePassword(BaseModel):
    """Schema for password update."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        from app.core.security import validate_password

        is_valid, error_msg = validate_password(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v


class UserInDB(UserBase):
    """User schema as stored in database."""

    id: UUID
    is_active: bool
    is_superuser: bool
    email_verified: bool
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserResponse(UserInDB):
    """User schema for API responses (public data)."""

    pass


class UserMe(UserResponse):
    """Extended user schema for /me endpoint with subscription info."""

    # Will be extended with subscription data
    pass


# =============================================================================
# AUTH SCHEMAS
# =============================================================================


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str  # User ID
    exp: datetime
    type: str  # "access" or "refresh"


class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""

    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Request password reset."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with token."""

    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class EmailVerification(BaseModel):
    """Email verification schema."""

    token: str


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str
    detail: Optional[str] = None
