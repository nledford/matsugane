from textual.app import App, ComposeResult
from textual.containers import VerticalGroup
from textual.reactive import reactive
from textual.widgets import Footer, Header

from matsugane.components.last_refresh import LastRefresh
from matsugane.components.recent_plays import RecentPlays
from matsugane.components.stats_header import StatsHeader
from matsugane.components.top_artists import TopArtists
from matsugane.components.top_plays_by_hour import TopPlaysByHour
from matsugane.data.lastfm import LastfmTracks


class MatsuganeApp(App):
    """A Textual app to display stats from Lastfm."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [("r", "refresh_data", "Refresh Last.fm Data")]

    ut: reactive[LastfmTracks] = reactive(LastfmTracks())
    is_refreshing: reactive[bool] = reactive(False)

    async def on_mount(self) -> None:
        await self.refresh_tracks()

    def update_is_refreshing(self, override: bool = False) -> None:
        if override:
            self.is_refreshing = True
        else:
            self.is_refreshing = not self.is_refreshing

    async def refresh_tracks(self) -> None:
        self.update_is_refreshing(True)
        self.ut = await LastfmTracks.build(True)
        self.update_is_refreshing()

    def compose(self) -> ComposeResult:
        yield Header()

        with VerticalGroup(id="appContainer"):
            yield LastRefresh(id="lastRefreshed").data_bind(MatsuganeApp.is_refreshing)
            yield StatsHeader().data_bind(MatsuganeApp.ut)
            yield RecentPlays(id="recentPlays").data_bind(MatsuganeApp.ut)
            yield TopArtists().data_bind(MatsuganeApp.ut)
            yield TopPlaysByHour().data_bind(MatsuganeApp.ut)

        yield Footer()

    async def action_refresh_data(self) -> None:
        await self.refresh_tracks()


if __name__ == "__main__":
    app = MatsuganeApp()
    app.run()
