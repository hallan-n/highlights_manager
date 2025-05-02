
from model import Channel
from main import get_channel_info
import pytest

@pytest.mark.asyncio
async def test_get_channel_info_success_cached(mocker, channel):
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
    result = await get_channel_info('https://www.youtube.com/@canal_teste')
    assert isinstance(result, Channel)
    assert result.dict() == channel.dict()

@pytest.mark.asyncio
async def test_get_channel_info_success_no_cached(mocker, channel):
    mock_cache = mocker.patch('cache.get_value')
    mock_cache.return_value = None

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
    result = await get_channel_info('https://www.youtube.com/@canal_teste')
    assert isinstance(result, Channel)
    assert result.dict() == channel.dict()

    
@pytest.mark.asyncio
async def test_get_channel_info_no_items(mocker):
    mock_get = mocker.patch('httpx.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}
    resultado = await get_channel_info('https://www.youtube.com/@canal_teste')
    assert resultado == None

@pytest.mark.asyncio
async def test_get_channel_info_not_found(mocker):
    mock_get = mocker.patch('httpx.get')
    mock_get.return_value.status_code = 404 
    
    mock_get.return_value.json.return_value = {}
    resultado = await get_channel_info('https://www.youtube.com/@canal_inexistente')
    assert resultado is None

@pytest.mark.asyncio
async def test_get_channel_info_invalid_url_format():
    resultado = await get_channel_info('invalid_url')
    assert resultado == None
