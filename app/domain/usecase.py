from infra.logger import logger
import re
from domain.model import Channel, Video
from infra.cache import get_value, set_value, get_by_prefix
from infra.youtube_api import fetch_channel, fetch_video

async def get_channel_info(custom_url: str) -> Channel:
    if not re.match(r"https:\/\/www\.youtube\.com\/@\w+", custom_url):
        logger.error("URL no formato inválida.")
        raise ValueError("URL no formato inválida.")
    
    url_split = custom_url.split('@')[1]
    cached_channel = await get_value(url_split, 'channel')

    if cached_channel:
        return cached_channel

    data = await fetch_channel(url_split)
    if not data:
        logger.error("Canal não encontrado.")
        raise ValueError("Canal não encontrado.")

    if not 'items' in data and len(data['items']) <= 0:
        logger.error("Canal não encontrado.")
        raise ValueError("Canal não encontrado.")

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
    await set_value(url_split, channel.json(), 'channel')
    return channel

async def get_video_by_channel_id(channel_id, next_page_token=None, limit=5):
    data = await fetch_video(channel_id, next_page_token, limit)
    if not data:
        logger.error("Vídeos não encontrados.")
        raise ValueError("Vídeos não encontrados.")
    if not 'items' in data and len(data['items']) <= 0:
        logger.error("Vídeos não encontrados.")
        raise ValueError("Vídeos não encontrados.")
    data = data['items']

    videos_cached = await get_by_prefix(channel_id, 'video')

    if videos_cached:
        video_ids = {video.id for video in videos_cached}
        data = [item for item in data if item['id']['videoId'] not in video_ids]

    if not data:
        logger.info("Nenhum vídeo novo encontrado.")
        return []
    
    published_cached = await get_by_prefix(channel_id, 'published')

    if published_cached:
        published_ids = {video.id for video in published_cached}
        data = [item for item in data if item['id']['videoId'] not in published_ids]

    if not data:
        logger.info("Videos já publicados.")
        return []

    videos = []
    for item in data:
        video = Video(
            id=item['id']['videoId'],
            etag=item['etag'],
            url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            title=item['snippet']['title'],
            thumbnail=item['snippet']['thumbnails']['high']['url'],
            description=item['snippet']['description'],
            published_at=item['snippet']['publishedAt'],
            channel_id=channel_id,
            channel_title=item['snippet']['channelTitle']
            )
        videos.append(video)
        key = channel_id + video.id
        await set_value(key, video.json(), 'video')
    return videos
