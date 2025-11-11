"""Authentication service - handles user registration, login, tokens."""
from typing import Optional, Tuple
from datetime import datetime, timedelta
import secrets

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.models.subscription import Subscription, SubscriptionPlan, SubscriptionStatus
from app.schemas.user import UserCreate
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)


class AuthService:
    """Authentication service for user management and token handling."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user_data: UserCreate) -> Tuple[User, str, str]:
        """
        Register a new user.

        Returns:
            (user, access_token, refresh_token)

        Raises:
            HTTPException: If email already exists
        """
        # Check if email exists
        result = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create user
        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            company=user_data.company,
            is_active=True,
            email_verified=False,  # TODO: Send verification email
            role=UserRole.USER,
        )

        self.db.add(user)
        await self.db.flush()  # Get user ID

        # Create free subscription
        subscription = Subscription(
            user_id=user.id,
            plan=SubscriptionPlan.FREE,
            status=SubscriptionStatus.ACTIVE,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30),
            searches_used="0",
            alerts_used="0",
        )

        self.db.add(subscription)
        await self.db.commit()
        await self.db.refresh(user)

        # Generate tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return user, access_token, refresh_token

    async def authenticate_user(
        self, email: str, password: str
    ) -> Optional[User]:
        """
        Authenticate user with email and password.

        Returns:
            User if authentication successful, None otherwise
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        return user

    async def login(self, email: str, password: str) -> Tuple[User, str, str]:
        """
        Login user and return tokens.

        Returns:
            (user, access_token, refresh_token)

        Raises:
            HTTPException: If credentials are invalid
        """
        user = await self.authenticate_user(email, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Generate tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return user, access_token, refresh_token

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def verify_email(self, user_id: str) -> User:
        """
        Mark user email as verified.

        TODO: Implement token-based verification
        """
        user = await self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.email_verified = True
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def request_password_reset(self, email: str) -> str:
        """
        Request password reset token.

        Returns:
            Reset token (in production, send via email)
        """
        user = await self.get_user_by_email(email)

        if not user:
            # Don't reveal if email exists (security best practice)
            return "If email exists, reset instructions have been sent"

        # Generate reset token (expires in 1 hour)
        reset_token = secrets.token_urlsafe(32)

        # TODO: Store token in Redis with expiry
        # TODO: Send email with reset link

        return reset_token

    async def reset_password(
        self, user_id: str, new_password: str
    ) -> User:
        """
        Reset user password.

        TODO: Validate reset token
        """
        user = await self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.password_hash = get_password_hash(new_password)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> User:
        """Change user password (requires current password)."""
        user = await self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password"
            )

        # Update password
        user.password_hash = get_password_hash(new_password)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def create_superuser(
        self, email: str, password: str, full_name: str
    ) -> User:
        """Create a superuser (admin)."""
        # Check if exists
        existing = await self.get_user_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        user = User(
            email=email,
            password_hash=get_password_hash(password),
            full_name=full_name,
            is_active=True,
            email_verified=True,
            is_superuser=True,
            role=UserRole.ADMIN,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user
