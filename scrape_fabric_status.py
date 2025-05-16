import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://support.fabric.microsoft.com/en-gb/support/")
        await page.wait_for_selector("table", timeout=15000)

        rows = await page.query_selector_all("table tr")
        data = []
        for i, row in enumerate(rows):
            cells = await row.query_selector_all("th" if i == 0 else "td")
            data.append([await cell.inner_text() for cell in cells])

        await browser.close()

        df = pd.DataFrame(data[1:], columns=data[0])

        # Ensure the folder exists
        os.makedirs("fabric_status", exist_ok=True)

        # Save CSV in the folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filepath = f"fabric_status/fabric_status_{timestamp}.csv"
        df.to_csv(filepath, index=False)
        print(f"Saved: {filepath}")

asyncio.run(run())
