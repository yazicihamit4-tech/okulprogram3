import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Load the local HTML file
        import os
        file_path = f"file://{os.path.abspath('kulup_paneli_yedekli_guncel (6).html')}"
        await page.goto(file_path)

        # 1. Take screenshot of login screen
        await page.screenshot(path="login_screen.png")

        # 2. Try wrong login
        await page.fill("#loginUsername", "wronguser")
        await page.fill("#loginPassword", "1234")
        await page.click("button:has-text('Giriş Yap')")
        await page.wait_for_timeout(500)
        await page.screenshot(path="login_error.png")

        # 3. Try correct login
        await page.fill("#loginUsername", "zübeydehanım")
        await page.fill("#loginPassword", "715859")
        await page.click("button:has-text('Giriş Yap')")
        await page.wait_for_timeout(500)
        await page.screenshot(path="main_app.png")

        await browser.close()

asyncio.run(main())
