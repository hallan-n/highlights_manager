
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from domain.model import Login
from consts import YOUTUBE_LOGIN, YOUTUBE_PASSWORD, YOUTUBE_EXPIRE_SESSION
import json

async def get_login_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.youtube.com/signin")
        await page.wait_for_selector('input[type="email"]')
        await page.fill('input[type="email"]', YOUTUBE_LOGIN)
        await page.click('button:has-text("Next")')
        await page.wait_for_selector('input[type="password"]', timeout=15000)
        await page.fill('input[type="password"]', YOUTUBE_PASSWORD)
        await page.click('button:has-text("Next")')
        await page.wait_for_url("https://www.youtube.com/*", timeout=20000)

        state = await context.storage_state()
        cookies = await context.cookies()
        local_storage = await page.evaluate("() => JSON.stringify(window.localStorage)")
        session_storage = await page.evaluate("() => JSON.stringify(window.sessionStorage)")
        expire_at = datetime.now() + timedelta(days=YOUTUBE_EXPIRE_SESSION)

        login = Login(
            state=state,
            cookies=cookies,
            local_storage=json.loads(local_storage),
            session_storage=json.loads(session_storage),
            expire_at=expire_at.isoformat()
        )
        await browser.close()
        return login
