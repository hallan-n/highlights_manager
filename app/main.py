import httpx
from app.consts import API_KEY, BASE_URL


def get_channel_id(custom_url):
    url_split = custom_url.split('@')[1]
    params = {
        'part': 'snippet',
        'forHandle': url_split,
        'key': API_KEY
    }
    response = httpx.get(f"{BASE_URL}/channels", params=params)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['id']
        else:
            print("Canal não encontrado.")
            return None
    else:
        print(f"Erro ao buscar canal: {response.status_code}")
        print(response.text)
        return None

channel_info = get_channel_id("https://www.youtube.com/@milkz2")

print(channel_info)