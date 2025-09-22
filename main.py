from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from database import get_connection
from scraper import fetch_and_store_jobs
from scheduler import start_scheduler

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Start the background scheduler
start_scheduler(interval_minutes=60)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/jobs")
def get_jobs():
    print("get_jobs")
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM jobs ORDER BY published_date DESC")
    jobs = [dict(zip([column[0] for column in c.description], row)) for row in c.fetchall()]
    print(jobs)
    return JSONResponse(content=jobs)

@app.get("/api/check-now")
def manual_check():
    print("manual_check")
    jobs = fetch_and_store_jobs()
    print(jobs)
    return JSONResponse(content={"message": f"{len(jobs)} jobs fetched"})