from textual import events
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import DataTable, Label

from matsugane import utils
from matsugane.music.tracks import UniversalTracks


class RecentPlays(Widget):
    ut: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)

    def compose(self) -> ComposeResult:
        yield Label("Recent Plays")
        yield RecentPlaysTable().data_bind(RecentPlays.ut)


class RecentPlaysTable(DataTable):
    ut: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)

    def on_resize(self, event: events.Resize) -> None:
        """
        Automatically expands or shrinks table columns to fit available space
        SOURCE: https://github.com/Textualize/textual/issues/5455#issuecomment-2571464847
        """
        total_width = event.size.width
        total_padding = 2 * (self.cell_padding * len(self.columns))
        column_width = (total_width - total_padding) // len(self.columns)

        for column in self.columns.values():
            column.auto_width = False
            column.width = column_width
        self.refresh()

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
            self.add_row("No tracks", "", "", "", key="NO DATA")
        else:
            for track in ut.lastfm_tracks:
                self.add_row(
                    track.title,
                    track.artist,
                    track.album,
                    utils.convert_ts_to_local_dt(track.played_at),
                    key=track.id,
                )
