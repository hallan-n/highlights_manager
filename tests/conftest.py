import pytest
from model import Channel

@pytest.fixture
def channel():
    return Channel(
        id='id_mock',
        etag='tag_mock',
        name='name_mock',
        url='https://www.youtube.com/@canal_teste',
        custom_url='canal_teste',
        description='description_mock',
        country='country_mock',
        published_at='published_at_mock',
        thumbnail='url_mock'
    )