from apscheduler.schedulers.background import BackgroundScheduler
from scraper import fetch_and_store_jobs

scheduler = BackgroundScheduler()

def start_scheduler(interval_minutes=3600):
    scheduler.add_job(fetch_and_store_jobs, 'interval', minutes=interval_minutes, id='fetch_jobs', replace_existing=True)
    scheduler.start()