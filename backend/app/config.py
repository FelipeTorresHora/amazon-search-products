"""
Application configuration management.
Loads settings from environment variables with validation.
"""
from typing import List, Optional, Any
from pydantic import Field, field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    """Application settings with environment variable loading."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # =============================================================================
    # APPLICATION
    # =============================================================================
    APP_NAME: str = "Amazon Search Products"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    API_V1_PREFIX: str = "/api/v1"

    # =============================================================================
    # DATABASE
    # =============================================================================
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/amazon_search"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 0
    DB_ECHO: bool = False

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure database URL is valid."""
        if not v.startswith("postgresql"):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v

    # =============================================================================
    # REDIS
    # =============================================================================
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # 1 hour

    # =============================================================================
    # CELERY
    # =============================================================================
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_TASK_ALWAYS_EAGER: bool = False
    CELERY_TASK_SOFT_TIME_LIMIT: int = 300
    CELERY_TASK_TIME_LIMIT: int = 600

    # =============================================================================
    # JWT
    # =============================================================================
    JWT_SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    JWT_REFRESH_TOKEN_COOKIE_SECURE: bool = False

    # =============================================================================
    # CORS
    # =============================================================================
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:8501",
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    FRONTEND_URL: str = "http://localhost:8501"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v

    # =============================================================================
    # AMAZON API (RapidAPI)
    # =============================================================================
    RAPIDAPI_KEY: str = ""
    RAPIDAPI_HOST: str = "real-time-amazon-data.p.rapidapi.com"
    RAPIDAPI_BASE_URL: str = "https://real-time-amazon-data.p.rapidapi.com"
    AMAZON_API_RATE_LIMIT: int = 1000
    AMAZON_API_DELAY: int = 1

    # =============================================================================
    # STRIPE
    # =============================================================================
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_CURRENCY: str = "BRL"
    STRIPE_SUCCESS_URL: str = "http://localhost:8501/success"
    STRIPE_CANCEL_URL: str = "http://localhost:8501/cancel"

    STRIPE_PRICE_ID_PRO: Optional[str] = None
    STRIPE_PRICE_ID_BUSINESS: Optional[str] = None
    STRIPE_PRICE_ID_ENTERPRISE: Optional[str] = None

    # =============================================================================
    # EMAIL (SendGrid)
    # =============================================================================
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = "noreply@amazonanalytics.com.br"
    SENDGRID_FROM_NAME: str = "Amazon Analytics"
    EMAIL_TEMPLATES_DIR: str = "./email_templates"

    # =============================================================================
    # AWS
    # =============================================================================
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "amazon-search-products-data"
    AWS_CLOUDFRONT_DOMAIN: Optional[str] = None

    # =============================================================================
    # MONITORING
    # =============================================================================
    SENTRY_DSN: Optional[str] = None
    SENTRY_ENVIRONMENT: str = "development"
    SENTRY_TRACES_SAMPLE_RATE: float = 1.0

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE: Optional[str] = None

    # =============================================================================
    # RATE LIMITING (per minute)
    # =============================================================================
    RATE_LIMIT_FREE: int = 10
    RATE_LIMIT_PRO: int = 100
    RATE_LIMIT_BUSINESS: int = 1000
    RATE_LIMIT_ENTERPRISE: int = 10000

    # =============================================================================
    # USAGE LIMITS (per month)
    # =============================================================================
    USAGE_LIMIT_FREE_SEARCHES: int = 50
    USAGE_LIMIT_FREE_ALERTS: int = 5
    USAGE_LIMIT_PRO_SEARCHES: int = 1000
    USAGE_LIMIT_PRO_ALERTS: int = 50
    USAGE_LIMIT_BUSINESS_SEARCHES: int = 5000
    USAGE_LIMIT_BUSINESS_ALERTS: int = 200

    # =============================================================================
    # ADMIN
    # =============================================================================
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis123!"
    FIRST_SUPERUSER_NAME: str = "Admin User"

    # =============================================================================
    # TESTING
    # =============================================================================
    TEST_DATABASE_URL: Optional[str] = None
    TEST_REDIS_URL: Optional[str] = None

    # =============================================================================
    # WORKER
    # =============================================================================
    WORKER_CONCURRENCY: int = 4
    WORKER_MAX_TASKS_PER_CHILD: int = 1000
    WORKER_PREFETCH_MULTIPLIER: int = 4

    # =============================================================================
    # STREAMLIT
    # =============================================================================
    STREAMLIT_SERVER_PORT: int = 8501
    STREAMLIT_SERVER_ADDRESS: str = "0.0.0.0"
    STREAMLIT_THEME_PRIMARY_COLOR: str = "#FF4B4B"
    STREAMLIT_BROWSER_GATHER_USAGE_STATS: bool = False

    # =============================================================================
    # FEATURE FLAGS
    # =============================================================================
    FEATURE_OAUTH_ENABLED: bool = False
    FEATURE_2FA_ENABLED: bool = False
    FEATURE_API_PUBLIC_ACCESS: bool = False
    FEATURE_WEBHOOKS_ENABLED: bool = False
    FEATURE_WHITE_LABEL: bool = False

    # =============================================================================
    # METRICS
    # =============================================================================
    ENABLE_METRICS: bool = True
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3001

    # =============================================================================
    # ELASTICSEARCH
    # =============================================================================
    ELASTICSEARCH_URL: Optional[str] = None
    ELASTICSEARCH_INDEX: str = "products"

    # =============================================================================
    # SECURITY
    # =============================================================================
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    SECURE_SSL_REDIRECT: bool = False
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "lax"

    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGIT: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = False

    # =============================================================================
    # BACKUP
    # =============================================================================
    BACKUP_ENABLED: bool = True
    BACKUP_SCHEDULE: str = "0 2 * * *"
    BACKUP_RETENTION_DAYS: int = 30
    BACKUP_S3_BUCKET: str = "amazon-search-backups"

    # =============================================================================
    # HELPER METHODS
    # =============================================================================

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT.lower() == "development"

    @property
    def is_testing(self) -> bool:
        """Check if running in testing."""
        return self.ENVIRONMENT.lower() == "testing"

    def get_rate_limit(self, plan: str) -> int:
        """Get rate limit for a subscription plan."""
        rate_limits = {
            "free": self.RATE_LIMIT_FREE,
            "pro": self.RATE_LIMIT_PRO,
            "business": self.RATE_LIMIT_BUSINESS,
            "enterprise": self.RATE_LIMIT_ENTERPRISE,
        }
        return rate_limits.get(plan.lower(), self.RATE_LIMIT_FREE)

    def get_usage_limit(self, plan: str, limit_type: str = "searches") -> int:
        """Get usage limit for a subscription plan and type."""
        limits = {
            "free": {
                "searches": self.USAGE_LIMIT_FREE_SEARCHES,
                "alerts": self.USAGE_LIMIT_FREE_ALERTS,
            },
            "pro": {
                "searches": self.USAGE_LIMIT_PRO_SEARCHES,
                "alerts": self.USAGE_LIMIT_PRO_ALERTS,
            },
            "business": {
                "searches": self.USAGE_LIMIT_BUSINESS_SEARCHES,
                "alerts": self.USAGE_LIMIT_BUSINESS_ALERTS,
            },
            "enterprise": {
                "searches": 999999,  # Unlimited
                "alerts": 999999,
            },
        }
        return limits.get(plan.lower(), {}).get(limit_type, 0)

    def get_stripe_price_id(self, plan: str) -> Optional[str]:
        """Get Stripe price ID for a plan."""
        price_ids = {
            "pro": self.STRIPE_PRICE_ID_PRO,
            "business": self.STRIPE_PRICE_ID_BUSINESS,
            "enterprise": self.STRIPE_PRICE_ID_ENTERPRISE,
        }
        return price_ids.get(plan.lower())


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    This function is cached to avoid reloading settings on every call.
    """
    return Settings()


# Convenience instance for importing
settings = get_settings()


# Development helper to print all settings (without secrets)
if __name__ == "__main__":
    import json

    settings_dict = settings.model_dump()

    # Mask sensitive values
    sensitive_keys = [
        "SECRET_KEY", "JWT_SECRET_KEY", "DATABASE_URL", "REDIS_URL",
        "RAPIDAPI_KEY", "STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET",
        "SENDGRID_API_KEY", "AWS_SECRET_ACCESS_KEY", "SENTRY_DSN",
        "FIRST_SUPERUSER_PASSWORD"
    ]

    for key in sensitive_keys:
        if key in settings_dict and settings_dict[key]:
            settings_dict[key] = "***REDACTED***"

    print(json.dumps(settings_dict, indent=2))
