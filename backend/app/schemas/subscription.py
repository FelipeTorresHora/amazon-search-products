"""Subscription Pydantic schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


# =============================================================================
# SUBSCRIPTION SCHEMAS
# =============================================================================

class SubscriptionBase(BaseModel):
    """Base subscription schema."""
    plan: str = Field(..., pattern="^(free|pro|business|enterprise)$")


class SubscriptionCreate(SubscriptionBase):
    """Create subscription."""
    user_id: UUID


class SubscriptionUpdate(BaseModel):
    """Update subscription."""
    plan: Optional[str] = Field(None, pattern="^(free|pro|business|enterprise)$")
    status: Optional[str] = Field(
        None,
        pattern="^(active|canceled|past_due|trialing|incomplete)$"
    )


class SubscriptionInDB(SubscriptionBase):
    """Subscription as stored in DB."""
    id: UUID
    user_id: UUID
    status: str
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    stripe_customer_id: Optional[str]
    stripe_subscription_id: Optional[str]
    searches_used: str
    alerts_used: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SubscriptionResponse(SubscriptionInDB):
    """Subscription response for API."""
    api_key: Optional[str] = None  # Only for Business+


class UsageStats(BaseModel):
    """Usage statistics for current billing period."""
    plan: str
    status: str
    searches_used: int
    searches_limit: int
    searches_remaining: int
    alerts_used: int
    alerts_limit: int
    alerts_remaining: int
    period_start: Optional[datetime]
    period_end: Optional[datetime]
    can_upgrade: bool


# =============================================================================
# SUBSCRIPTION PLANS
# =============================================================================

class PlanFeatures(BaseModel):
    """Features included in a plan."""
    searches_per_month: int
    alerts_limit: int
    api_access: bool
    webhooks: bool
    history_months: Optional[int]  # None = unlimited
    export_formats: list[str]
    support: str
    rate_limit_per_minute: int


class SubscriptionPlan(BaseModel):
    """Subscription plan details."""
    id: str
    name: str
    price: float
    currency: str = "BRL"
    interval: str = "month"
    features: PlanFeatures
    stripe_price_id: Optional[str] = None
    is_popular: bool = False


class PlanListResponse(BaseModel):
    """List of available plans."""
    plans: list[SubscriptionPlan]


# =============================================================================
# STRIPE CHECKOUT
# =============================================================================

class CheckoutSessionCreate(BaseModel):
    """Create Stripe checkout session."""
    plan: str = Field(..., pattern="^(pro|business|enterprise)$")
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class CheckoutSessionResponse(BaseModel):
    """Checkout session response."""
    session_id: str
    checkout_url: str


class CustomerPortalResponse(BaseModel):
    """Customer portal response."""
    portal_url: str


# =============================================================================
# STRIPE WEBHOOKS
# =============================================================================

class StripeWebhookEvent(BaseModel):
    """Stripe webhook event."""
    type: str
    data: dict
