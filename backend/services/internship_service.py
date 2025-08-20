import os
import requests
from dotenv import load_dotenv

load_dotenv()

SCRAPINGDOG_API_KEY = os.getenv("SCRAPINGDOG_API_KEY")
BASE_URL = "https://api.scrapingdog.com/linkedinjobs/"

async def fetch_internships(field: str, location: str = "Worldwide", geoid: str = "92000000",
                            page: int = 1, sort_by: str = "week"):
    """
    Fetch internships via ScrapingDog LinkedIn Jobs API.
    Defaults: global geoid, last 7 days, exp_level=internship.
    """
    if not SCRAPINGDOG_API_KEY:
        return []

    params = {
        "api_key": SCRAPINGDOG_API_KEY,
        "field": field,
        "location": location,
        "geoid": geoid,
        "page": str(page),
        "sort_by": sort_by,          # day | week | month
        "exp_level": "internship",   # filter for internships
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=45)
        resp.raise_for_status()
        jobs = resp.json() or []
        jobs = jobs[:8]  # small cap for UI
        results = []
        for j in jobs:
            results.append({
                "title": j.get("job_position") or "Internship",
                "company": j.get("company_name") or "Unknown",
                "location": j.get("job_location") or "",
                "site": "LinkedIn",
                "date_posted": j.get("job_posting_date") or "",
                "url": j.get("job_link") or "",
            })
        return results
    except Exception:
        return []
