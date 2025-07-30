#!/bin/bash

# AI Web Scraper - Commit and Push Script
# This script commits changes and pushes them to GitHub

echo "📝 AI Web Scraper - Commit and Push"
echo "=================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository."
    echo "Please run this script from the AIWebscraper directory."
    exit 1
fi

# Check if there are any changes to commit
if git diff-index --quiet HEAD --; then
    echo "ℹ️  No changes to commit."
    echo "All files are up to date!"
    exit 0
fi

# Show current status
echo "📊 Current git status:"
git status --short
echo ""

# Get commit message from user
echo "💬 Enter commit message (or press Enter for default):"
read -r commit_message

# Use default message if none provided
if [ -z "$commit_message" ]; then
    commit_message="Update AI Web Scraper - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Add all changes
echo "📦 Adding all changes..."
git add .

# Commit changes
echo "💾 Committing changes with message: '$commit_message'"
git commit -m "$commit_message"

# Check if remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Error: No remote 'origin' found."
    echo "Please add your GitHub repository as origin:"
    echo "git remote add origin https://github.com/daitok6/AIWebscraper.git"
    exit 1
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
if git push origin main; then
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Your repository: https://github.com/daitok6/AIWebscraper"
else
    echo "❌ Error: Failed to push to GitHub."
    echo "Please check your internet connection and GitHub credentials."
    exit 1
fi

echo ""
echo "🎉 All done! Your changes are now live on GitHub." 