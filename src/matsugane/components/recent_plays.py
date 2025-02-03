from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from matsugane import utils
from matsugane.components.ui import StretchyDataTable
from matsugane.music.tracks import UniversalTracks


class RecentPlays(Widget):
    ut: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)

    def compose(self) -> ComposeResult:
        yield Label("Recent Plays")
        yield RecentPlaysTable().data_bind(RecentPlays.ut)


class RecentPlaysTable(StretchyDataTable):
    ut: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)

    def watch_ut(self, tracks: UniversalTracks) -> None:
        self.ut = tracks
        self.build_table(tracks)

    def on_mount(self) -> None:
        self.add_columns("Title", "Artist", "Album", "Played at")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.build_table(self.ut)

    def build_table(self, ut: UniversalTracks) -> None:
        self.clear()

        if ut.is_empty and self.row_count == 0:
            self.add_row("No tracks", "", "", "", key="NO DATA RECENT PLAYS")
        else:
            for track in ut.lastfm_tracks:
                self.add_row(
                    track.title,
                    track.artist,
                    track.album,
                    utils.convert_ts_to_local_time(track.played_at),
                    key=track.id,
                )
