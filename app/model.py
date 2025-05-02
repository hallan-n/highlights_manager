from dataclasses import dataclass, asdict
import json

@dataclass
class Channel:
    id: str
    etag: str
    name: str
    url: str
    custom_url: str
    description: str
    country: str
    published_at: str
    thumbnail: str

    def dict(self):
        return asdict(self)

    def json(self):
        return json.dumps(asdict(self))


@dataclass
class Video:
    id: str
    etag: str
    url: str
    title: str
    thumbnail: str
    description: str
    published_at: str
    channel_id: str
    channel_title: str

    def dict(self):
        return asdict(self)

    def json(self):
        return json.dumps(asdict(self))