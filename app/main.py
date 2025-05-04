import httpx
from consts import API_KEY, BASE_URL, YOUTUBE_VIDEO_BASE_URL
from app.infra.logger import logger
import re
from app.domain.model import Channel, Video
from app.infra.cache import get_value, set_value
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
            await set_value(data['id'], channel.json())
            return channel
        else:
            logger.error("Canal não encontrado.")
            return None
    else:
        logger.error(f"Erro ao buscar canal: {response.status_code}")
        return None


async def get_video_by_channel_id(channel_id, next_page_token=None, limit=5):
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
        
    response = httpx.get(f"{BASE_URL}/search", params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            video_list: list[Video] = []
            items = data['items']
            logger.info(f'{len(items)} Vídeos encontrados')

            for item in items:
                video = Video(
                    id=item['id']['videoId'],
                    etag=item['etag'],
                    url=YOUTUBE_VIDEO_BASE_URL + item['id']['videoId'],
                    title=item['snippet']['title'],
                    thumbnail=item['snippet']['thumbnails']['high']['url'],
                    description=item['snippet']['description'],
                    published_at=item['snippet']['publishedAt'],
                    channel_id=item['snippet']['channelId'],
                    channel_title=item['snippet']['channelTitle']
                )
                key = item['snippet']['channelId'] + item['id']['videoId']
                await set_value(key, video.json())
                video_list.append(video)
            
            return video_list

        else:
            logger.error("Canal não encontrado.")
            return None
    else:
        logger.error(f"Erro ao buscar vídeo: {response.status_code}")
        return None
