from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Label

from matsugane.music.tracks import UniversalTracks


class Stats(HorizontalGroup):
    def __init__(self, header: str, data: str):
        super().__init__()
        self.header = header
        self.cell = data

    def compose(self) -> ComposeResult:
        yield Label(self.header, classes="stats-cell-header")
        yield Label(self.cell, classes="stats-cell")


class StatsHeader(HorizontalGroup):
    def __init__(self, ut: UniversalTracks):
        super().__init__()
        self.tracks: UniversalTracks = ut

    def compose(self) -> ComposeResult:
        # yield HorizontalGroup(
        #     Stats(header="Total Artists", data=str(self.tracks.total_artists)),
        #     Stats(header="Total Albums", data=str(self.tracks.total_albums)),
        #     Stats(header="Total Tracks", data=str(self.tracks.total_tracks)),
        #     Stats(header="Total Plays", data=str(self.tracks.total_plays)),
        #     id="StatsHeader",
        # )
        yield VerticalGroup(
            HorizontalGroup(
                Stats(header="Total Artists", data=str(self.tracks.total_artists)),
                Stats(header="Total Albums", data=str(self.tracks.total_albums)),
                Stats(header="Total Tracks", data=str(self.tracks.total_tracks)),
                Stats(header="Total Plays", data=str(self.tracks.total_plays)),
            ),
            HorizontalGroup(
                Stats(
                    header="Avg. Plays Per Artist",
                    data=str(self.tracks.average_plays_per_artist),
                ),
                Stats(
                    header="Avg. Plays Per Album",
                    data=str(self.tracks.average_plays_per_album),
                ),
            ),
        )
