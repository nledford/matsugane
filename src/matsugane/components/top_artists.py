from textual.reactive import reactive
from textual.widgets import DataTable

# from matsugane.components.ui import StretchyDataTable
from matsugane.music.tracks import UniversalTracks


class TopArtists(DataTable):
    ut: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)

    def watch_ut(self, tracks: UniversalTracks) -> None:
        self.ut = tracks
        self.build_table(tracks)

    def on_mount(self) -> None:
        self.add_columns("Artist", "Plays", "Tracks", "Albums")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.border_title = "Top Artists By Plays"
        self.build_table(self.ut)
        self.refresh()

    def build_table(self, ut: UniversalTracks) -> None:
        self.clear()

        if ut.is_empty and self.row_count == 0:
            self.add_row("No Tracks", "", "", "", key="NO DATA TOP ARTISTS")
        else:
            for top_artist in ut.top_artists:
                self.add_row(
                    top_artist.name,
                    top_artist.total_plays,
                    top_artist.total_tracks,
                    top_artist.total_albums,
                )
