#!/usr/bin/env python3
"""Generate status.json from running script status files."""
import json
import os
import time

STATUS_PATHS = {
    'metrics': 'analytics/scripts/metrics.status',
    'cloak': 'cloaking/scripts/cloak.status',
    'generate_presell': 'content/scripts/generate_presell.status',
    'financial_tracking': 'financial/scripts/financial_tracking.status',
    'security_audit': 'security/scripts/security_audit.status',
}
REVENUE_FILE = 'financial/scripts/revenue.txt'

while True:
    data = {'scripts': {}, 'revenue': 0.0}
    for name, path in STATUS_PATHS.items():
        status = 'stopped'
        if os.path.isfile(path):
            with open(path) as f:
                status = f.read().strip() or 'running'
        data['scripts'][name] = status
    if os.path.isfile(REVENUE_FILE):
        try:
            with open(REVENUE_FILE) as f:
                data['revenue'] = float(f.read().strip())
        except Exception:
            data['revenue'] = 0.0
    with open('status.json', 'w') as f:
        json.dump(data, f)
    time.sleep(30)
