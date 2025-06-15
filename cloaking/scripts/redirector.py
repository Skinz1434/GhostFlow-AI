#!/usr/bin/env python
"""FastAPI service for cloaking and tracking affiliate links."""

import os
from fastapi import FastAPI, Request, HTTPException
import re
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
import psycopg2
import psycopg2.pool

load_dotenv()
app = FastAPI()

DATABASE_URL = os.getenv("PG_DSN")

# initialize a simple connection pool
pool = psycopg2.pool.SimpleConnectionPool(1, 20, DATABASE_URL) if DATABASE_URL else None


def record_click(slug: str, ip: str, user_agent: str) -> None:
    """Insert a click record using a pooled connection."""
    if pool is None:
        return
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO clicks(tag, ip, ua) VALUES(%s,%s,%s)",
                (slug, ip, user_agent),
            )
            conn.commit()
    finally:
        pool.putconn(conn)


@app.get("/out/{slug}")
async def redirect_affiliate_link(slug: str, request: Request):
    """Redirect to the affiliate link while tracking the click."""
    if not re.match(r"^[a-zA-Z0-9_-]+$", slug):
        raise HTTPException(status_code=400, detail="Invalid slug")
    target_url = os.getenv(f"AFF_{slug.upper()}")
    if not target_url:
        raise HTTPException(status_code=404, detail="Invalid link")

    ip = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")
    record_click(slug, ip, user_agent)

    response = RedirectResponse(
        url=f"{target_url}?utm_source=ghostflow&utm_medium=redirect", status_code=302
    )
    response.headers["Cache-Control"] = "no-store"
    return response

# SkinZAI Easter Egg: This redirector zips faster than a ghost on roller skates!

