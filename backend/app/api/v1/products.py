"""Product search and analysis API endpoints."""
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.product import (
    ProductSearchFilters,
    ProductSearchResponse,
    ProductDetail,
    BulkSearchRequest,
    BulkSearchResponse,
)
from app.services.product_service import ProductService
from app.services.subscription_service import SubscriptionService
from app.core.security import get_current_active_user, check_user_plan
from app.models.user import User

router = APIRouter()


@router.get("/search", response_model=ProductSearchResponse)
async def search_products(
    q: str = Query(..., description="Search query"),
    category: str = Query("all", description="Product category"),
    min_price: float = Query(None, description="Minimum price"),
    max_price: float = Query(None, description="Maximum price"),
    min_rating: float = Query(None, description="Minimum rating"),
    is_prime: bool = Query(None, description="Prime only"),
    sort_by: str = Query("relevance", description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Search Amazon products with filters.

    Requires: Active subscription with available search quota.
    """
    # Check usage quota
    subscription_service = SubscriptionService(db)
    can_search = await subscription_service.increment_usage(
        current_user.id, "searches"
    )

    if not can_search:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Search quota exceeded. Please upgrade your plan."
        )

    # Build filters
    filters = ProductSearchFilters(
        query=q,
        category=category if category != "all" else None,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        is_prime=is_prime,
        sort_by=sort_by,
        page=page,
        per_page=per_page
    )

    # Search products
    product_service = ProductService()
    results = await product_service.search_products(filters)

    return results


@router.get("/{asin}", response_model=ProductDetail)
async def get_product(
    asin: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get product details by ASIN."""
    product_service = ProductService()
    product = await product_service.get_product_detail(asin)

    if not product:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {asin} not found"
        )

    return product


@router.get("/{asin}/history")
async def get_product_history(
    asin: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get price and rating history for a product."""
    product_service = ProductService()
    history = await product_service.get_product_history(asin)

    return history


@router.post("/bulk-search", response_model=BulkSearchResponse)
async def bulk_search(
    request: BulkSearchRequest,
    current_user: User = Depends(check_user_plan("business"))
):
    """
    Search multiple products at once.

    Requires: Business+ plan
    """
    # TODO: Implement bulk search
    return BulkSearchResponse(
        products=[],
        found=0,
        not_found=request.asins
    )
