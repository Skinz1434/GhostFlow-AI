#!/usr/bin/env python
"""Serverless functions for analytics and KPI monitoring."""

import os
import json
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

GTM_ENDPOINT = "https://www.googletagmanager.com/collect"
DATABASE_URL = os.getenv("PG_DSN")


def lambda_handler(event, context):
    """Proxy events to Google Tag Manager with EU consent check."""
    event_body = json.loads(event.get('body', '{}'))
    if event_body.get('euConsent') is False:
        return {'statusCode': 204}

    headers = {'Content-Type': 'application/json'}
    response = requests.post(GTM_ENDPOINT, json=event_body, headers=headers)
    if response.status_code == 200:
        return {'statusCode': 200}
    print(f"\u274c GTM Proxy Error: {response.status_code} - {response.text}")
    return {'statusCode': response.status_code}


def ingest_kpi_event(event, context):
    """Store KPI metrics in PostgreSQL for Metabase dashboards."""
    payload = json.loads(event.get('body', '{}'))
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO kpi (metric, val) VALUES (%s, %s)",
            (payload['metric'], payload['val'])
        )
        conn.commit()
        print(f"\u2705 Successfully ingested KPI: {payload['metric']} = {payload['val']}")
        return {'statusCode': 200}
    except Exception as e:
        print(f"\u274c KPI ingestion failed: {e}")
        conn.rollback()
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
    finally:
        cursor.close()
        conn.close()
