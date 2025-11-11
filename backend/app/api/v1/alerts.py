"""Price and stock alerts API endpoints."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResponse,
    AlertListResponse,
)
from app.schemas.user import MessageResponse
from app.services.alert_service import AlertService
from app.services.subscription_service import SubscriptionService
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=AlertListResponse)
async def list_alerts(
    active_only: bool = True,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's active alerts."""
    alert_service = AlertService(db)
    alerts = await alert_service.get_user_alerts(current_user.id, active_only)

    active_count = sum(1 for a in alerts if a.is_active)

    return AlertListResponse(
        alerts=alerts,
        total=len(alerts),
        active=active_count,
        inactive=len(alerts) - active_count
    )


@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_data: AlertCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new price/stock alert.

    Requires: Available alert quota for current plan.
    """
    # Check alert quota
    subscription_service = SubscriptionService(db)
    can_create = await subscription_service.increment_usage(
        current_user.id, "alerts"
    )

    if not can_create:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Alert quota exceeded. Please upgrade your plan."
        )

    alert_service = AlertService(db)
    alert = await alert_service.create_alert(current_user.id, alert_data)

    return alert


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get alert details."""
    alert_service = AlertService(db)
    alert = await alert_service.get_alert(alert_id, current_user.id)

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )

    return alert


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: UUID,
    alert_data: AlertUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update alert configuration."""
    alert_service = AlertService(db)
    alert = await alert_service.update_alert(alert_id, current_user.id, alert_data)

    return alert


@router.delete("/{alert_id}", response_model=MessageResponse)
async def delete_alert(
    alert_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete alert."""
    alert_service = AlertService(db)
    await alert_service.delete_alert(alert_id, current_user.id)

    return MessageResponse(message="Alert deleted successfully")
