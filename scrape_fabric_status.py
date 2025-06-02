import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta
import os

# Delete screenshots older than 21 days
def clean_old_files(folder: str, days: int = 21):
    cutoff = datetime.now() - timedelta(days=days)
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime < cutoff:
                    os.remove(file_path)
                    print(f"Deleted old file: {file_path}")

async def run():
    folder = "fabric_status"
    os.makedirs(folder, exist_ok=True)
    clean_old_files(folder)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Navigating to Microsoft Fabric Support page...")
        await page.goto("https://support.fabric.microsoft.com/en-gb/support/", timeout=60000)

        # Wait 5 seconds to ensure all dynamic content loads
        await page.wait_for_timeout(5000)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{folder}/fabric_status_{timestamp}.png"
        await page.screenshot(path=filename, full_page=True)
        print(f"Screenshot saved: {filename}")

        await browser.close()

asyncio.run(run())
