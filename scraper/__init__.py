import json
from enum import Enum
from typing import Any, Dict

import requests
from bs4 import BeautifulSoup


class SalaryType(Enum):
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class IndeedScraper:
    def __init__(self, *, salary_type: SalaryType) -> None:
        self.salary_type = salary_type
        self.url_tempalte = (
            "https://www.indeed.com/career/{job_title}/salaries/{location}"
        )

    def _extract_script(self, *, soup: BeautifulSoup) -> Dict[Any, Any]:
        script = soup.find("script", {"id": "__NEXT_DATA__"})
        return json.loads(script.string)

    def _extract_salary(self, *, data: Dict[Any, Any]) -> str:
        salaries = data["props"]["pageProps"]["localSalaryAggregate"]["salaries"]
        salary = salaries["salaries"][self.salary_type.value]["estimatedMedian"]
        currency = salaries["currency"]
        return f"{round(salary, 2)} {currency}"

    def _get_soup(self, *, text: str) -> BeautifulSoup:
        return BeautifulSoup(text, "html.parser")

    def _slugify(self, *, text: str) -> str:
        return "-".join(text.lower().split())

    def scrape(self, *, job_title: str, location: str) -> str:
        response = requests.get(
            self.url_tempalte.format(
                job_title=self._slugify(text=job_title),
                location=self._slugify(text=location),
            ),
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"
            },
        )
        soup = self._get_soup(text=response.text)
        salaries = self._extract_script(soup=soup)
        salary = self._extract_salary(data=salaries)

        return salary
