from typing import Optional

from fastapi import FastAPI

from scraper import IndeedScraper, SalaryType

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/salary/")
async def salary(salary_type: SalaryType, job_title: str, location: Optional[str] = ""):
    scraper = IndeedScraper(salary_type=salary_type)
    salary = scraper.scrape(job_title=job_title, location=location)
    return {"salary": salary}
