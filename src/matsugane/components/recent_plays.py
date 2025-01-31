from textual.reactive import reactive
from textual.widgets import DataTable

from matsugane.music.tracks import UniversalTracks


class RecentPlays(DataTable):
    tracks: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)

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

        if self.tracks.is_empty:
            self.add_row("No tracks", "", "", "")
        else:
            for track in self.tracks.tracks:
                self.add_row(
                    track.title, track.artist.name, track.album.name, track.played_at
                )
