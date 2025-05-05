from domain.model import Channel, Video
import json
from typing import Union, List

def parse_video(video: Union[list, str]) -> Union[List[Video], Video]:
    if isinstance(video, list):
        return [Video(**json.loads(v)) for v in video]
    elif isinstance(video, str):
        return Video(**json.loads(video))
    else:
        raise ValueError("Video no formato inválido.")
    
def parse_channel(channel: str) -> Channel:
    if isinstance(channel, str):
        return Channel(**json.loads(channel))
    else:
        raise ValueError("Canal no formato inválido.")
