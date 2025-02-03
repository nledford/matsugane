from textual.reactive import reactive

from matsugane.components.ui import StretchyDataTable
from matsugane.music.tracks import UniversalTracks


class TopPlaysByHour(StretchyDataTable):
    ut: reactive[UniversalTracks] = reactive(UniversalTracks())

    def watch_ut(self, tracks: UniversalTracks) -> None:
        self.ut = tracks
        self.build_table(tracks)

    def on_mount(self) -> None:
        self.add_columns("Hour", "Plays")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.build_table(self.ut)
        self.border_title = "Top Plays by Hour"

    def build_table(self, ut: UniversalTracks) -> None:
        self.clear()

        if ut.is_empty and self.row_count == 0:
            self.add_row("No tracks", "", key="NO DATA TOP HOURS")
        else:
            for hour, plays in ut.plays_by_hour.items():
                if plays > 0:
                    self.add_row(f"{hour:02}:00", f"{plays} plays")
