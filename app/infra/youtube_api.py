import httpx
from domain.model import Video, Login
from consts import API_KEY, BASE_URL, YOUTUBE_LOGIN, YOUTUBE_PASSWORD
from infra.logger import logger
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
import json

async def fetch_channel(custom_id: str) -> dict | None:
    async with httpx.AsyncClient() as client:
        params = {
            'part': 'snippet',
            'forHandle': custom_id,
            'key': API_KEY
        }
        response = await client.get(f"{BASE_URL}/channels", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

async def fetch_video(channel_id, next_page_token=None, limit=5) -> dict | None:        
    async with httpx.AsyncClient() as client:
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'key': API_KEY,
            'type': 'video',
            'order': 'date',
            'maxResults': limit
        }
        if next_page_token:
            params['pageToken'] = next_page_token
        
        response = await client.get(f"{BASE_URL}/search", params=params)
        if response.status_code == 200:
            logger.info('Vídeos encontrados')
            return response.json()
        else:
            logger.error(f"Erro ao buscar vídeos: {response.status_code}")
            return None

async def _get_login():
    """
    Verificar se o login já existe no redis
    """
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
        expire_at = datetime.now() + timedelta(days=2)

        login = Login(
            state=state,
            cookies=cookies,
            local_storage=json.loads(local_storage),
            session_storage=json.loads(session_storage),
            expire_at=expire_at.isoformat()
        )
        """
            Adicioonar ao redis
        """
        await browser.close()


