from dataclasses import dataclass, asdict

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
    thumbnails: str

    def dict(self):
        return asdict(self)
