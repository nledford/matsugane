from typing import NewType

from attrs import define

from matsugane import utils
from matsugane.music.artist import Artist

AlbumName = NewType("AlbumName", str)


@define
class Album:
    name: AlbumName
    artist: Artist

    @property
    def id(self) -> str:
        return utils.hash_string(f"album-{self.sort_name}-{self.artist.id}")

    @property
    def sort_name(self) -> str:
        sort_name = utils.convert_japanese_to_romanji(self.name)
        return utils.remove_articles(sort_name.lower())
