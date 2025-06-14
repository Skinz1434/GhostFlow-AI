#!/bin/bash
# Replit ↔ GitHub Continuous Synchronization Script
echo "🔄 Starting continuous Replit ↔ GitHub sync... SkinZAI style!"

# Configure Git user explicitly
git config --global user.email "github-actions[bot]@users.noreply.github.com"
git config --global user.name "github-actions[bot]"

while true
do
    echo "🔄 Checking for changes explicitly from GitHub..."
    git pull origin main
    echo "✅ Pull completed clearly."

    echo "🔄 Pushing local Replit changes explicitly to GitHub (if any)..."
    git add .
    git commit -m "🚀 Automatic Replit sync commit" || echo "✅ Nothing new to commit explicitly."
    git push https://${GITHUB_TOKEN}@github.com/Skinz1434/GhostFlow-AI.git main || echo "⚠️ Push explicitly failed—check credentials."

    echo "🕒 Explicitly waiting 60 seconds until next sync..."
    sleep 60
done
