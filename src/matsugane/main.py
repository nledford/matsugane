from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label

from matsugane import utils
from matsugane.components.stats_header import StatsHeader
from matsugane.music.tracks import UniversalTracks


class MatsuganeApp(App):
    """A Textual app to display stats from Lastfm."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [("r", "refresh_data", "Refresh Last.fm Data")]

    tracks: reactive[UniversalTracks] = reactive(UniversalTracks(), recompose=True)
    last_refresh: reactive[str] = reactive(utils.get_last_refresh())

    def __init__(self) -> None:
        super().__init__()
        self.set_reactive(MatsuganeApp.last_refresh, utils.get_last_refresh())

    def update_last_refresh(self, refreshing: bool = False):
        if refreshing:
            self.last_refresh = "Refreshing. Please wait..."
        else:
            self.last_refresh = utils.get_last_refresh()

    def watch_last_refresh(self, text: str) -> None:
        self.query_one("#lastRefresh", Label).update(text)

    async def on_load(self) -> None:
        await self.tracks.fetch_tracks()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        yield Label(utils.get_last_refresh(), id="lastRefresh")
        yield StatsHeader().data_bind(MatsuganeApp.tracks)

        yield Footer()

    async def action_refresh_data(self) -> None:
        """An action to fetch new data from Last.fm"""
        self.update_last_refresh(True)
        await self.tracks.fetch_tracks()
        self.update_last_refresh()


if __name__ == "__main__":
    app = MatsuganeApp()
    app.run()
