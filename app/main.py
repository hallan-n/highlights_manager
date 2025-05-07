from domain.usecase import get_video_by_channel_id, get_channel_info
import asyncio

# data = asyncio.run(get_channel_info('https://www.youtube.com/@MBLiveTV'))
data = asyncio.run(get_video_by_channel_id('UCZYyHef3eBoBEztAOY'))
print(data)