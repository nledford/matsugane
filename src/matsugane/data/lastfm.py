import os
from typing import ClassVar

import httpx
from attrs import define
from dotenv import load_dotenv

from matsugane import utils
from matsugane.music.track import UniversalTrack

load_dotenv()


@define
class LastfmFetcher:
    api_key: ClassVar[str] = str(os.getenv("LASTFM_KEY"))
    api_secret: ClassVar[str] = str(os.getenv("LASTFM_SECRET"))
    username: ClassVar[str] = str(os.getenv("LASTFM_USER"))
    password: ClassVar[str] = str(os.getenv("LASTFM_PASSWORD"))

    @classmethod
    async def fetch_recent_tracks(cls, limit: int = 200) -> list[UniversalTrack]:
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

            universal_tracks: list[UniversalTrack] = []
            for track in recent_tracks:
                title = track["name"]
                artist = track["artist"]["name"]
                # artist_url = track['artist']['url']
                album = track["album"]["#text"]
                played_at = track["date"]["uts"]
                # track_url = track['url']

                universal_track = UniversalTrack.from_lastfm_api(
                    title=title, artist=artist, album=album, played_at=played_at
                )
                universal_tracks.append(universal_track)
            return universal_tracks
