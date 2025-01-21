from typing import NewType
import cutlet
from attrs import define

from matsugane import utils

katsu = cutlet.Cutlet()

ArtistName = NewType("ArtistName", str)


@define(eq=False)
class Artist:
    name: ArtistName

    @property
    def id(self) -> str:
        return utils.hash_string(f"artist-{self.sort_name}")

    @property
    def sort_name(self) -> str:
        if self.name.startswith("Noel Gallagher"):
            name = "Noel Gallagher's High Flying Birds"
        else:
            name = self.name

        return utils.build_sort_name(name)
