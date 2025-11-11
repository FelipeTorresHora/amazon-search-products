"""Subscription service - manage user subscriptions and billing."""

from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

import stripe
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.security import generate_api_key
from app.models.subscription import Subscription, SubscriptionPlan, SubscriptionStatus
from app.models.user import User, UserRole
from app.schemas.subscription import SubscriptionPlan as PlanSchema
from app.schemas.subscription import UsageStats

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionService:
    """Service for subscription and billing management."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_subscription(self, user_id: UUID) -> Optional[Subscription]:
        """Get user's subscription."""
        result = await self.db.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_usage_stats(self, user_id: UUID) -> UsageStats:
        """Get usage statistics for user's current billing period."""
        subscription = await self.get_subscription(user_id)

        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
            )

        # Get limits for plan
        searches_limit = settings.get_usage_limit(subscription.plan.value, "searches")
        alerts_limit = settings.get_usage_limit(subscription.plan.value, "alerts")

        searches_used = int(subscription.searches_used or "0")
        alerts_used = int(subscription.alerts_used or "0")

        return UsageStats(
            plan=subscription.plan.value,
            status=subscription.status.value,
            searches_used=searches_used,
            searches_limit=searches_limit,
            searches_remaining=max(0, searches_limit - searches_used),
            alerts_used=alerts_used,
            alerts_limit=alerts_limit,
            alerts_remaining=max(0, alerts_limit - alerts_used),
            period_start=subscription.current_period_start,
            period_end=subscription.current_period_end,
            can_upgrade=subscription.plan != SubscriptionPlan.ENTERPRISE,
        )

    async def increment_usage(
        self, user_id: UUID, usage_type: str = "searches"
    ) -> bool:
        """
        Increment usage counter and check if limit exceeded.

        Returns:
            True if under limit, False if exceeded
        """
        subscription = await self.get_subscription(user_id)

        if not subscription:
            return False

        # Get limit
        limit = settings.get_usage_limit(subscription.plan.value, usage_type)

        # Get current usage
        if usage_type == "searches":
            current = int(subscription.searches_used or "0")
        elif usage_type == "alerts":
            current = int(subscription.alerts_used or "0")
        else:
            return False

        # Check limit
        if current >= limit:
            return False

        # Increment
        new_value = str(current + 1)
        if usage_type == "searches":
            subscription.searches_used = new_value
        elif usage_type == "alerts":
            subscription.alerts_used = new_value

        await self.db.commit()
        return True

    async def create_checkout_session(
        self,
        user_id: UUID,
        plan: str,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
    ) -> dict:
        """
        Create Stripe checkout session for subscription upgrade.

        Returns:
            {"session_id": str, "checkout_url": str}
        """
        # Get user
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Get subscription
        subscription = await self.get_subscription(user_id)

        # Get Stripe price ID
        price_id = settings.get_stripe_price_id(plan)

        if not price_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid plan: {plan}"
            )

        try:
            # Create or retrieve Stripe customer
            if subscription and subscription.stripe_customer_id:
                customer_id = subscription.stripe_customer_id
            else:
                customer = stripe.Customer.create(
                    email=user.email,
                    name=user.full_name,
                    metadata={"user_id": str(user_id)},
                )
                customer_id = customer.id

                # Save customer ID
                if subscription:
                    subscription.stripe_customer_id = customer_id
                    await self.db.commit()

            # Create checkout session
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                success_url=success_url or settings.STRIPE_SUCCESS_URL,
                cancel_url=cancel_url or settings.STRIPE_CANCEL_URL,
                metadata={
                    "user_id": str(user_id),
                    "plan": plan,
                },
            )

            return {
                "session_id": session.id,
                "checkout_url": session.url,
            }

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}",
            )

    async def create_customer_portal_session(self, user_id: UUID) -> dict:
        """
        Create Stripe customer portal session for managing subscription.

        Returns:
            {"portal_url": str}
        """
        subscription = await self.get_subscription(user_id)

        if not subscription or not subscription.stripe_customer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No active Stripe subscription found",
            )

        try:
            session = stripe.billing_portal.Session.create(
                customer=subscription.stripe_customer_id,
                return_url=settings.FRONTEND_URL,
            )

            return {"portal_url": session.url}

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}",
            )

    async def handle_stripe_webhook(self, event: dict) -> bool:
        """
        Handle Stripe webhook events.

        Called by webhook endpoint to sync subscription state.
        """
        event_type = event.get("type")
        data = event.get("data", {}).get("object", {})

        if event_type == "checkout.session.completed":
            # Payment successful, activate subscription
            await self._activate_subscription(data)

        elif event_type == "customer.subscription.updated":
            # Subscription changed
            await self._update_subscription(data)

        elif event_type == "customer.subscription.deleted":
            # Subscription canceled
            await self._cancel_subscription(data)

        elif event_type == "invoice.payment_failed":
            # Payment failed
            await self._handle_payment_failure(data)

        return True

    async def _activate_subscription(self, session_data: dict):
        """Activate subscription after successful payment."""
        user_id = session_data.get("metadata", {}).get("user_id")
        plan = session_data.get("metadata", {}).get("plan")
        subscription_id = session_data.get("subscription")

        if not user_id or not plan:
            return

        # Get subscription
        subscription = await self.get_subscription(UUID(user_id))

        if not subscription:
            return

        # Update subscription
        subscription.plan = SubscriptionPlan(plan)
        subscription.status = SubscriptionStatus.ACTIVE
        subscription.stripe_subscription_id = subscription_id
        subscription.current_period_start = datetime.utcnow()
        subscription.current_period_end = datetime.utcnow() + timedelta(days=30)

        # Generate API key for Business+
        if plan in ["business", "enterprise"]:
            subscription.api_key = generate_api_key()

            # Update user role
            result = await self.db.execute(select(User).where(User.id == UUID(user_id)))
            user = result.scalar_one_or_none()
            if user:
                user.role = UserRole(plan.upper())

        # Reset usage counters
        subscription.searches_used = "0"
        subscription.alerts_used = "0"

        await self.db.commit()

    async def _update_subscription(self, subscription_data: dict):
        """Update subscription details."""
        # TODO: Implement subscription update logic
        pass

    async def _cancel_subscription(self, subscription_data: dict):
        """Handle subscription cancellation."""
        stripe_sub_id = subscription_data.get("id")

        result = await self.db.execute(
            select(Subscription).where(
                Subscription.stripe_subscription_id == stripe_sub_id
            )
        )
        subscription = result.scalar_one_or_none()

        if subscription:
            subscription.status = SubscriptionStatus.CANCELED
            subscription.plan = SubscriptionPlan.FREE

            # Update user role
            result = await self.db.execute(
                select(User).where(User.id == subscription.user_id)
            )
            user = result.scalar_one_or_none()
            if user:
                user.role = UserRole.USER

            await self.db.commit()

    async def _handle_payment_failure(self, invoice_data: dict):
        """Handle failed payment."""
        customer_id = invoice_data.get("customer")

        result = await self.db.execute(
            select(Subscription).where(Subscription.stripe_customer_id == customer_id)
        )
        subscription = result.scalar_one_or_none()

        if subscription:
            subscription.status = SubscriptionStatus.PAST_DUE
            await self.db.commit()

    @staticmethod
    def get_available_plans() -> List[PlanSchema]:
        """Get list of available subscription plans."""
        # This would come from database or config
        # For now, return hardcoded plans
        return []  # TODO: Implement plan listing
