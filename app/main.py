import httpx
from consts import API_KEY, BASE_URL
from logger import logger
import re

def get_channel_info(custom_url):
    if not re.match(r"https:\/\/www\.youtube\.com\/@\w+", custom_url):
        logger.error("URL no formato inválida.")
        return None

    url_split = custom_url.split('@')[1]
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
            return data['items'][0]
        else:
            logger.error("Canal não encontrado.")
            return None
    else:
        logger.error(f"Erro ao buscar canal: {response.status_code}")
        return None
