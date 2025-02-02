from typing import List, NewType

import cutlet
from attrs import define

from matsugane import utils
from matsugane.music.album import Album

katsu = cutlet.Cutlet()

ArtistName = NewType("ArtistName", str)


@define(eq=False)
class Artist:
    name: ArtistName
    _albums: List[Album] = []

    @property
    def id(self) -> str:
        return utils.hash_string(f"artist-{self.sort_name}")

    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.name)

    @property
    def albums(self) -> List[Album]:
        return self._albums

    @property
    def total_albums(self) -> int:
        return len(self._albums)
