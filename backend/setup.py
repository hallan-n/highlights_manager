import os
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.environ.get("API_KEY", "chave-teste")
BASE_URL_SEARCH = os.environ.get("BASE_URL_SEARCH", "url-teste")
BASE_URL_CHANNELS = os.environ.get("BASE_URL_CHANNELS", "url-teste")
