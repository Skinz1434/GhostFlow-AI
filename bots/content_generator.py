#!/usr/bin/env python
"""
GhostFlow AI - Autonomous Content Generation Pipeline
Scheduled Script (runs daily via Replit Scheduled Tasks or GitHub Actions Cron)
Pulls daily keywords, generates SEO-optimized, compliant articles via GPT,
and saves Markdown files securely into the designated content directory.
"""

import os
import datetime as dt
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load secure environment variables
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# GPT system prompt (FTC, GDPR compliant)
SYSTEM_PROMPT = """
You are a creative, engaging, and witty AI copywriter for GhostFlow AI. 
Your content strictly adheres to FTC and GDPR guidelines.
Always clearly disclose affiliate relationships when discussing products or services.
Maintain a conversational yet authoritative SkinZAI-branded tone throughout.
"""

# Function to generate a single SEO-optimized article
def generate_article(keyword: str, word_count: int = 1200) -> str:
    prompt = f"""
    Write a high-quality, SEO-friendly, {word_count}-word article about "{keyword}".
    Ensure content is engaging, informative, and conversational in the distinctive SkinZAI style.
    Inject affiliate disclosures naturally and transparently wherever necessary.
    Include clear headings (H2, H3), bullet points, and FAQs for readability.
    """
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    article_content = completion.choices[0].message.content.strip()
    return article_content

# Main daily article generation workflow
def run_content_generation():
    # Load daily keywords (CSV from Ahrefs API integration)
    keyword_file = "data/daily_keywords.csv"
    try:
        kw_df = pd.read_csv(keyword_file)
    except FileNotFoundError:
        print(f"\u274c Keyword file '{keyword_file}' not found.")
        return
    except Exception as e:
        print(f"\u274c Error reading '{keyword_file}': {e}")
        return

    # Ensure output directory exists
    content_dir = "apps/content/"
    os.makedirs(content_dir, exist_ok=True)

    # Generate and save articles
    for keyword in kw_df["keyword"]:
        try:
            print(f"🖊️ Generating article for keyword: '{keyword}'...")
            article_markdown = generate_article(keyword)
            timestamp = dt.datetime.utcnow().strftime("%Y%m%d%H%M")
            safe_keyword = keyword.lower().replace(' ', '-').replace('/', '-')
            outfile = os.path.join(content_dir, f"{safe_keyword}-{timestamp}.md")

            with open(outfile, "w", encoding="utf-8") as file:
                file.write(article_markdown)

            print(f"\u2705 Article saved to '{outfile}'")
        except Exception as e:
            print(f"\u274c Error generating article for '{keyword}': {e}")

if __name__ == "__main__":
    run_content_generation()

# SkinZAI Easter Egg: If you can read this, you're as sharp as a ghost's fangs!
