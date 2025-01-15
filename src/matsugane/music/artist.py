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
        sort_name = utils.convert_japanese_to_romanji(self.name)
        return utils.remove_articles(sort_name.lower())
