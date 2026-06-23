import requests
import pandas as pd
import time
import re
from datetime import datetime

# Arbeitnow has a free public API - no key needed, which is why I went with it.
# Tried a few others (Adzuna, Indeed) but they require approval or have rate limits
# that make scraping annoying for a side project like this.
# API docs: https://www.arbeitnow.com/api/job-board-api

# roles I actually care about for my own job search - adjust as needed
TARGET_TITLES = [
    "werkstudent", "working student", "intern", "praktikant",
    "business development", "strategy", "consulting", "operations",
    "analyst", "junior", "associate", "marketing", "growth",
    "project management", "product", "venture", "startup"
]

TARGET_LOCATIONS = ["berlin", "remote"]

MAX_PAGES = 10
SLEEP_BETWEEN = 0.6  # don't hammer the API
OUTPUT_FILE = "raw_jobs.csv"
API_URL = "https://www.arbeitnow.com/api/job-board-api"


def clean_html(raw):
    # job descriptions come back as messy HTML, this strips it down to plain text
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_relevant(job):
    title = (job.get("title") or "").lower()
    location = (job.get("location") or "").lower()
    title_match = any(kw in title for kw in TARGET_TITLES)
    location_match = any(loc in location for loc in TARGET_LOCATIONS)
    return title_match and location_match


def fetch_page(page):
    try:
        resp = requests.get(API_URL, params={"page": page}, timeout=15)
        resp.raise_for_status()
        return resp.json().get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"  page {page} failed: {e}")
        return []


def scrape_jobs():
    print(f"scraping jobs — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"fetching up to {MAX_PAGES} pages...\n")

    all_relevant = []

    for page in range(1, MAX_PAGES + 1):
        jobs = fetch_page(page)
        if not jobs:
            print(f"  page {page}: empty, stopping")
            break

        relevant = [j for j in jobs if is_relevant(j)]
        all_relevant.extend(relevant)
        print(f"  page {page}: {len(jobs)} total, {len(relevant)} matched ({len(all_relevant)} so far)")
        time.sleep(SLEEP_BETWEEN)

    if not all_relevant:
        print("\nno relevant jobs found - try broadening TARGET_TITLES or check your connection")
        return

    rows = []
    for job in all_relevant:
        rows.append({
            "title":       job.get("title", ""),
            "company":     job.get("company_name", ""),
            "location":    job.get("location", ""),
            "remote":      job.get("remote", False),
            "url":         job.get("url", ""),
            "created_at":  job.get("created_at", ""),
            "tags":        ", ".join(job.get("tags", [])),
            "description": clean_html(job.get("description", "")),
        })

    df = pd.DataFrame(rows).drop_duplicates(subset=["title", "company"])
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"\ndone — {len(df)} unique jobs saved to {OUTPUT_FILE}")
    return df


if __name__ == "__main__":
    scrape_jobs()
