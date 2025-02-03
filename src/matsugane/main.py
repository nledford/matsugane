from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header

from matsugane.components.last_refresh import LastRefresh
from matsugane.components.recent_plays import RecentPlays
from matsugane.components.stats_header import StatsHeader
from matsugane.components.ui import StretchyDataTable
from matsugane.music.tracks import UniversalTracks


class TopArtists(StretchyDataTable):
    ut: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)

    def watch_ut(self, tracks: UniversalTracks) -> None:
        self.ut = tracks
        self.build_table(tracks)

    def on_mount(self) -> None:
        self.add_columns("Artist", "Albums", "Plays")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.build_table(self.ut)

    def build_table(self, ut: UniversalTracks) -> None:
        self.clear()

        if ut.is_empty and self.row_count == 0:
            self.add_row("No Tracks", "", "", key="NO DATA TOP ARTISTS")
        else:
            for top_artist in ut.top_artists:
                self.add_row(
                    top_artist.name, top_artist.total_albums, top_artist.total_plays
                )


class MatsuganeApp(App):
    """A Textual app to display stats from Lastfm."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [("r", "refresh_data", "Refresh Last.fm Data")]

    ut: reactive[UniversalTracks] = reactive(UniversalTracks())
    is_refreshing: reactive[bool] = reactive(False)

    async def on_mount(self) -> None:
        await self.refresh_tracks()

    def update_is_refreshing(self, override: bool = False) -> None:
        if override:
            self.is_refreshing = True
        else:
            self.is_refreshing = not self.is_refreshing

        self.query_one(StatsHeader).loading = self.is_refreshing
        self.query_one(RecentPlays).loading = self.is_refreshing

    async def refresh_tracks(self) -> None:
        self.update_is_refreshing(True)
        self.ut = await UniversalTracks.build(True)
        self.update_is_refreshing()

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="appContainer"):
            yield LastRefresh(id="lastRefreshed").data_bind(MatsuganeApp.is_refreshing)
            yield StatsHeader().data_bind(MatsuganeApp.ut)
            yield RecentPlays(id="recentPlays").data_bind(MatsuganeApp.ut)

            # yield TopArtists().data_bind(MatsuganeApp.ut)

        yield Footer()

    async def action_refresh_data(self) -> None:
        await self.refresh_tracks()


if __name__ == "__main__":
    app = MatsuganeApp()
    app.run()
