#!/usr/bin/env python
"""Publish generated markdown articles to an external site."""
import os
import glob
import requests
import markdown
from dotenv import load_dotenv

load_dotenv()
API_ENDPOINT = os.getenv("SITE_API_ENDPOINT")
API_KEY = os.getenv("SITE_API_KEY")


def publish_markdown(md_file: str) -> None:
    """Convert markdown to HTML and post it to the target site."""
    with open(md_file, "r", encoding="utf-8") as file:
        md_content = file.read()
    html_content = markdown.markdown(md_content)

    data = {
        "api_key": API_KEY,
        "title": os.path.basename(md_file).replace(".md", "").replace("-", " ").title(),
        "content": html_content,
        "seo_metadata": {
            "description": "Learn about " + os.path.basename(md_file).replace(".md", ""),
            "keywords": ", ".join(os.path.basename(md_file).split("-")),
        },
    }
    resp = requests.post(API_ENDPOINT, json=data)
    if resp.ok:
        print(f"✅ Published successfully: {md_file}")
    else:
        print(f"❌ Publishing failed for {md_file}: {resp.text}")


if __name__ == "__main__":
    for path in glob.glob("apps/content/*.md"):
        publish_markdown(path)
