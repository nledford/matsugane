from textual import events
from textual.reactive import reactive
from textual.widgets import DataTable

from matsugane import utils
from matsugane.music.tracks import UniversalTracks


class RecentPlays(DataTable):
    tracks: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)

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

    def watch_tracks(self, tracks: UniversalTracks) -> None:
        self.tracks = tracks
        self.build_table(clear_data=True)

    def on_mount(self) -> None:
        self.build_table()

    def build_table(self, clear_data: bool = False) -> None:
        if clear_data:
            self.clear()

        if not clear_data:
            self.add_columns("title", "artist", "album", "played at")
            self.cursor_type = "row"
            self.zebra_stripes = True

        if self.tracks.is_empty and self.row_count == 0:
            self.add_row("No tracks", "", "", "", key="NO DATA")
        else:
            for track in self.tracks.tracks:
                self.add_row(
                    track.title,
                    track.artist.name,
                    track.album.name,
                    utils.convert_ts_to_local_dt(track.played_at),
                    key=track.unique_id,
                )
