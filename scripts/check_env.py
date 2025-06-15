#!/usr/bin/env python
"""Environment sanity check for GhostFlow AI.

Verifies that required environment variables are defined before running
scripts locally or in CI. This helps prevent accidental exposure of
credentials in code or logs.
"""

import os

REQUIRED_VARS = [
    "OPENAI_API_KEY",
    "STRIPE_KEY",
    "PG_DSN",
    "SLACK_BOT_TOKEN",
    "GF_ENC_KEY",
]

missing = [var for var in REQUIRED_VARS if not os.getenv(var)]

if missing:
    print("Missing required variables:", ", ".join(missing))
    raise SystemExit(1)
else:
    print("All environment variables set. \U0001F6E0")
