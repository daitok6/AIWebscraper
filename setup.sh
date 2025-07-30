#!/bin/bash

# AI Web Scraper - Deployment Setup Script
echo "🚀 Setting up AI Web Scraper for deployment..."

# Install dependencies
pip install -r requirements.txt

# Make chromedriver executable
chmod +x chromedriver

echo "✅ Setup complete!" 