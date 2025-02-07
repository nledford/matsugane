from typing import List

import attrs.validators
from attrs import define, field
from more_itertools import flatten

from matsugane import utils
from matsugane.data.lastfm import LastfmFetcher, LastfmTrack
from matsugane.music.album import Album, AlbumName
from matsugane.music.artist import Artist, ArtistName
from matsugane.music.stats import Stats
from matsugane.music.track import TrackTitle, UniversalTrack

fetcher = LastfmFetcher()


@define
class PlaysByHour:
    hour: int = field(
        default=0,
        validator=attrs.validators.and_(
            attrs.validators.ge(0), attrs.validators.lt(24)
        ),
    )
    plays: int = field(default=0)
    percent: float = field(default=0.0)

    @property
    def hour_fmt(self) -> str:
        return f"{self.hour:02}:00"

    @property
    def plays_fmt(self) -> str:
        return f"{self.plays} play{'' if self.plays == 1 else 's'}"

    @property
    def percent_fmt(self) -> str:
        return f"{self.percent * 100}%"


@define
class UniversalTracks:
    lastfm_tracks: List[LastfmTrack] = []
    """A list of `LastfmTrack`s"""

    last_updated: str = field(default=utils.get_last_refresh())
    _tracks: List[Artist] = []

    @staticmethod
    async def build(fetch_tracks: bool = False) -> "UniversalTracks":
        """
        Builds (or rebuilds) a `UniversalTracks` object.
        :param fetch_tracks: If true, fetches tracks from Lastfm
        :return: A new `UniversalTracks` object.
        """
        ut = UniversalTracks()
        if fetch_tracks:
            await ut.fetch_tracks()
        return ut

    async def fetch_tracks(self) -> None:
        """
        Fetches tracks from Lastfm.
        """
        self.lastfm_tracks = await fetcher.fetch_recent_tracks()
        self.last_updated = utils.get_last_refresh()

    @property
    def artists(self) -> List[Artist]:
        raw_artists = set([track.artist for track in self.lastfm_tracks])

        artists = []

        for raw_artist in raw_artists:
            artist = Artist(ArtistName(raw_artist))
            albums = self._albums_by_artist(artist)
            artist.albums = albums
            artists.append(artist)

        return sorted(artists, key=lambda a: a.sort_name)

    def _albums_by_artist(self, artist: Artist) -> List[Album]:
        raw_albums = set(
            [track.album for track in self.lastfm_tracks if track.artist == artist.name]
        )
        albums = []
        for raw_album in raw_albums:
            album = Album(AlbumName(raw_album))
            album.tracks = self._tracks_by_album(artist, album)
            albums.append(album)

        return sorted(albums, key=lambda a: a.sort_name)

    def _tracks_by_album(self, artist: Artist, album: Album) -> List[UniversalTrack]:
        raw_tracks = set(
            [
                track
                for track in self.lastfm_tracks
                if track.artist == artist.name and track.album == album.name
            ]
        )

        plays_dict: dict[str, int] = dict()
        played_at_dict: dict[str, List[str]] = dict()
        for raw_track in raw_tracks:
            plays_dict[raw_track.title] = plays_dict.get(raw_track.title, 0) + 1
            played_at_dict.setdefault(raw_track.title, [])
            played_at_dict[raw_track.title].append(raw_track.played_at)

        tracks = []
        for raw_track in raw_tracks:
            track = UniversalTrack(
                TrackTitle(raw_track.title),
                plays=plays_dict[raw_track.title],
                played_at=played_at_dict[raw_track.title],
            )
            tracks.append(track)
        return sorted(tracks, key=lambda t: t.sort_name)

    @property
    def has_tracks(self) -> bool:
        return len(self.lastfm_tracks) > 0

    @property
    def is_empty(self) -> bool:
        return not self.has_tracks

    @property
    def total_tracks(self) -> int:
        """
        Returns the number of tracks from all artists and albums.
        """
        if self.is_empty:
            return 0

        return sum(artist.total_tracks for artist in self.artists)

    @property
    def total_plays(self) -> int:
        """
        Returns the sum of plays from all tracks.
        """
        if self.is_empty:
            return 0

        return sum(artist.total_plays for artist in self.artists)

    @property
    def total_artists(self) -> int:
        """
        Returns the total number of artists.
        """
        return len(self.artists)

    @property
    def total_albums(self) -> int:
        """
        Returns the total number of albums for all artists.
        """
        if self.is_empty:
            return 0

        return sum(artist.total_albums for artist in self.artists)

    @property
    def plays_per_artist_stats(self) -> Stats:
        """
        Builds and returns a `Stats` objects for plays per artist.
        :return: A `Stats` object for plays per artist.
        """
        return Stats([artist.total_tracks for artist in self.artists])

    @property
    def plays_per_album_stats(self) -> Stats:
        """
        Builds and returns a `Stats` object for plays per album.
        :return: A `Stats` object for plays per album.
        """
        albums = flatten([artist.albums for artist in self.artists])
        plays = [album.total_plays for album in albums]
        return Stats(plays)

    @property
    def top_artists(self) -> List[Artist]:
        top_artists = sorted(
            self.artists,
            key=lambda x: (
                -x.total_plays,
                -x.total_tracks,
                -x.total_albums,
                x.sort_name,
            ),
        )[:10]
        return top_artists

    @property
    def plays_by_hour(self) -> list[PlaysByHour]:
        hours = dict.fromkeys(range(0, 24), 0)

        for track in self.lastfm_tracks:
            played_at_hour = utils.convert_ts_to_dt(track.played_at).hour
            hours[played_at_hour] += 1

        plays_by_hour = [
            PlaysByHour(k, v, float(v) / self.total_tracks) for k, v in hours.items()
        ]
        plays_by_hour.sort(key=lambda x: (-x.percent, -x.plays, -x.hour))

        return plays_by_hour
