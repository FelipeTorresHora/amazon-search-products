"""Subscription and billing API endpoints."""
from fastapi import APIRouter

router = APIRouter()

@router.get("/plans")
async def list_plans():
    """List all available subscription plans."""
    return {
        "plans": [
            {"name": "Free", "price": 0, "searches": 50},
            {"name": "Pro", "price": 97, "searches": 1000},
            {"name": "Business", "price": 297, "searches": 5000},
            {"name": "Enterprise", "price": "custom", "searches": "unlimited"}
        ]
    }

@router.post("/checkout")
async def create_checkout_session():
    """Create Stripe checkout session."""
    return {"checkout_url": "https://checkout.stripe.com/..."}

@router.post("/portal")
async def customer_portal():
    """Create Stripe customer portal session."""
    return {"portal_url": "https://billing.stripe.com/..."}

@router.get("/usage")
async def get_usage():
    """Get current usage statistics."""
    return {"searches_used": 10, "searches_limit": 50, "alerts_used": 2}

@router.post("/webhook")
async def stripe_webhook():
    """Handle Stripe webhooks (subscription updates)."""
    return {"received": True}
