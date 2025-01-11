from typing import NewType
import cutlet
from pydantic import BaseModel

from lastfm_stats import utils

katsu = cutlet.Cutlet()

ArtistName = NewType("ArtistName", str)


class Artist(BaseModel):
    name: ArtistName

    @property
    def id(self) -> str:
        return utils.hash_string(f"artist-{self.sort_name}")

    @property
    def sort_name(self) -> str:
        sort_name = utils.convert_japanese_to_romanji(self.name)
        return utils.remove_articles(sort_name.lower())

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)
