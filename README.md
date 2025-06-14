# GhostFlow AI

This repository contains a prototype of the GhostFlow AI automation system.
It provides simple scripts for analytics, cloaking, content generation,
financial tracking and security auditing.

## Setup
Run the setup script to create required directories:
```bash
bash scripts/setup.sh
```

## Running
In a Replit environment the `.replit` file launches all core scripts and the
GitHub sync service automatically. You can also run them manually:
```bash
bash scripts/replit.sync.sh &
python analytics/scripts/metrics.py &
python cloaking/scripts/cloak.py &
python content/scripts/generate_presell.py &
python financial/scripts/financial_tracking.py &
python security/scripts/security_audit.py &
python scripts/generate_status.py
```

Open `dashboard.html` in the Replit web view to see live metrics.
