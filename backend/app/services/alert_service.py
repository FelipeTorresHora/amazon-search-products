"""Alert service - manage product alerts and notifications."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert, AlertType
from app.schemas.alert import AlertCreate, AlertUpdate


class AlertService:
    """Service for product alert management."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_alert(self, user_id: UUID, alert_data: AlertCreate) -> Alert:
        """Create new product alert."""
        # Check if alert already exists
        result = await self.db.execute(
            select(Alert).where(
                and_(
                    Alert.user_id == user_id,
                    Alert.product_asin == alert_data.product_asin,
                    Alert.alert_type == AlertType(alert_data.alert_type),
                    Alert.is_active.is_(True),
                )
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Alert already exists for this product",
            )

        # Create alert
        alert = Alert(
            user_id=user_id,
            product_asin=alert_data.product_asin,
            alert_type=AlertType(alert_data.alert_type),
            threshold_value=alert_data.threshold_value,
            notify_email=alert_data.notify_email,
            notify_webhook=alert_data.notify_webhook,
            webhook_url=str(alert_data.webhook_url) if alert_data.webhook_url else None,
            is_active=True,
            trigger_count="0",
        )

        self.db.add(alert)
        await self.db.commit()
        await self.db.refresh(alert)

        return alert

    async def get_user_alerts(
        self, user_id: UUID, active_only: bool = True
    ) -> List[Alert]:
        """Get all alerts for a user."""
        query = select(Alert).where(Alert.user_id == user_id)

        if active_only:
            query = query.where(Alert.is_active.is_(True))

        query = query.order_by(Alert.created_at.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_alert(self, alert_id: UUID, user_id: UUID) -> Optional[Alert]:
        """Get specific alert (must belong to user)."""
        result = await self.db.execute(
            select(Alert).where(and_(Alert.id == alert_id, Alert.user_id == user_id))
        )
        return result.scalar_one_or_none()

    async def update_alert(
        self, alert_id: UUID, user_id: UUID, alert_data: AlertUpdate
    ) -> Alert:
        """Update alert configuration."""
        alert = await self.get_alert(alert_id, user_id)

        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found"
            )

        # Update fields if provided
        if alert_data.alert_type is not None:
            alert.alert_type = AlertType(alert_data.alert_type)

        if alert_data.threshold_value is not None:
            alert.threshold_value = alert_data.threshold_value

        if alert_data.is_active is not None:
            alert.is_active = alert_data.is_active

        if alert_data.notify_email is not None:
            alert.notify_email = alert_data.notify_email

        if alert_data.notify_webhook is not None:
            alert.notify_webhook = alert_data.notify_webhook

        if alert_data.webhook_url is not None:
            alert.webhook_url = str(alert_data.webhook_url)

        await self.db.commit()
        await self.db.refresh(alert)

        return alert

    async def delete_alert(self, alert_id: UUID, user_id: UUID) -> bool:
        """Delete alert."""
        alert = await self.get_alert(alert_id, user_id)

        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found"
            )

        await self.db.delete(alert)
        await self.db.commit()

        return True

    async def trigger_alert(
        self, alert: Alert, old_value: Optional[float], new_value: float, message: str
    ):
        """
        Trigger an alert (called by background tasks).

        Updates trigger count and last_triggered timestamp.
        Sends notifications via email/webhook.
        """
        alert.last_triggered = datetime.utcnow()
        alert.trigger_count = str(int(alert.trigger_count) + 1)

        await self.db.commit()

        # TODO: Send email notification
        if alert.notify_email:
            await self._send_email_notification(alert, message)

        # TODO: Send webhook notification
        if alert.notify_webhook and alert.webhook_url:
            await self._send_webhook_notification(alert, old_value, new_value, message)

    async def _send_email_notification(self, alert: Alert, message: str):
        """Send email notification (via SendGrid)."""
        # TODO: Implement SendGrid email sending
        print(f"Email notification: {message}")

    async def _send_webhook_notification(
        self, alert: Alert, old_value: Optional[float], new_value: float, message: str
    ):
        """Send webhook notification."""
        # TODO: Implement webhook POST request
        print(f"Webhook notification to {alert.webhook_url}: {message}")

    async def get_alerts_to_check(self) -> List[Alert]:
        """
        Get all active alerts that need checking.

        Called by Celery task to check for price changes.
        """
        result = await self.db.execute(select(Alert).where(Alert.is_active.is_(True)))
        return list(result.scalars().all())
