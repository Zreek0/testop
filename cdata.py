from typing import List
from dataclasses import dataclass
@dataclass
class MangaCard:
    client: "MangaClient"
    name: str
    url: str
    picture_url: str

    def get_url(self):
        return self.url

    def unique(self):
        return str(hash(self.url))
@dataclass
class MangaChapter:
    client: "MangaClient"
    name: str
    url: str
    manga: MangaCard
    pictures: List[str]

    def get_url(self):
        return self.url

    def unique(self):
        return str(hash(self.url))
