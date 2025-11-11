"""
FastAPI main application module.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.config import settings
from app.api.v1 import auth, users, products, subscriptions, alerts, analytics


# Initialize Sentry for error tracking (production)
if settings.SENTRY_DSN and settings.is_production:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENVIRONMENT,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        integrations=[FastApiIntegration()],
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📦 Environment: {settings.ENVIRONMENT}")
    print(f"🔧 Debug mode: {settings.DEBUG}")

    # TODO: Initialize database connection pool
    # TODO: Initialize Redis connection
    # TODO: Warm up caches if needed

    yield

    # Shutdown
    print("👋 Shutting down gracefully...")
    # TODO: Close database connections
    # TODO: Close Redis connections
    # TODO: Cleanup resources


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SaaS platform for Amazon Brazil product analysis and market intelligence",
    docs_url=f"{settings.API_V1_PREFIX}/docs" if settings.DEBUG else None,
    redoc_url=f"{settings.API_V1_PREFIX}/redoc" if settings.DEBUG else None,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)


# =============================================================================
# MIDDLEWARE
# =============================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression for responses > 1KB
app.add_middleware(GZipMiddleware, minimum_size=1000)


# =============================================================================
# EXCEPTION HANDLERS
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    # Log the error (would be sent to Sentry in production)
    print(f"❌ Unhandled error: {exc}")

    # Don't expose internal errors in production
    if settings.is_production:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error. Please try again later."}
        )

    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


# =============================================================================
# ROOT ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "operational",
        "docs": f"{settings.API_V1_PREFIX}/docs" if settings.DEBUG else None,
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    # TODO: Add checks for:
    # - Database connectivity
    # - Redis connectivity
    # - External API availability

    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
    }


@app.get("/readiness")
async def readiness_check():
    """
    Readiness check for Kubernetes deployments.
    """
    # TODO: Verify all dependencies are ready
    return {"status": "ready"}


# =============================================================================
# API ROUTERS
# =============================================================================

# Authentication & Authorization
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"]
)

# User Management
app.include_router(
    users.router,
    prefix=f"{settings.API_V1_PREFIX}/users",
    tags=["Users"]
)

# Product Search & Analysis
app.include_router(
    products.router,
    prefix=f"{settings.API_V1_PREFIX}/products",
    tags=["Products"]
)

# Subscriptions & Billing
app.include_router(
    subscriptions.router,
    prefix=f"{settings.API_V1_PREFIX}/subscriptions",
    tags=["Subscriptions"]
)

# Price & Stock Alerts
app.include_router(
    alerts.router,
    prefix=f"{settings.API_V1_PREFIX}/alerts",
    tags=["Alerts"]
)

# Analytics & Reporting
app.include_router(
    analytics.router,
    prefix=f"{settings.API_V1_PREFIX}/analytics",
    tags=["Analytics"]
)


# =============================================================================
# STARTUP MESSAGE
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  🚀 {settings.APP_NAME} v{settings.APP_VERSION}                     ║
    ║                                                              ║
    ║  📊 Amazon Product Analysis SaaS Platform                   ║
    ║  🌍 Environment: {settings.ENVIRONMENT.upper().center(39)} ║
    ║  🔧 Debug: {str(settings.DEBUG).center(47)} ║
    ║                                                              ║
    ║  📖 API Docs: http://localhost:8000{settings.API_V1_PREFIX}/docs       ║
    ║  ❤️  Health: http://localhost:8000/health                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
