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
        seen = set()
        albums = []
        for album in self._albums:
            if album.name not in seen:
                seen.add(album.name)
                albums.append(album)
        return albums

    @albums.setter
    def albums(self, albums: List[Album]) -> None:
        self._albums = albums

    @property
    def total_albums(self) -> int:
        """
        Returns the total number of albums in associated with this artist.
        """
        return len(self.albums)

    @property
    def total_tracks(self) -> int:
        """
        Returns total number of tracks from all albums.
        """
        return sum(album.total_tracks for album in self.albums)

    @property
    def total_plays(self) -> int:
        """
        Returns the sum of all plays from all albums.
        """
        return sum(album.total_plays for album in self.albums)
