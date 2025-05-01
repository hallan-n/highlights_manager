import os
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.environ.get("API_KEY", "chave-teste")
BASE_URL = os.environ.get("BASE_URL", "url-teste")
