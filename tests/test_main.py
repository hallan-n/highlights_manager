
from model import Channel
from main import get_channel_info

def test_get_channel_info_success(mocker, channel):
    mock_get = mocker.patch('httpx.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'items': [
            {
                'etag': 'tag_mock',
                'id': 'id_mock',
                'snippet': {
                    'title': 'name_mock',
                    'description': 'description_mock',
                    'customUrl': 'custom_url_mock',
                    'publishedAt': 'published_at_mock',
                    'thumbnails': {
                        'high': {
                            'url': 'url_mock',
                        }
                    },
                    'country': 'country_mock'
                }
            }
        ]
    }
    result = get_channel_info('https://www.youtube.com/@canal_teste')
    assert isinstance(result, Channel)
    assert result.dict() == channel.dict()
    
def test_get_channel_info_no_items(mocker):
    mock_get = mocker.patch('httpx.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}
    resultado = get_channel_info('https://www.youtube.com/@canal_teste')
    assert resultado == None

def test_get_channel_info_api_error(mocker):
    mock_get = mocker.patch('httpx.get')
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {}
    resultado = get_channel_info('https://www.youtube.com/@canal_teste')
    assert resultado == None

def test_get_channel_info_invalid_url_format():
    resultado = get_channel_info('invalid_url')
    assert resultado == None
