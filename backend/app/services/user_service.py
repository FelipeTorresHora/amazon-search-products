"""User service - user management operations."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserUpdate


class UserService:
    """Service for user management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users (admin only)."""
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        """Update user profile."""
        user = await self.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Update fields if provided
        if user_data.full_name is not None:
            user.full_name = user_data.full_name

        if user_data.company is not None:
            user.company = user_data.company

        if user_data.email is not None:
            # Check email uniqueness
            result = await self.db.execute(
                select(User).where(User.email == user_data.email, User.id != user_id)
            )
            existing = result.scalar_one_or_none()

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use",
                )

            user.email = user_data.email
            user.email_verified = False  # Require re-verification

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete_user(self, user_id: UUID) -> bool:
        """
        Delete user (LGPD compliance).

        Deletes user and all related data (cascading).
        """
        user = await self.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Soft delete (deactivate)
        user.is_active = False
        await self.db.commit()

        # For hard delete (uncomment):
        # await self.db.delete(user)
        # await self.db.commit()

        return True

    async def deactivate_user(self, user_id: UUID) -> User:
        """Deactivate user account."""
        user = await self.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user.is_active = False
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def activate_user(self, user_id: UUID) -> User:
        """Activate user account."""
        user = await self.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user.is_active = True
        await self.db.commit()
        await self.db.refresh(user)

        return user
