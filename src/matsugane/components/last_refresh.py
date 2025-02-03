from textual.reactive import reactive
from textual.widgets import Label

from matsugane import utils


class LastRefresh(Label):
    is_refreshing: reactive[bool] = reactive(False)

    def watch_is_refreshing(self, refreshing: bool) -> None:
        if refreshing:
            self.update("Refreshing. Please wait...")
        else:
            self.update(utils.get_last_refresh())
