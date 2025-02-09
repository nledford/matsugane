import os
from typing import ClassVar

import arrow
import httpx
from arrow import Arrow
from attrs import define
from dotenv import load_dotenv

from matsugane import utils

load_dotenv()


@define(eq=False)
class LastfmTrack:
    title: str
    track_url: str
    artist: str
    artist_url: str
    album: str
    played_at: str

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
    def id(self) -> str:
        return f"track={self.sort_title}-{self.artist_sort_name}-{self.album_sort_name}"

    @property
    def unique_id(self) -> str:
        return f"track-{self.artist_sort_name}-{self.album_sort_name}-{self.sort_title}-{self.played_at}"

    @property
    def track_artist_id(self) -> str:
        return f"track-{self.sort_title}-{self.artist_sort_name}"

    @property
    def artist_album_id(self) -> str:
        return f"track-{self.artist_sort_name}-{self.album_sort_name}"

    @property
    def played_at_ts(self) -> Arrow:
        return arrow.get(int(self.played_at))


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
