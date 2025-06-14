#!/bin/bash
set -e
if [ -d .git ]; then
  git pull origin main || true
  git add .
  git commit -m "replit sync" || true
  git push origin main || true
fi
