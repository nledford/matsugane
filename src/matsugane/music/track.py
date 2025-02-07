from typing import List, NewType

from attrs import define

from matsugane import utils

TrackTitle = NewType("TrackTitle", str)
PlayedAt = NewType("PlayedAt", str)


@define(eq=False)
class UniversalTrack:
    title: TrackTitle
    plays: int = 1
    played_at: List[str] = []

    @property
    def sort_name(self) -> str:
        return utils.build_sort_name(self.title)
