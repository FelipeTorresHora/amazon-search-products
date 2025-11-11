"""Product Pydantic schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


# =============================================================================
# PRODUCT SCHEMAS
# =============================================================================


class ProductBase(BaseModel):
    """Base product schema."""

    asin: str = Field(..., min_length=10, max_length=10)
    title: str
    price: Optional[float] = None
    currency: str = "BRL"
    rating: Optional[float] = Field(None, ge=0, le=5)
    num_ratings: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None


class ProductDetail(ProductBase):
    """Detailed product information."""

    original_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    product_url: HttpUrl
    image_url: Optional[HttpUrl] = None
    is_prime: bool = False
    is_best_seller: bool = False
    is_amazon_choice: bool = False
    sales_volume: Optional[str] = None
    delivery_info: Optional[str] = None
    num_offers: Optional[int] = None
    minimum_offer_price: Optional[float] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None


class ProductSearchResult(BaseModel):
    """Product search result item."""

    asin: str
    title: str
    price: Optional[float]
    rating: Optional[float]
    num_ratings: Optional[int]
    image_url: Optional[str]
    product_url: str
    is_prime: bool = False
    sales_volume: Optional[str] = None
    category: str


class ProductSearchResponse(BaseModel):
    """Product search response with pagination."""

    products: List[ProductSearchResult]
    total: int
    page: int = 1
    per_page: int = 20
    total_pages: int


class ProductSearchFilters(BaseModel):
    """Filters for product search."""

    query: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = Field(
        None, pattern="^(eletronicos|beleza|brinquedos|construcao|pet|all)$"
    )
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    is_prime: Optional[bool] = None
    sort_by: Optional[str] = Field(
        "relevance", pattern="^(relevance|price_asc|price_desc|rating|popularity)$"
    )
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class BulkSearchRequest(BaseModel):
    """Bulk product search (Business+ only)."""

    asins: List[str] = Field(..., min_length=1, max_length=100)


class BulkSearchResponse(BaseModel):
    """Bulk search response."""

    products: List[ProductDetail]
    found: int
    not_found: List[str]


# =============================================================================
# PRODUCT HISTORY
# =============================================================================


class PricePoint(BaseModel):
    """Single price data point."""

    date: datetime
    price: float
    discount: Optional[float] = None


class RatingPoint(BaseModel):
    """Single rating data point."""

    date: datetime
    rating: float
    num_ratings: int


class ProductHistory(BaseModel):
    """Historical product data."""

    asin: str
    title: str
    current_price: Optional[float]
    price_history: List[PricePoint]
    rating_history: List[RatingPoint]
    lowest_price: Optional[float]
    highest_price: Optional[float]
    average_price: Optional[float]
    price_trend: str = Field(..., pattern="^(increasing|decreasing|stable)$")


# =============================================================================
# ANALYTICS
# =============================================================================


class CategoryAnalytics(BaseModel):
    """Analytics for a product category."""

    category: str
    total_products: int
    average_price: float
    median_price: float
    average_rating: float
    total_reviews: int
    best_sellers_count: int
    price_range: dict  # {"min": float, "max": float}


class MarketTrends(BaseModel):
    """Market trends data."""

    category: str
    period: str  # "7d", "30d", "90d"
    price_trend: str
    popular_products: List[ProductSearchResult]
    trending_up: List[str]  # ASINs
    trending_down: List[str]  # ASINs
