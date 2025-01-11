from typing import NewType

from pydantic import BaseModel

from lastfm_stats import utils
from lastfm_stats.music.artist import Artist

AlbumName = NewType("AlbumName", str)


class Album(BaseModel):
    name: AlbumName
    artist: Artist

    @property
    def id(self) -> str:
        return utils.hash_string(f"album-{self.sort_name}-{self.artist.id}")

    @property
    def sort_name(self) -> str:
        sort_name = utils.convert_japanese_to_romanji(self.name)
        return utils.remove_articles(sort_name.lower())

    def __lt__(self, other):
        return self.name < other.name & self.artist.name < other.artist.name

    def __hash__(self):
        return hash((self.name, self.artist))
