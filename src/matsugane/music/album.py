
from attrs import define

from matsugane import utils


@define(eq=False)
class Album:
    name: str
    total_plays: int
    total_tracks: int

    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.name)
