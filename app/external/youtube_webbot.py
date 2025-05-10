
from datetime import datetime, timedelta
from playwright.async_api import async_playwright, Page
from domain.model import Login, Video
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

async def _inject_session(page: Page, login: Login):
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
    
async def upload_video(login: Login, video: Video) -> bool:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=login.state)

        page = await context.new_page()
        await page.goto("https://www.youtube.com/")

        try:
            await _inject_session(page, login)
            logger.info("Sessão injetada com sucesso.")
        except:
            logger.error(f"Erro ao injetar sessão")
            await browser.close()
            return None

        await page.goto('https://studio.youtube.com')

        await page.click('[test-id="upload-icon-url"]')

        try:

            input_video = await page.evaluate_handle("""
            () => {
                const input = document.querySelector('input[type="file"]');
                if (input) {
                    input.style.display = 'block';
                    input.removeAttribute('aria-hidden');
                    input.removeAttribute('tabindex');
                }
                return input;
            }
            """)
            await input_video.as_element().set_input_files(video.video_path)
            logger.info('Iniciando Upload do Video.')
            
            await page.wait_for_timeout(3000)

            input_thumb = await page.evaluate_handle("""
            () => {
                const input = document.querySelector('input[type="file"]');
                if (input){
                    input.style.display = 'block';
                    input.removeAttribute('aria-hidden');
                    input.removeAttribute('tabindex');
                }
                return input;
            }
            """)
            await input_thumb.as_element().set_input_files(video.thumb_path)
            logger.info('Iniciando Upload da Thumb.')

            await page.wait_for_timeout(3000)

            title = await page.query_selector('[aria-label^="Adicione um título"]')
            description = await page.query_selector('[aria-label^="Fale sobre"]')

            await title.fill(video.title)
            await description.fill(video.description)

            await page.click('[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')

            await page.click('button[aria-label="Próximo"]')
            await page.click('button[aria-label="Próximo"]')
            await page.click('button[aria-label="Próximo"]')

            await page.click('[name="PUBLIC"]')
            await page.click('button[aria-label="Publicar"]')

            logger.info('Video enviado, aguardando processamento da publicação')
            return True
        except:
            logger.error("Erro enviar o video")
            await browser.close()
            return None
        breakpoint()


        