from domain.usecase import publish_video
import asyncio

# data = asyncio.run(get_channel_info('https://www.youtube.com/@MBLiveTV'))
data = asyncio.run(publish_video())
print(data)