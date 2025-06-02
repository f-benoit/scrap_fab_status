import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta
import os
import subprocess

def clean_old_files_and_git_commit(folder: str, days: int = 7):
    cutoff = datetime.now() - timedelta(days=days)
    deleted_files = []

    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime < cutoff:
                    os.remove(file_path)
                    print(f"Deleted old file: {file_path}")
                    deleted_files.append(file_path)

    # Git remove and commit
    if deleted_files:
        try:
            subprocess.run(["git", "rm"] + deleted_files, check=True)
            subprocess.run(["git", "commit", "-m", f"Remove screenshots older than {days} days"], check=True)
            subprocess.run(["git", "push"], check=True)
            print(f"Committed and pushed deletion of {len(deleted_files)} file(s).")
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {e}")

async def run():
    folder = "fabric_status"
    os.makedirs(folder, exist_ok=True)
    clean_old_files_and_git_commit(folder)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Navigating to Microsoft Fabric Support page...")
        await page.goto("https://support.fabric.microsoft.com/en-gb/support/", timeout=60000)
        await page.wait_for_timeout(5000)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{folder}/fabric_status_{timestamp}.png"
        await page.screenshot(path=filename, full_page=True)
        print(f"Screenshot saved: {filename}")

        await browser.close()

asyncio.run(run())
