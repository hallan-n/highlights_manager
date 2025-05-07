from infra.logger import logger
import re
from domain.model import Channel, Video
from domain.parser import parse_channel, parse_video
from infra.cache import get_value, set_value, get_by_prefix
import json 
from infra.youtube_api import fetch_channel, fetch_video

async def get_channel_info(custom_url: str) -> Channel:
    if not re.match(r"https:\/\/www\.youtube\.com\/@\w+", custom_url):
        logger.error("URL no formato inválida.")
        raise ValueError("URL no formato inválida.")
    
    url_split = custom_url.split('@')[1]
    cached_channel = await get_value(url_split, 'channel')

    if cached_channel:
        return parse_channel(cached_channel)

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

    published_videos_raw = await get_by_prefix(channel_id, 'published')
    published_videos = parse_video(published_videos_raw)
    for video in published_videos:
        for item in data:
            if video.id == item['id']:
                data.remove(item)
                break

    """
        Verficiar se os vídeos retornado pela API
        já estão no cache, se sim, exluir da var data
        os que forem novos, faça append em data e
        retorne.
    """
    # for item in data:
    #     video = Video(
    #         id=item['id'],
    #         etag=item['etag'],
    #         url=f"https://www.youtube.com/watch?v={item['id']}",
    #         title=item['snippet']['title'],
    #         thumbnail=item['snippet']['thumbnails']['high']['url'],
    #         description=item['snippet']['description'],
    #         published_at=item['snippet']['publishedAt'],
    #         channel_id=channel_id,
    #         channel_title=item['snippet']['channelTitle']
    #     )
    #     videos.append(video)
    # return videos