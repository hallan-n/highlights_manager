from infra.logger import logger
import re
import os
from datetime import datetime
from domain.model import Channel, Video, Login
from infra.cache import get_value, set_value, get_by_prefix, delete_key
from external.youtube_api import fetch_channel, fetch_video
from external.youtube_webbot import get_login_session, upload_video
from external.youtube_downloader import donwload_video, download_thumbnail
from consts import DOWNLOAD_TEMP_DIR, VIDEO_EXTENSION, THUMB_EXTENSION


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

async def get_video_by_channel_id(channel_id, limit=5) -> list[Video]:
    data = await fetch_video(channel_id, limit)
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
            channel_title=item['snippet']['channelTitle'],
            thumb_path=None,
            video_path=None
        )
        videos.append(video)
        key = channel_id + video.id
        await set_value(key, video.json(), 'video')
    return videos

async def _get_login() -> Login:
    login_session_cached = await get_value('youtube', 'login')
    if login_session_cached:
        expire_at = datetime.fromisoformat(login_session_cached.expire_at)
        if expire_at > datetime.now():
            return login_session_cached
        else:
            logger.info("Login expirado, realizando novo login.")
            await delete_key('youtube', 'login')
    
    login_session = await get_login_session()
    if not login_session:
        logger.error("Erro ao realizar login.")
        raise ValueError("Erro ao realizar login.")
    
    await set_value('youtube', login_session.json(), 'login')
    return login_session

async def dl_video_and_thumb(video: Video) -> Video:
    os.makedirs(DOWNLOAD_TEMP_DIR, exist_ok=True)

    is_videodl = donwload_video(video.id, video.url)
    if not is_videodl:
        logger.error('Erro ao baixar video.')
        raise ValueError('Erro ao baixar vídeo')

    logger.info('Vídeo baixado com sucesso!')
    
    is_thumbdl = await download_thumbnail(video.id, video.thumbnail)
    if not is_thumbdl:
        logger.error('Erro ao baixar thumbnail')
        raise ValueError('Erro ao baixar thumbnail')
    video.thumb_path
    
    logger.info('Thumbnail baixada com sucesso!')
    video.thumb_path=f'{DOWNLOAD_TEMP_DIR}/{video.id}.{THUMB_EXTENSION}'
    video.video_path=f'{DOWNLOAD_TEMP_DIR}/{video.id}.{VIDEO_EXTENSION}'

    return video

async def publish_video(video: Video):
    login = await _get_login()
    await upload_video(login, None)
    if not video.thumb_path or video.video_path:
        logger.error('Os arquivos deThumbnail e Vídeo não foram encontrados.')
        raise ValueError('Os arquivos deThumbnail e Vídeo não foram encontrados.')

    if not any(os.scandir(DOWNLOAD_TEMP_DIR)):
        logger.error('Os arquivos deThumbnail e Vídeo não foram encontrados.')
        raise ValueError('Os arquivos deThumbnail e Vídeo não foram encontrados.')

    login = await _get_login()
    
    if not login:
        logger.error("Erro ao obter sessão de login.")
        raise ValueError("Erro ao obter sessão de login.")
    
    if not login.state:
        logger.error("Erro ao obter estado de armazenamento.")
        raise ValueError("Erro ao obter estado de armazenamento.")

    if not login.cookies:
        logger.error("Erro ao obter cookies.")
        raise ValueError("Erro ao obter cookies.")
    
    if not login.local_storage:
        logger.error("Erro ao obter armazenamento local.")
        raise ValueError("Erro ao obter armazenamento local.")
    
    if not login.session_storage:
        logger.error("Erro ao obter armazenamento de sessão.")
        raise ValueError("Erro ao obter armazenamento de sessão.")

    try:
        result = await upload_video(login, None)
    except Exception as e:
        logger.error(f"Erro ao fazer upload do vídeo: {e}")
        raise ValueError("Erro ao fazer upload do vídeo.")
    
