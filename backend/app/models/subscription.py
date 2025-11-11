"""Subscription database model."""

from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class SubscriptionPlan(str, enum.Enum):
    """Available subscription plans."""

    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    """Subscription statuses."""

    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    TRIALING = "trialing"
    INCOMPLETE = "incomplete"


class Subscription(BaseModel):
    """User subscription model."""

    __tablename__ = "subscriptions"

    # User relationship
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )

    # Plan details
    plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)

    status = Column(
        Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False
    )

    # Billing period
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)

    # Stripe integration
    stripe_customer_id = Column(String(255), nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)

    # API access
    api_key = Column(String(255), nullable=True, unique=True)  # Hashed

    # Usage tracking
    searches_used = Column(String, default="0", nullable=False)
    alerts_used = Column(String, default="0", nullable=False)

    # Relationships
    # user = relationship("User", back_populates="subscription")

    def __repr__(self):
        return f"<Subscription {self.plan} - {self.status}>"
