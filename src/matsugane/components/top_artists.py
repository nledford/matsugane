from textual.reactive import reactive
from textual.widgets import DataTable

from matsugane import utils
from matsugane.data.lastfm import LastfmTracks


class TopArtists(DataTable):
    ut: reactive[LastfmTracks] = reactive(LastfmTracks(), recompose=True)

    def watch_ut(self, tracks: LastfmTracks) -> None:
        self.ut = tracks
        self.build_table(tracks)

    def on_mount(self) -> None:
        self.add_columns("Artist", "Plays", "Tracks", "Albums", "Plays %")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.border_title = "Top Artists By Plays"
        self.build_table(self.ut)
        self.classes = "table"
        self.refresh()

    def build_table(self, ut: LastfmTracks) -> None:
        self.clear()

        def percentage(artist_plays: int = 0) -> str:
            if artist_plays == 0:
                result = 0
            else:
                result = (float(artist_plays) / float(self.ut.total_plays)) * 100

            return f"{result:.7f}%"

        if ut.is_empty and self.row_count == 0:
            self.add_row("No Tracks", "", "", "", key="NO DATA TOP ARTISTS")
        else:
            for top_artist in ut.top_artists:
                self.add_row(
                    utils.truncate(top_artist.name, 35),
                    top_artist.total_plays,
                    top_artist.total_tracks,
                    top_artist.total_albums,
                    percentage(top_artist.total_plays),
                )
