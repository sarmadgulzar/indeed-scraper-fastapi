from typing import Optional

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from scraper import IndeedScraper, SalaryType

app = FastAPI()


app.mount("/static", StaticFiles(directory="assets"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/salary/")
async def salary(salary_type: SalaryType, job_title: str, location: Optional[str] = ""):
    scraper = IndeedScraper(salary_type=salary_type)
    salary = scraper.scrape(job_title=job_title, location=location)
    return {"salary": salary}
