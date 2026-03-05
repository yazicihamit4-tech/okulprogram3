import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        filepath = os.path.abspath("kulup_paneli_yedekli_guncel (6).html")
        await page.goto(f"file://{filepath}")

        # 1. Login
        await page.fill('#loginUsername', 'zübeydehanım')
        await page.fill('#loginPassword', '715859')
        await page.click('button:has-text("Giriş Yap")')
        await page.wait_for_selector('#mainAppWrapper', state='visible')

        # 2. Click "Personel / Maaş Yönetimi" button to open the modal
        await page.click('#btnManageSalaries')
        await page.wait_for_selector('#salaryModalOverlay', state='visible')

        # Add personnel through the UI since state is scoped
        # wait for modal
        await page.wait_for_selector('#btnAddPersonnel')

        # Add Kadir Şişman
        await page.click('#btnAddPersonnel')
        await page.fill('#pName', 'Kadir Şişman')
        await page.select_option('#pRole', 'teacher_pool')
        await page.click('#btnSavePersonnel')

        # Add Ahmet Yılmaz
        await page.click('#btnAddPersonnel')
        await page.fill('#pName', 'Ahmet Yılmaz')
        await page.select_option('#pRole', 'teacher_pool')
        await page.click('#btnSavePersonnel')

        # 3. Ensure the salary table and tfoot loaded
        await page.wait_for_selector('#personnelTbody tr')
        await page.wait_for_selector('#personnelTfoot tr')

        await page.screenshot(path="salary_table_verified_full.png", full_page=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
