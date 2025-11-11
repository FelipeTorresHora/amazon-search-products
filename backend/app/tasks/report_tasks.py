"""Celery tasks for generating and sending reports."""
from celery import shared_task


@shared_task(name="app.tasks.report_tasks.send_weekly_reports")
def send_weekly_reports():
    """
    Send weekly usage and trends reports to all users.

    Runs every Sunday at 8 AM.
    """
    print("📊 Sending weekly reports...")
    # TODO: Generate and send reports
    return {"status": "success", "reports_sent": 0}


@shared_task(name="app.tasks.report_tasks.generate_user_report")
def generate_user_report(user_id: str):
    """Generate custom report for a user."""
    print(f"📈 Generating report for user: {user_id}")
    # TODO: Generate report
    return {"status": "generated", "user_id": user_id}
