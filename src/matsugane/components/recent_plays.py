from textual.reactive import reactive
from textual.widgets import DataTable

from matsugane import utils
from matsugane.data.lastfm import LastfmTracks


class RecentPlays(DataTable):
    ut: reactive[LastfmTracks] = reactive(LastfmTracks(), recompose=True)

    def watch_ut(self, tracks: LastfmTracks) -> None:
        self.ut = tracks
        self.build_table(tracks)

    def on_mount(self) -> None:
        self.add_columns("Title", "Artist", "Album", "Played at")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.border_title = "Recent Plays"
        self.classes = "table"
        self.build_table(self.ut)

    def build_table(self, ut: LastfmTracks) -> None:
        self.clear()

        if ut.is_empty and self.row_count == 0:
            self.add_row("No tracks", "", "", "", key="NO DATA RECENT PLAYS")
        else:
            for track in ut.tracks:
                self.add_row(
                    utils.truncate(track.title),
                    utils.truncate(track.artist),
                    utils.truncate(track.album),
                    utils.convert_ts_to_local_time(track.played_at),
                    key=track.unique_id,
                )
