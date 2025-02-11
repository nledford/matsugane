import os
from typing import ClassVar, List

import arrow
import attrs
import httpx
from arrow import Arrow
from attrs import define, field
from dotenv import load_dotenv

from matsugane import utils
from matsugane.data.stats import Stats

load_dotenv()


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


@define(eq=False)
class LastfmItem:
    name: str
    total_plays: int
    total_tracks: int
    total_albums: int = 0

    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.name)


@define(eq=False)
class LastfmTrack:
    title: str
    track_url: str
    artist: str
    artist_url: str
    album: str
    played_at: str

    @property
    def track_id(self) -> str:
        return f"track={self.sort_title}-{self.artist_sort_name}-{self.album_sort_name}"

    @property
    def play_id(self) -> str:
        return f"track-{self.artist_sort_name}-{self.album_sort_name}-{self.sort_title}-{self.played_at}"

    @property
    def track_artist_id(self) -> str:
        return f"track-{self.sort_title}-{self.artist_sort_name}"

    @property
    def artist_album_id(self) -> str:
        return f"track-{self.artist_sort_name}-{self.album_sort_name}"

    @property
    def sort_title(self) -> str:
        return utils.build_sort_name(self.title)

    @property
    def artist_id(self) -> str:
        return f"artist-{self.artist_sort_name}"

    @property
    def artist_sort_name(self) -> str:
        return utils.build_sort_name(self.artist)

    @property
    def album_id(self) -> str:
        return f"album-{self.album_sort_name}-{self.album_sort_name}"

    @property
    def album_sort_name(self) -> str:
        return utils.build_sort_name(self.album)

    @property
    def played_at_ts(self) -> Arrow:
        return arrow.get(int(self.played_at))

    @property
    def played_at_fmt(self) -> str:
        return self.played_at_ts.strftime("%T")


@define
class LastfmTracks:
    tracks: List[LastfmTrack] = []

    @staticmethod
    async def build(fetch_tracks: bool = False) -> "LastfmTracks":
        """
        Builds a new `LastfmTracks` object.
        :param fetch_tracks: If true, fetches new batch of lastfm tracks
        :return: A new `LastfmTracks` object
        """

        tracks = LastfmTracks()
        if fetch_tracks:
            await tracks.fetch_tracks()
        return tracks

    async def fetch_tracks(self) -> None:
        """
        Fetches tracks from last.fm
        """
        fetcher = LastfmFetcher()
        self.tracks = await fetcher.fetch_recent_tracks(1000)

    @property
    def artists(self) -> List[LastfmItem]:
        artists_dict = dict()
        for track in self.tracks:
            artists_dict[track.artist_id] = track.artist

        artists = []
        for artist_id, artist_name in artists_dict.items():
            num_plays = self._plays_by_artist(artist_id)
            num_tracks = self._tracks_by_artist(artist_id)
            num_albums = self._albums_by_artist(artist_id)
            artist = LastfmItem(artist_name, num_plays, num_tracks, num_albums)
            artists.append(artist)

        return sorted(artists, key=lambda a: a.sort_name)

    def _plays_by_artist(self, artist_id: str) -> int:
        return len([track for track in self.tracks if track.artist_id == artist_id])

    def _tracks_by_artist(self, artist_id: str) -> int:
        seen = set()
        tracks = [track for track in self.tracks if track.artist_id == artist_id]
        for track in tracks:
            if track.track_id not in seen:
                seen.add(track.track_id)
        return len(seen)

    def _albums_by_artist(self, artist_id: str) -> int:
        seen = set()
        tracks = [track for track in self.tracks if track.artist_id == artist_id]
        for track in tracks:
            if track.album_id not in seen:
                seen.add(track.album_id)
        return len(seen)

    @property
    def albums(self) -> List[LastfmItem]:
        albums_dict = dict()
        for track in self.tracks:
            albums_dict[track.album_id] = track.album

        albums = []
        for album_id, album_name in albums_dict.items():
            num_plays = self._plays_by_album(album_id)
            num_tracks = self._tracks_by_album(album_id)

            album = LastfmItem(album_name, num_plays, num_tracks)
            albums.append(album)

        return sorted(albums, key=lambda a: a.sort_name)

    def _plays_by_album(self, album_id: str) -> int:
        return len([track for track in self.tracks if track.album_id == album_id])

    def _tracks_by_album(self, album_id: str) -> int:
        seen = set()
        tracks = [track for track in self.tracks if track.album_id == album_id]
        for track in tracks:
            if track.album_id not in seen:
                seen.add(track.album_id)
        return len(seen)

    @property
    def has_tracks(self) -> bool:
        return len(self.tracks) > 0

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
        for track in self.tracks:
            if track.track_id not in seen:
                seen.add(track.track_id)
        return len(seen)

    @property
    def total_plays(self) -> int:
        """
        Returns the sum of plays from all tracks.
        """
        if self.is_empty:
            return 0

        return len([track.play_id for track in self.tracks])

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
        for track in self.tracks:
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
    def top_artists(self) -> List[LastfmItem]:
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
        for track in self.tracks:
            hour = utils.convert_ts_to_dt(track.played_at).hour
            hours[hour] = hours.get(hour, 0) + 1

        plays_by_hour = [
            PlaysByHour(hour=k, plays=v, total=self.total_plays)
            for k, v in hours.items()
        ]
        plays_by_hour.sort(key=lambda x: (-x.percent, -x.plays, x.hour))
        return plays_by_hour


@define
class LastfmFetcher:
    api_key: ClassVar[str] = str(os.getenv("LASTFM_KEY"))
    api_secret: ClassVar[str] = str(os.getenv("LASTFM_SECRET"))
    username: ClassVar[str] = str(os.getenv("LASTFM_USER"))
    password: ClassVar[str] = str(os.getenv("LASTFM_PASSWORD"))

    @classmethod
    async def fetch_recent_tracks(cls, limit: int = 200) -> list[LastfmTrack]:
        params = {
            "method": "user.getrecenttracks",
            "user": cls.username,
            "extended": "1",
            "limit": str(limit),
            "api_key": cls.api_key,
            "from": str(utils.get_today_at_midnight()),
            "format": "json",
        }

        async with httpx.AsyncClient() as client:
            result = await client.get(
                "http://ws.audioscrobbler.com/2.0/", params=params
            )
            recent_tracks = result.json()["recenttracks"]["track"]

            return [
                LastfmTrack(
                    title=track["name"],
                    track_url=track["url"],
                    artist=track["artist"]["name"],
                    artist_url=track["artist"]["url"],
                    album=track["album"]["#text"],
                    played_at=track["date"]["uts"],
                )
                for track in recent_tracks
            ]
