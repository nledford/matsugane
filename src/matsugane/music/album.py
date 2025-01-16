from typing import NewType

from attrs import define

from matsugane import utils
from matsugane.music.artist import Artist

AlbumName = NewType("AlbumName", str)


@define(eq=False)
class Album:
    name: AlbumName
    artist: Artist

    @property
    def id(self) -> str:
        return utils.hash_string(f"album-{self.sort_name}-{self.artist.sort_name}")

    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.name)
