import os
from typing import Annotated, ClassVar

import pylast
from annotated_types import Gt
from dotenv import load_dotenv
from pydantic import BaseModel

from lastfm_stats import utils
from lastfm_stats.music.track import UniversalTrack

load_dotenv()


class LastfmFetcher(BaseModel):
    username: str = str(os.getenv("LASTFM_USER"))

    network: ClassVar[pylast.LastFMNetwork] = pylast.LastFMNetwork(
        api_key=str(os.getenv("LASTFM_KEY")),
        api_secret=str(os.getenv("LASTFM_SECRET")),
        username=username,
        password_hash=pylast.md5(str(os.getenv("LASTFM_PASSWORD"))),
    )

    def fetch_recent_tracks(self, limit: Annotated[int, Gt(0)] = 200) -> list[UniversalTrack]:
        user = self.network.get_user(self.username)
        raw_tracks = user.get_recent_tracks(
            cacheable=False,
            time_from=utils.get_today_at_midnight(),
            limit=limit
        )
        return [UniversalTrack.from_lastfm_track(track) for track in raw_tracks]
