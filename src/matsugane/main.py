from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label

from matsugane import utils
from matsugane.components.recent_plays import RecentPlays
from matsugane.components.stats_header import StatsHeader
from matsugane.music.tracks import UniversalTracks


class LastRefresh(Label):
    last_refresh: reactive[str] = reactive(utils.get_last_refresh())

    def watch_last_refresh(self, last_refresh: str) -> None:
        self.update(last_refresh)

# TODO set up loading indicators

class MatsuganeApp(App):
    """A Textual app to display stats from Lastfm."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [("r", "refresh_data", "Refresh Last.fm Data")]

    ut: reactive[UniversalTracks] = reactive(UniversalTracks())
    last_refresh: reactive[str] = reactive(utils.get_last_refresh())

    async def on_mount(self) -> None:
        await self.refresh_tracks()
        self.update_last_refresh()

    async def refresh_tracks(self) -> None:
        self.ut = await UniversalTracks.build(True)

    def update_last_refresh(self, is_refreshing: bool = False):
        if is_refreshing:
            self.last_refresh = "Refreshing. Please wait..."
        else:
            self.last_refresh = utils.get_last_refresh()

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="appContainer"):
            yield LastRefresh(id="lastRefreshed").data_bind(MatsuganeApp.last_refresh)
            yield StatsHeader().data_bind(MatsuganeApp.ut)
            yield RecentPlays(id="recentPlays").data_bind(MatsuganeApp.ut)

        yield Footer()

    async def action_refresh_data(self) -> None:
        self.update_last_refresh(True)
        await self.refresh_tracks()
        self.update_last_refresh()


if __name__ == "__main__":
    app = MatsuganeApp()
    app.run()
