
import cutlet
from attrs import define

from matsugane import utils

katsu = cutlet.Cutlet()


@define(eq=False)
class Artist:
    name: str
    total_plays: int
    total_tracks: int
    total_albums: int

    @property
    def id(self) -> str:
        return utils.hash_string(f"artist-{self.sort_name}")

    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.name)
