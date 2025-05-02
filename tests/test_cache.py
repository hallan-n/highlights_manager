
import pytest
from cache import set_value, get_value, delete_key

@pytest.mark.asyncio
async def test_set_value_success(monkeypatch):
    async def mock_set(key, value, ex=None):
        return True

    monkeypatch.setattr('cache.r.set', mock_set)
    result = await set_value('test_key', 'test_value')
    assert result is True


@pytest.mark.asyncio
async def test_set_value_fail(mocker):
    mock_redis_set = mocker.AsyncMock(side_effect=Exception("Erro simulado no Redis"))
    mocker.patch('cache.r.set', mock_redis_set)
    result = await set_value('test_key', 'test_value', expiration=60)
    mock_redis_set.assert_awaited_once_with('test_key', 'test_value', ex=60)
    assert result is False

@pytest.mark.asyncio
async def test_get_value_success(monkeypatch):
    async def mock_get(key):
        return True

    monkeypatch.setattr('cache.r.get', mock_get)
    result = await get_value('test_key')
    assert result is True

@pytest.mark.asyncio
async def test_get_value_is_none(monkeypatch):
    async def mock_get(key):
        return None

    monkeypatch.setattr('cache.r.get', mock_get)
    result = await get_value('test_key')
    assert result is None



@pytest.mark.asyncio
async def test_get_value_fail(mocker):
    mock_redis_get = mocker.AsyncMock(side_effect=Exception("Erro simulado no Redis"))
    mocker.patch('cache.r.get', mock_redis_get)
    result = await get_value('test_key')
    assert result is None


@pytest.mark.asyncio
async def test_delete_success(monkeypatch):
    async def mock_delete(key):
        return True

    monkeypatch.setattr('cache.r.delete', mock_delete)
    result = await delete_key('test_key')
    assert result is True

@pytest.mark.asyncio
async def test_delete_fail(mocker):
    mock_redis_delete = mocker.AsyncMock(side_effect=Exception("Erro simulado no Redis"))
    mocker.patch('cache.r.delete', mock_redis_delete)
    result = await delete_key('test_key')
    assert result is False
