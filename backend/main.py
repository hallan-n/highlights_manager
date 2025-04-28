# Retorna uma lista de vídeos que correspondem aos parâmetros de solicitação da API.
# GET https://www.googleapis.com/youtube/v3/videos


import requests


content = requests.get('https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=MBLiveTV&key=AIzaSyCPt5Z_ieIz3Lxy55UTyKE6ygRcqoHZWVQ', verify=False)

print(content)


import requests

url = "https://www.googleapis.com/youtube/v3/search"
params = {
    "part": "snippet",
    "q": "MBLiveTV",
    "type": "channel",
    "key": "YOUR_API_KEY"
}

response = requests.get(url, params=params, verify=False)

if response.status_code == 403:
    print("Erro 403: Acesso proibido. Verifique sua chave de API e permissões.")
else:
    print(response.json())
