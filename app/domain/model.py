import json
from dataclasses import asdict, dataclass


@dataclass
class Base:
    def dict(self):
        return asdict(self)

    def json(self):
        return json.dumps(asdict(self))


@dataclass
class Channel(Base):
    id: str
    etag: str
    name: str
    url: str
    custom_url: str
    description: str
    country: str
    published_at: str
    thumbnail: str


@dataclass
class Video(Base):
    id: str
    etag: str
    url: str
    title: str
    thumbnail: str
    description: str
    published_at: str
    channel_id: str
    channel_title: str
    video_path: str
    thumb_path: str


@dataclass
class Login(Base):
    state: dict
    cookies: dict
    local_storage: dict
    session_storage: dict
    expire_at: str
