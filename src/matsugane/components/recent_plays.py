from textual.reactive import reactive
from textual.widgets import DataTable

from matsugane import utils
from matsugane.music.tracks import UniversalTracks


class RecentPlays(DataTable):
    ut: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)

    def watch_ut(self, tracks: UniversalTracks) -> None:
        self.ut = tracks
        self.build_table(tracks)

    def on_mount(self) -> None:
        self.add_columns("Title", "Artist", "Album", "Played at")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.border_title = "Recent Plays"
        self.classes = "table"
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
                    utils.truncate(track.album),
                    utils.convert_ts_to_local_time(track.played_at),
                    key=track.id,
                )
