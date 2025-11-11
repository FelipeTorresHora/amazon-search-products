"""Celery tasks for cleanup and maintenance."""

from celery import shared_task


@shared_task(name="app.tasks.cleanup_tasks.cleanup_old_data")
def cleanup_old_data():
    """
    Cleanup old data based on user subscription plan.

    - Free: Keep 30 days
    - Pro: Keep 6 months
    - Business+: Keep unlimited

    Runs daily at 3 AM.
    """
    print("🧹 Cleaning up old data...")
    # TODO: Implement cleanup logic
    return {"status": "success", "rows_deleted": 0}
