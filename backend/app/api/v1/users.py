"""User management API endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_users():
    """List all users (admin only)."""
    return {"users": []}


@router.get("/{user_id}")
async def get_user(user_id: str):
    """Get user by ID."""
    return {"user_id": user_id}


@router.put("/{user_id}")
async def update_user(user_id: str):
    """Update user profile."""
    return {"message": "User updated"}


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete user account (LGPD compliance)."""
    return {"message": "User deleted"}
