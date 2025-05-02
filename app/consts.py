import os
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.environ.get("API_KEY", "chave-teste")
BASE_URL="https://www.googleapis.com/youtube/v3"
YOUTUBE_VIDEO_BASE_URL="https://www.youtube.com/watch?v="