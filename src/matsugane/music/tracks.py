from typing import List

import attrs.validators
from attrs import define, field

from matsugane import utils
from matsugane.data.lastfm import LastfmFetcher, LastfmTrack
from matsugane.music.album import Album
from matsugane.music.artist import Artist
from matsugane.music.stats import Stats

fetcher = LastfmFetcher()


@define
class PlaysByHour:
    plays: int
    total: int
    hour: int = field(
        default=0,
        validator=attrs.validators.and_(
            attrs.validators.ge(0), attrs.validators.lt(24)
        ),
    )

    @property
    def hour_fmt(self) -> str:
        return f"{self.hour:02}:00"

    @property
    def plays_fmt(self) -> str:
        return f"{self.plays} play{'' if self.plays == 1 else 's'}"

    @property
    def percent(self) -> float:
        return self.plays / self.total

    @property
    def percent_fmt(self) -> str:
        return f"{(self.percent * 100):.7f}%"


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
        artists_dict = dict()
        for track in self.lastfm_tracks:
            artists_dict[track.artist_id] = track.artist

        artists = []
        for artist_id, artist_name in artists_dict.items():
            num_plays = self._plays_by_artist(artist_id)
            num_tracks = self._tracks_by_artist(artist_id)
            num_albums = self._albums_by_artist(artist_id)
            artist = Artist(artist_name, num_plays, num_tracks, num_albums)
            artists.append(artist)

        return sorted(artists, key=lambda a: a.sort_name)

    def _plays_by_artist(self, artist_id: str) -> int:
        return len(
            [track for track in self.lastfm_tracks if track.artist_id == artist_id]
        )

    def _tracks_by_artist(self, artist_id: str) -> int:
        seen = set()
        for track in self.lastfm_tracks:
            if track.artist_id == artist_id and track.unique_id not in seen:
                seen.add(track.unique_id)
        return len(seen)

    def _albums_by_artist(self, artist_id: str) -> int:
        seen = set()
        for track in self.lastfm_tracks:
            if track.artist_id == artist_id and track.album_id not in seen:
                seen.add(track.album_id)
        return len(seen)


    @property
    def albums(self) -> List[Album]:
        albums_dict = dict()
        for track in self.lastfm_tracks:
            albums_dict[track.album_id] = track.album

        albums = []
        for album_id,album_name in albums_dict.items():
            num_plays = self._plays_by_album(album_id)
            num_tracks = self._tracks_by_album(album_id)

            album = Album(album_name, num_plays, num_tracks)
            albums.append(album)

        return sorted(albums, key=lambda a: a.sort_name)

    def _plays_by_album(self, album_id: str) -> int:
        return len(
            [track for track in self.lastfm_tracks if track.album_id == album_id]
        )

    def _tracks_by_album(self, album_id: str) -> int:
        seen = set()
        for track in self.lastfm_tracks:
            if track.album_id == album_id and track.album_id not in seen:
                seen.add(track.album_id)
        return len(seen)


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

        seen = set()
        for track in self.lastfm_tracks:
            if track.id not in seen:
                seen.add(track.id)
        return len(seen)

    @property
    def total_plays(self) -> int:
        """
        Returns the sum of plays from all tracks.
        """
        if self.is_empty:
            return 0

        seen = set()
        for track in self.lastfm_tracks:
            if track.track_artist_id not in seen:
                seen.add(track.track_artist_id)
        return len(seen)

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

        seen = set()
        for track in self.lastfm_tracks:
            if track.artist_album_id not in seen:
                seen.add(track.artist_album_id)
        return len(seen)

    @property
    def plays_per_artist_stats(self) -> Stats:
        """
        Builds and returns a `Stats` objects for plays per artist.
        :return: A `Stats` object for plays per artist.
        """
        return Stats([artist.total_plays for artist in self.artists])

    @property
    def plays_per_album_stats(self) -> Stats:
        """
        Builds and returns a `Stats` object for plays per album.
        :return: A `Stats` object for plays per album.
        """
        plays = [album.total_plays for album in self.albums]
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
        )[:25]
        return top_artists

    @property
    def plays_by_hour(self) -> list[PlaysByHour]:
        hours: dict[int, int] = dict()
        for track in self.lastfm_tracks:
            hour = utils.convert_ts_to_dt(track.played_at).hour
            hours[hour] = hours.get(hour, 0) + 1

        plays_by_hour = [
            PlaysByHour(hour=k, plays=v, total=self.total_plays)
            for k, v in hours.items()
        ]
        plays_by_hour.sort(key=lambda x: (-x.percent, -x.plays, x.hour))
        return plays_by_hour
