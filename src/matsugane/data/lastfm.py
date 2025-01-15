import os
from typing import ClassVar

import pylast
from dotenv import load_dotenv
from attrs import define

from matsugane import utils
from matsugane.music.track import UniversalTrack

load_dotenv()


@define
class LastfmFetcher:
    username: str = str(os.getenv("LASTFM_USER"))

    network: ClassVar[pylast.LastFMNetwork] = pylast.LastFMNetwork(
        api_key=str(os.getenv("LASTFM_KEY")),
        api_secret=str(os.getenv("LASTFM_SECRET")),
        username=username,
        password_hash=pylast.md5(str(os.getenv("LASTFM_PASSWORD"))),
    )

    def fetch_recent_tracks(self, limit: int = 200) -> list[UniversalTrack]:
        user = self.network.get_user(self.username)
        raw_tracks = user.get_recent_tracks(
            cacheable=False, time_from=utils.get_today_at_midnight(), limit=limit
        )
        return [UniversalTrack.from_lastfm_track(track) for track in raw_tracks]
