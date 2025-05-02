import httpx
from consts import API_KEY, BASE_URL
from logger import logger
import re
from model import Channel
from cache import get_value, set_value
import json 

async def get_channel_info(custom_url: str) -> Channel:
    if not re.match(r"https:\/\/www\.youtube\.com\/@\w+", custom_url):
        logger.error("URL no formato inválida.")
        return None

    url_split = custom_url.split('@')[1]

    cached_channel = await get_value(url_split)
    if cached_channel:
        return Channel(**json.loads(cached_channel))

    params = {
        'part': 'snippet',
        'forHandle': url_split,
        'key': API_KEY
    }
    logger.info('Realizando requisição para a API do YouTube')
    response = httpx.get(f"{BASE_URL}/channels", params=params)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            logger.info('Canal encontrado')
            data = data['items'][0]
            channel = Channel(
                id=data['id'],
                etag=data['etag'],
                name=data['snippet']['title'],
                url=custom_url,
                custom_url=url_split,
                description=data['snippet']['description'],
                country=data['snippet']['country'],
                published_at=data['snippet']['publishedAt'],
                thumbnail=data['snippet']['thumbnails']['high']['url']
            )
            await set_value(url_split, channel.json())
            return channel
        else:
            logger.error("Canal não encontrado.")
            return None
    else:
        logger.error(f"Erro ao buscar canal: {response.status_code}")
        return None
