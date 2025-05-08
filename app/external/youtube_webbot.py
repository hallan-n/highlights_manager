
from datetime import datetime, timedelta
from playwright.async_api import async_playwright, Page
from domain.model import Login
from infra.logger import logger
from consts import YOUTUBE_LOGIN, YOUTUBE_PASSWORD, YOUTUBE_EXPIRE_SESSION
import json

async def get_login_session() -> Login | None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto("https://www.youtube.com/signin")
            await page.wait_for_selector('input[type="email"]')
            await page.fill('input[type="email"]', YOUTUBE_LOGIN)
            await page.click('button:has-text("Next")')
            await page.wait_for_selector('input[type="password"]', timeout=15000)
            await page.fill('input[type="password"]', YOUTUBE_PASSWORD)
            await page.click('button:has-text("Next")')
            await page.wait_for_url("https://www.youtube.com/*", timeout=20000)
        except Exception as e:
            await browser.close()
            return None

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

async def get_session_page(login: Login) -> Page:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=login.state)

        page = await context.new_page()
        await page.goto("https://www.youtube.com/")

        try:
            await page.add_init_script(
                f"""() => {{
                    const data = {json.dumps(login.local_storage)};
                    for (const [key, value] of Object.entries(data)) {{
                        localStorage.setItem(key, value);
                    }}
                }}"""
            )

            await page.add_init_script(
                f"""() => {{
                    const data = {json.dumps(login.session_storage)};
                    for (const [key, value] of Object.entries(data)) {{
                        sessionStorage.setItem(key, value);
                    }}
                }}"""
            )
        except Exception as e:
            await browser.close()
            return None

        await page.reload()
        return page
