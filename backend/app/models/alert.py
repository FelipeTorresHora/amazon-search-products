"""Alert database model."""
from sqlalchemy import Column, String, Enum, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class AlertType(str, enum.Enum):
    """Types of alerts."""
    PRICE_DROP = "price_drop"
    STOCK_AVAILABLE = "stock_available"
    NEW_SELLER = "new_seller"
    RATING_CHANGE = "rating_change"


class Alert(BaseModel):
    """Product alert model."""

    __tablename__ = "alerts"

    # User relationship
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Product info
    product_asin = Column(String(20), nullable=False, index=True)
    product_title = Column(String(500), nullable=True)

    # Alert configuration
    alert_type = Column(Enum(AlertType), nullable=False)
    threshold_value = Column(Float, nullable=True)  # For price alerts

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    last_triggered = Column(DateTime, nullable=True)
    trigger_count = Column(String, default="0", nullable=False)

    # Notification settings
    notify_email = Column(Boolean, default=True, nullable=False)
    notify_webhook = Column(Boolean, default=False, nullable=False)
    webhook_url = Column(String(500), nullable=True)

    # Relationships
    # user = relationship("User", back_populates="alerts")

    def __repr__(self):
        return f"<Alert {self.alert_type} for {self.product_asin}>"
