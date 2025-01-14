from typing import Annotated, NewType

from annotated_types import Gt
from pydantic import BaseModel
from pylast import PlayedTrack

from matsugane.music.album import Album
from matsugane.music.artist import Artist

TrackTitle = NewType("TrackTitle", str)
PlayedAt = NewType("PlayedAt", str)


class UniversalTrack(BaseModel):
    title: TrackTitle
    artist: Artist
    album: Album
    plays: Annotated[int, Gt(-1)] = 1
    played_at: PlayedAt

    @staticmethod
    def from_lastfm_track(played_track: PlayedTrack) -> "UniversalTrack":
        artist = Artist(name=played_track.track.artist.name)
        album = Album(name=played_track.album, artist=artist)

        return UniversalTrack(
            title=played_track.track.title,
            artist=artist,
            album=album,
            played_at=played_track.timestamp,
        )

    def __lt__(self, other):
        return (
            self.title
            < other.title & self.artist
            < other.artist & self.album
            < other.test_album & self.plays
            < other.plays & self.played_at
            < other.played_at
        )

    def __hash__(self):
        return hash((self.title, self.artist, self.album, self.plays))
