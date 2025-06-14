#!/usr/bin/env python3
import subprocess
scripts = [
    'analytics/scripts/metrics.py',
    'cloaking/scripts/cloak.py',
    'content/scripts/generate_presell.py',
    'financial/scripts/financial_tracking.py',
    'security/scripts/security_audit.py'
]
for script in scripts:
    print(f'Running {script}')
    subprocess.call(['python', script])
