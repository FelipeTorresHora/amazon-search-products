"""Product service - Amazon product search and analysis."""
from typing import List, Dict, Any, Optional
import httpx
from datetime import datetime, timedelta
import pandas as pd

from app.config import settings
from app.schemas.product import (
    ProductSearchFilters,
    ProductSearchResponse,
    ProductSearchResult,
    ProductDetail,
)


class ProductService:
    """Service for Amazon product search and data retrieval."""

    def __init__(self):
        self.api_key = settings.RAPIDAPI_KEY
        self.api_host = settings.RAPIDAPI_HOST
        self.base_url = settings.RAPIDAPI_BASE_URL
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host,
        }

    async def search_products(
        self, filters: ProductSearchFilters
    ) -> ProductSearchResponse:
        """
        Search Amazon products with filters.

        Uses RapidAPI Amazon Data API.
        """
        try:
            # For demo purposes, use local CSV data if available
            # In production, this would call the actual API
            products = await self._search_local_data(filters)

            return ProductSearchResponse(
                products=products,
                total=len(products),
                page=filters.page,
                per_page=filters.per_page,
                total_pages=(len(products) + filters.per_page - 1) // filters.per_page
            )

        except Exception as e:
            print(f"Error searching products: {e}")
            # Return empty results on error
            return ProductSearchResponse(
                products=[],
                total=0,
                page=filters.page,
                per_page=filters.per_page,
                total_pages=0
            )

    async def _search_local_data(
        self, filters: ProductSearchFilters
    ) -> List[ProductSearchResult]:
        """
        Search products from local CSV data.

        TODO: Replace with actual API call in production.
        """
        try:
            # Map category names
            category_map = {
                "eletronicos": "eletronicos",
                "beleza": "beleza",
                "brinquedos": "brinquedo",
                "construcao": "construcao",
                "pet": "pet",
            }

            category = category_map.get(filters.category, "beleza")
            csv_path = f"./dados/{category}/atual/{category}_produtos.csv"

            # Read CSV
            df = pd.read_csv(csv_path)

            # Filter by query (search in title)
            if filters.query:
                df = df[
                    df["product_title"].str.contains(
                        filters.query, case=False, na=False
                    )
                ]

            # Filter by price
            if filters.min_price is not None:
                df["price_numeric"] = df["product_price"].str.replace(
                    "R$ ", ""
                ).str.replace(",", ".").astype(float, errors="ignore")
                df = df[df["price_numeric"] >= filters.min_price]

            if filters.max_price is not None:
                df = df[df["price_numeric"] <= filters.max_price]

            # Filter by rating
            if filters.min_rating is not None:
                df["rating_numeric"] = pd.to_numeric(
                    df["product_star_rating"], errors="coerce"
                )
                df = df[df["rating_numeric"] >= filters.min_rating]

            # Filter by Prime
            if filters.is_prime:
                df = df[df["is_prime"] == True]

            # Sort
            if filters.sort_by == "price_asc":
                df = df.sort_values("price_numeric", ascending=True)
            elif filters.sort_by == "price_desc":
                df = df.sort_values("price_numeric", ascending=False)
            elif filters.sort_by == "rating":
                df = df.sort_values("rating_numeric", ascending=False)

            # Pagination
            start = (filters.page - 1) * filters.per_page
            end = start + filters.per_page
            df = df.iloc[start:end]

            # Convert to response format
            products = []
            for _, row in df.iterrows():
                products.append(
                    ProductSearchResult(
                        asin=row.get("asin", ""),
                        title=row.get("product_title", ""),
                        price=self._parse_price(row.get("product_price")),
                        rating=self._parse_rating(row.get("product_star_rating")),
                        num_ratings=self._parse_int(row.get("product_num_ratings")),
                        image_url=row.get("product_photo"),
                        product_url=row.get("product_url", ""),
                        is_prime=row.get("is_prime", False),
                        sales_volume=row.get("sales_volume"),
                        category=category,
                    )
                )

            return products

        except Exception as e:
            print(f"Error reading local data: {e}")
            return []

    async def get_product_detail(self, asin: str) -> Optional[ProductDetail]:
        """Get detailed product information by ASIN."""
        # TODO: Implement API call or database query
        return None

    async def get_product_history(self, asin: str) -> Dict[str, Any]:
        """Get price and rating history for a product."""
        # TODO: Implement historical data retrieval
        return {
            "asin": asin,
            "price_history": [],
            "rating_history": [],
        }

    async def _call_amazon_api(
        self, endpoint: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call RapidAPI Amazon Data API.

        This is the actual API call implementation.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=params,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    def _parse_price(price_str: Any) -> Optional[float]:
        """Parse price string to float."""
        try:
            if pd.isna(price_str):
                return None
            price_clean = str(price_str).replace("R$ ", "").replace(",", ".")
            return float(price_clean)
        except:
            return None

    @staticmethod
    def _parse_rating(rating_str: Any) -> Optional[float]:
        """Parse rating string to float."""
        try:
            if pd.isna(rating_str):
                return None
            return float(rating_str)
        except:
            return None

    @staticmethod
    def _parse_int(value: Any) -> Optional[int]:
        """Parse value to int."""
        try:
            if pd.isna(value):
                return None
            return int(value)
        except:
            return None
