#!/usr/bin/env python
"""Automated KPI monitoring and alerting via Slack."""

import os
import psycopg2
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()

KPI_THRESHOLDS = {
    "epc": 0.60,
    "bounce": 0.50,
}

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
DATABASE_URL = os.getenv("PG_DSN")


def get_latest_kpi(metric: str) -> float:
    """Return the latest metric value or ``None`` if not found."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT val FROM kpi WHERE metric=%s ORDER BY ts DESC LIMIT 1", (metric,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return float(result[0]) if result else None


def check_and_alert() -> None:
    """Check metrics and send Slack alerts when thresholds are breached."""
    for metric, threshold in KPI_THRESHOLDS.items():
        latest_value = get_latest_kpi(metric)
        if latest_value is not None and latest_value < threshold:
            slack_client.chat_postMessage(
                channel="#ghostflow-ops",
                text=(
                    f":rotating_light: Alert! {metric.upper()} dropped to "
                    f"{latest_value:.2f}. Immediate investigation required."
                ),
            )


if __name__ == "__main__":
    check_and_alert()
