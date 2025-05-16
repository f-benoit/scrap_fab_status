import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Navigating to Microsoft Fabric Support page...")
        await page.goto("https://support.fabric.microsoft.com/en-gb/support/", timeout=60000)

        # Wait 5 seconds to ensure all dynamic content loads
        await page.wait_for_timeout(5000)

        os.makedirs("fabric_status", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"fabric_status/fabric_status_{timestamp}.png"
        await page.screenshot(path=filename, full_page=True)
        print(f"Screenshot saved: {filename}")

        await browser.close()

asyncio.run(run())
