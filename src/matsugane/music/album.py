from typing import List, NewType

from attrs import define

from matsugane import utils
from matsugane.music.track import UniversalTrack

AlbumName = NewType("AlbumName", str)


@define(eq=False)
class Album:
    name: AlbumName
    tracks: List[UniversalTrack] = []

    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.name)

    @property
    def total_tracks(self) -> int:
        return len(self.tracks)

    @property
    def total_plays(self) -> int:
        return sum(track.plays for track in self.tracks)
