
import yt_dlp
from consts import DOWNLOAD_TEMP_DIR, VIDEO_EXTENSION, THUMB_EXTENSION
import httpx
from infra.logger import logger

def donwload_video(video_id: str, url: str) -> bool:
    output_path = f'{DOWNLOAD_TEMP_DIR}/{video_id}.%(ext)s'

    ydl_opts = {
        'format': 'bv*+ba/best',
        'merge_output_format': VIDEO_EXTENSION,
        'outtmpl': output_path
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logger.info('Vídeo baixado com sucesso!')
        return True
    except Exception as e:
        logger.error(f'Erro ao baixar thumbnail: {e}')
        return False


async def download_thumbnail(video_id: str, url: str) -> bool:
    file_name = f"{video_id}.{THUMB_EXTENSION}"
    full_path = f"{DOWNLOAD_TEMP_DIR}/{file_name}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            with open(full_path, 'wb') as f:
                f.write(response.content)

            logger.info('Thumbnail baixada com sucesso!')
            return True
        else:
            logger.error(f'Erro ao baixar thumbnail: {response.status_code}')
            return False
