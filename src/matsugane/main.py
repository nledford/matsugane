from datetime import datetime

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label

from matsugane.components.stats_header import StatsHeader
from matsugane.music.tracks import UniversalTracks


def current_time() -> str:
    """Returns the current 24-hour time as a string."""
    return datetime.now().strftime("%H:%M:%S")


class MatsuganeApp(App):
    """A Textual app to display stats from Lastfm."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [("r", "refresh_data", "Refresh Last.fm Data")]

    tracks: reactive[UniversalTracks] = reactive(UniversalTracks())
    last_refresh: reactive[str] = reactive(current_time())

    def __init__(self) -> None:
        super().__init__()
        self.set_reactive(MatsuganeApp.last_refresh, current_time())

    def update_last_refresh(self):
        self.last_refresh = f"Last Refresh: {current_time()}"

    def watch_last_refresh(self, text: str) -> None:
        self.query_one("#lastRefresh", Label).update(text)

    async def on_load(self) -> None:
        self.tracks.fetch_tracks()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        yield Label(f"Last Refresh: {current_time()}", id="lastRefresh")
        yield StatsHeader().data_bind(MatsuganeApp.tracks)

        yield Footer()

    async def action_refresh_data(self) -> None:
        """An action to fetch new data from Last.fm"""
        self.tracks.fetch_tracks()
        self.update_last_refresh()


if __name__ == "__main__":
    app = MatsuganeApp()
    app.run()
