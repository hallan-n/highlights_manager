import os
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY=os.environ.get('API_KEY', 'chave-teste')
REDIS_HOST=os.environ.get('REDIS_HOST', '0.0.0.0')
REDIS_PORT=int(os.environ.get('REDIS_PORT', '6379'))
YOUTUBE_LOGIN=os.environ.get('YOUTUBE_LOGIN', 'login-teste')
YOUTUBE_PASSWORD=os.environ.get('YOUTUBE_PASSWORD', 'pwd-teste')
YOUTUBE_EXPIRE_SESSION = 7
REDIS_DB = {
    'channel': 0,
    'video': 1,
    'published': 2,
    'login': 3,
}
BASE_URL='https://www.googleapis.com/youtube/v3'
YOUTUBE_VIDEO_BASE_URL='https://www.youtube.com/watch?v='
DOWNLOAD_TEMP_DIR='app/infra/temp'
VIDEO_EXTENSION='mp4'
THUMB_EXTENSION='jpeg'