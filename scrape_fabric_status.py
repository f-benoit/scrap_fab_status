import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Navigating to Microsoft Fabric Support page...")
        await page.goto("https://support.fabric.microsoft.com/en-gb/support/", timeout=60000)

        # Wait for up to 30s for table to appear
        try:
            await page.wait_for_selector("table", timeout=30000)
            print("Table detected.")
        except:
            print("No table found. Taking screenshot for debug.")
            os.makedirs("debug", exist_ok=True)
            await page.screenshot(path="debug/page_debug.png", full_page=True)
            await browser.close()
            return

        rows = await page.query_selector_all("table tr")
        if not rows:
            print("No rows found in table. Taking screenshot.")
            os.makedirs("debug", exist_ok=True)
            await page.screenshot(path="debug/page_debug.png", full_page=True)
            await browser.close()
            return

        print(f"Extracting {len(rows)} rows...")
        data = []
        for i, row in enumerate(rows):
            cells = await row.query_selector_all("th" if i == 0 else "td")
            data.append([await cell.inner_text() for cell in cells])

        df = pd.DataFrame(data[1:], columns=data[0])
        os.makedirs("fabric_status", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filepath = f"fabric_status/fabric_status_{timestamp}.csv"
        df.to_csv(filepath, index=False)
        print(f"Saved: {filepath}")

        # Also save screenshot for visual inspection
        os.makedirs("debug", exist_ok=True)
        await page.screenshot(path=f"debug/page_debug_{timestamp}.png", full_page=True)

        await browser.close()

asyncio.run(run())
