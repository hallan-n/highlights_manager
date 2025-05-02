import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from main import get_channel_info

def test_get_channel_info_success(mocker):
    mock_get = mocker.patch('httpx.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'items': ['teste']}
    resultado = get_channel_info('https://www.youtube.com/@canal_teste')
    assert resultado == "teste"
    
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
