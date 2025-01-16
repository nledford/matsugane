from typing import NewType

from matsugane import utils
from pylast import PlayedTrack

from matsugane.music.album import Album
from matsugane.music.artist import Artist

from attrs import define, field, validators

TrackTitle = NewType("TrackTitle", str)
PlayedAt = NewType("PlayedAt", str)


@define(eq=False)
class UniversalTrack:
    title: TrackTitle
    artist: Artist
    album: Album
    played_at: PlayedAt
    plays: int = field(default=1, validator=validators.gt(0))

    @property
    def id(self) -> str:
        return utils.hash_string(f"track-{self.title}-{self.artist.id}")

    @property
    def unique_id(self) -> str:
        return utils.hash_string(
            f"track-{self.title}-{self.artist.id}-{self.album.id}-{self.played_at}"
        )

    @property
    def complete_id(self) -> str:
        return utils.hash_string(f"track-{self.title}-{self.artist.id}-{self.album.id}")

    @classmethod
    def from_lastfm_track(cls, played_track: PlayedTrack) -> "UniversalTrack":
        artist = Artist(name=played_track.track.artist.name)
        album = Album(name=played_track.album, artist=artist)

        return cls(
            title=played_track.track.title,
            artist=artist,
            album=album,
            played_at=played_track.timestamp,
        )
