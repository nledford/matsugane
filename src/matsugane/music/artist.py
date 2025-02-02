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
    albums: List[Album] = []

    @property
    def id(self) -> str:
        return utils.hash_string(f"artist-{self.sort_name}")

    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.name)

    @property
    def total_albums(self) -> int:
        return len(self.albums)

    @property
    def total_tracks(self) -> int:
        tracks = 0
        for album in self.albums:
            tracks += len(album.tracks)
        return tracks

    @property
    def total_plays(self) -> int:
        plays = 0
        for album in self.albums:
            for track in album.tracks:
                plays += track.plays
        return plays
