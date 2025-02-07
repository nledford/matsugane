from textual import events
from textual.widgets import DataTable


class StretchyDataTable(DataTable):
    """
    Automatically expands or shrinks table columns to fit available space
    SOURCE: https://github.com/Textualize/textual/issues/5455#issuecomment-2571464847
    """

    def on_resize(self, event: events.Resize) -> None:
        total_width = event.size.width - (len(self.columns) // 2)
        total_padding = 2 * (self.cell_padding * len(self.columns))
        column_width = (total_width - total_padding) // len(self.columns)

        for column in self.columns.values():
            column.auto_width = False
            column.width = column_width
        self.refresh()

    def on_mount(self) -> None:
        self.classes = "table"
