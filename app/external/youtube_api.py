import httpx
from consts import API_KEY, BASE_URL
from infra.logger import logger

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
