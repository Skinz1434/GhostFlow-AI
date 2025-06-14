#!/usr/bin/env python3
"""Simple analytics metrics collector."""
import os
import signal
import sys
import time

STATUS_FILE = os.path.join(os.path.dirname(__file__), 'metrics.status')

def write_status(state: str) -> None:
    with open(STATUS_FILE, 'w') as f:
        f.write(state)

def cleanup(*_):
    write_status('stopped')
    sys.exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

while True:
    print('Metrics collected successfully')
    write_status('running')
    time.sleep(10)
