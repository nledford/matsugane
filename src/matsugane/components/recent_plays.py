from textual import events
from textual.reactive import reactive
from textual.widgets import DataTable

from matsugane import utils
from matsugane.music.tracks import UniversalTracks


class RecentPlays(DataTable):
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
        self.add_columns("title", "artist", "album", "played at")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.build_table(self.ut)

    def build_table(self, ut: UniversalTracks) -> None:
        self.clear()

        if ut.is_empty and self.row_count == 0:
            self.add_row("No tracks", "", "", "", key="NO DATA")
        else:
            for track in ut.tracks:
                self.add_row(
                    track.title,
                    track.artist.name,
                    track.album.name,
                    utils.convert_ts_to_local_dt(track.played_at),
                    key=track.unique_id,
                )
