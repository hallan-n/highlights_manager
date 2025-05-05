from domain.usecase import get_video_by_channel_id, get_channel_info
from infra.cache import get_redis, get_by_prefix
import asyncio

data = asyncio.run(get_by_prefix('UC1VZDEtGNxfQzh7', 'channel'))
print(data)