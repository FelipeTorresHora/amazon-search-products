"""Celery tasks for scraping Amazon products."""
from celery import shared_task


@shared_task(name="app.tasks.scraper_tasks.scrape_all_categories")
def scrape_all_categories():
    """
    Scrape all product categories and update database.

    Runs hourly via Celery Beat.
    """
    print("🔄 Scraping all categories...")
    # TODO: Implement actual scraping logic
    return {"status": "success", "categories_scraped": 5}


@shared_task(name="app.tasks.scraper_tasks.scrape_category")
def scrape_category(category: str):
    """Scrape specific category."""
    print(f"🔄 Scraping category: {category}")
    # TODO: Implement scraping for category
    return {"status": "success", "category": category}
