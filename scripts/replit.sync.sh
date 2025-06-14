#!/bin/bash
echo "🔄 Starting continuous sync clearly (Replit ↔ GitHub)..."
while true; do
  git pull origin main
  git add .
  git commit -m "🚀 Auto-sync commit by Replit" || echo "✅ No changes detected explicitly."
  git push https://${GITHUB_TOKEN}@github.com/Skinz1434/GhostFlow-AI.git main
  sleep 60
done
