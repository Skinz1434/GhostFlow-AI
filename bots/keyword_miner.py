#!/usr/bin/env python
"""Fetch top keywords from Ahrefs and store them to CSV."""
import os
import requests
import csv
import datetime
from dotenv import load_dotenv

load_dotenv()
AHREFS_API_TOKEN = os.getenv("AHREFS_API_TOKEN")
TARGET_KEYWORD = "affiliate marketing"
KEYWORD_LIMIT = 100
OUTPUT_CSV = "data/daily_keywords.csv"


def fetch_keywords():
    """Fetch keywords from Ahrefs API."""
    params = {
        "token": AHREFS_API_TOKEN,
        "from": "keywords_explorer",
        "target": TARGET_KEYWORD,
        "mode": "phrase_match",
        "output": "json",
    }
    response = requests.get("https://apiv2.ahrefs.com", params=params)
    response.raise_for_status()
    return response.json().get("keywords", [])[:KEYWORD_LIMIT]


def save_keywords(keywords):
    """Save a list of keywords to CSV."""
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["keyword"])
        writer.writeheader()
        for item in keywords:
            writer.writerow({"keyword": item.get("keyword")})
    print(f"✅ Keywords saved → {OUTPUT_CSV}")


if __name__ == "__main__":
    print(f"🚧 Fetching keywords at {datetime.datetime.utcnow()}")
    kw_list = fetch_keywords()
    save_keywords(kw_list)
