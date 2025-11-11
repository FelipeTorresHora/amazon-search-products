"""Subscription and billing API endpoints."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.subscription import (
    CheckoutSessionCreate,
    CheckoutSessionResponse,
    CustomerPortalResponse,
    UsageStats,
)
from app.services.subscription_service import SubscriptionService

router = APIRouter()


@router.get("/plans")
async def list_plans():
    """List all available subscription plans."""
    return {
        "plans": [
            {
                "id": "free",
                "name": "Free",
                "price": 0,
                "currency": "BRL",
                "features": {
                    "searches_per_month": 50,
                    "alerts_limit": 5,
                    "api_access": False,
                    "support": "Community",
                },
            },
            {
                "id": "pro",
                "name": "Pro",
                "price": 97,
                "currency": "BRL",
                "features": {
                    "searches_per_month": 1000,
                    "alerts_limit": 50,
                    "api_access": False,
                    "support": "Email (48h)",
                },
                "is_popular": True,
            },
            {
                "id": "business",
                "name": "Business",
                "price": 297,
                "currency": "BRL",
                "features": {
                    "searches_per_month": 5000,
                    "alerts_limit": 200,
                    "api_access": True,
                    "support": "Email (24h)",
                },
            },
            {
                "id": "enterprise",
                "name": "Enterprise",
                "price": "custom",
                "currency": "BRL",
                "features": {
                    "searches_per_month": "unlimited",
                    "alerts_limit": "unlimited",
                    "api_access": True,
                    "support": "Phone (4h)",
                },
            },
        ]
    }


@router.post("/checkout", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    checkout_data: CheckoutSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create Stripe checkout session.

    Redirects user to Stripe payment page.
    """
    subscription_service = SubscriptionService(db)
    session = await subscription_service.create_checkout_session(
        current_user.id,
        checkout_data.plan,
        checkout_data.success_url,
        checkout_data.cancel_url,
    )

    return CheckoutSessionResponse(**session)


@router.post("/portal", response_model=CustomerPortalResponse)
async def customer_portal(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create Stripe customer portal session.

    Allows users to manage subscription and billing.
    """
    subscription_service = SubscriptionService(db)
    portal = await subscription_service.create_customer_portal_session(current_user.id)

    return CustomerPortalResponse(**portal)


@router.get("/usage", response_model=UsageStats)
async def get_usage(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current usage statistics for billing period."""
    subscription_service = SubscriptionService(db)
    usage = await subscription_service.get_usage_stats(current_user.id)

    return usage


@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Handle Stripe webhooks (subscription updates).

    Called by Stripe to notify of payment events.
    """
    payload = await request.body()

    # TODO: Verify webhook signature with Stripe

    import json

    event = json.loads(payload)

    subscription_service = SubscriptionService(db)
    await subscription_service.handle_stripe_webhook(event)

    return {"received": True}
