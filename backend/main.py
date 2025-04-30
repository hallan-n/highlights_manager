import httpx
from .setup import API_KEY, BASE_URL_CHANNELS, BASE_URL_SEARCH

def get_channel_id(channel_name):
    params = {
        'part': 'snippet',
        'forUsername': channel_name,
        'key': API_KEY
    }
    response = httpx.get(BASE_URL_CHANNELS, params=params, verify=False)
    
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

def search_videos_by_channel(channel_id, max_results=5):
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'order': 'date',
        'type': 'video',
        'maxResults': max_results,
        'key': API_KEY
    }
    response = httpx.get(BASE_URL_SEARCH, params=params, verify=False)

    if response.status_code == 200:
        data = response.json()
        videos = []
        for item in data.get('items', []):
            video_info = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'videoId': item['id']['videoId'],
                'channelTitle': item['snippet']['channelTitle']
            }
            videos.append(video_info)
        return videos
    else:
        print(f"Erro ao buscar vídeos: {response.status_code}")
        print(response.text)
        return []



if __name__ == '__main__':
    channel_name = input("Digite o nome do canal para buscar os últimos vídeos: ")
    channel_id = get_channel_id(channel_name)

    if channel_id:
        results = search_videos_by_channel(channel_id)

        if results:
            print("Últimos vídeos encontrados:")
            for idx, video in enumerate(results, start=1):
                video_model = {
                    'index': idx,
                    'titulo': video['title'],
                    'canal': video['channelTitle'],
                    'link': f'https://www.youtube.com/watch?v={video['videoId']}',
                    'descricao': video['description']
                }
                print(video_model)
        else:
            print("Nenhum vídeo encontrado.")
    else:
        print("Não foi possível encontrar o canal.")