"""
Celery application configuration for background tasks.
"""
from celery import Celery
from celery.schedules import crontab

from app.config import settings

# Create Celery app
celery_app = Celery(
    "amazon_search",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,  # For testing
)

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    "scrape-products-hourly": {
        "task": "app.tasks.scraper_tasks.scrape_all_categories",
        "schedule": crontab(minute=0),  # Every hour
    },
    "check-alerts-every-15min": {
        "task": "app.tasks.alert_tasks.check_all_alerts",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
    },
    "cleanup-old-data-daily": {
        "task": "app.tasks.cleanup_tasks.cleanup_old_data",
        "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    "send-usage-reports-weekly": {
        "task": "app.tasks.report_tasks.send_weekly_reports",
        "schedule": crontab(day_of_week=0, hour=8, minute=0),  # Sundays at 8 AM
    },
}

# Auto-discover tasks
celery_app.autodiscover_tasks(["app.tasks"])
