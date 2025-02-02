from typing import List, NewType

from attrs import define

from matsugane import utils

TrackTitle = NewType("TrackTitle", str)
PlayedAt = NewType("PlayedAt", str)


@define(eq=False)
class UniversalTrack:
    title: TrackTitle
    plays: int = 1
    played_at: List[str] = []
    # played_at: PlayedAt

    # title: TrackTitle
    # artist: Artist
    # album: Album
    # played_at: PlayedAt
    # plays: int = field(default=1, validator=validators.gt(0))
    #
    # @property
    # def id(self) -> str:
    #     return utils.hash_string(f"track-{self.sort_name}")
    #
    # @property
    # def unique_id(self) -> str:
    #     return utils.hash_string(
    #         f"track-{self.sort_name}-{self.artist.id}-{self.album.id}-{self.played_at}"
    #     )
    #
    # @property
    # def complete_id(self) -> str:
    #     return utils.hash_string(
    #         f"track-{self.sort_name}-{self.artist.id}-{self.album.id}"
    #     )
    #
    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.title)

    #
    # @classmethod
    # def from_lastfm_api(
    #     cls, title: str, artist: str, album: str, played_at: str
    # ) -> "UniversalTrack":
    #     universal_artist = Artist(name=ArtistName(artist))
    #     universal_album = Album(name=AlbumName(album), artist_id=universal_artist.id)
    #
    #     return cls(
    #         title=TrackTitle(title),
    #         artist=universal_artist,
    #         album=universal_album,
    #         played_at=PlayedAt(played_at),
    #     )
