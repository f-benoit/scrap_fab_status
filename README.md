# Microsoft Fabric Status Scraper

This project scrapes the Microsoft Fabric product status page every 15 minutes using GitHub Actions and Playwright.

## Features

- Runs fully online, even when your computer is off
- Extracts dynamic product status table
- Saves a timestamped CSV on each run

## Setup

1. Create a new GitHub repository and push this folder.
2. GitHub Actions will automatically run every 15 minutes.
3. You can view results as CSV files in the repo history or artifacts.

## Local Run (Optional)

```bash
pip install -r requirements.txt
playwright install
python scrape_fabric_status.py
```
