"""Alert Pydantic schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl


# =============================================================================
# ALERT SCHEMAS
# =============================================================================


class AlertBase(BaseModel):
    """Base alert schema."""

    product_asin: str = Field(..., min_length=10, max_length=10)
    alert_type: str = Field(
        ..., pattern="^(price_drop|stock_available|new_seller|rating_change)$"
    )
    threshold_value: Optional[float] = Field(None, description="For price_drop alerts")
    notify_email: bool = True
    notify_webhook: bool = False
    webhook_url: Optional[HttpUrl] = None


class AlertCreate(AlertBase):
    """Create new alert."""

    pass


class AlertUpdate(BaseModel):
    """Update alert."""

    alert_type: Optional[str] = Field(
        None, pattern="^(price_drop|stock_available|new_seller|rating_change)$"
    )
    threshold_value: Optional[float] = None
    is_active: Optional[bool] = None
    notify_email: Optional[bool] = None
    notify_webhook: Optional[bool] = None
    webhook_url: Optional[HttpUrl] = None


class AlertInDB(AlertBase):
    """Alert as stored in DB."""

    id: UUID
    user_id: UUID
    product_title: Optional[str]
    is_active: bool
    last_triggered: Optional[datetime]
    trigger_count: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AlertResponse(AlertInDB):
    """Alert response for API."""

    pass


class AlertListResponse(BaseModel):
    """List of alerts."""

    alerts: list[AlertResponse]
    total: int
    active: int
    inactive: int


# =============================================================================
# ALERT TRIGGERS
# =============================================================================


class AlertTrigger(BaseModel):
    """Alert trigger event."""

    alert_id: UUID
    product_asin: str
    product_title: str
    alert_type: str
    old_value: Optional[float]
    new_value: Optional[float]
    triggered_at: datetime
    message: str


class AlertHistory(BaseModel):
    """Alert trigger history."""

    alert_id: UUID
    triggers: list[AlertTrigger]
    total_triggers: int
