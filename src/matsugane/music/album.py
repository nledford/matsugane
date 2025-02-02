from typing import NewType

from attrs import define

from matsugane import utils
from matsugane.music.track import UniversalTrack

AlbumName = NewType("AlbumName", str)


@define(eq=False)
class Album:
    name: AlbumName
    _tracks: [UniversalTrack] = []

    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.name)
