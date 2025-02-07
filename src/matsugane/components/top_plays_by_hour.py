from textual.reactive import reactive
from textual.widgets import DataTable

from matsugane.music.tracks import UniversalTracks


class TopPlaysByHour(DataTable):
    ut: reactive[UniversalTracks] = reactive(UniversalTracks())

    def watch_ut(self, tracks: UniversalTracks) -> None:
        self.ut = tracks
        self.build_table(tracks)

    def on_mount(self) -> None:
        self.add_columns("Hour", "Plays", "%")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.build_table(self.ut)
        self.border_title = "Top Plays by Hour"
        self.classes = "table"

    def build_table(self, ut: UniversalTracks) -> None:
        self.clear()

        if ut.is_empty and self.row_count == 0:
            self.add_row("No tracks", "", "", key="NO DATA TOP HOURS")
        else:
            for item in ut.plays_by_hour:
                if item.plays > 0:
                    self.add_row(item.hour_fmt, item.plays_fmt, item.percent_fmt)
