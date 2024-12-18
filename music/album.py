from pydantic import BaseModel

import utils
from music.artist import Artist


class Album(BaseModel):
    name: str
    artist: Artist

    @property
    def id(self) -> str:
        return utils.hash_string(f"album-{self.name.lower()}-{self.artist.id}")

    @property
    def sort_name(self) -> str:
        sort_name = utils.convert_japanese_to_romanji(self.name)
        return utils.remove_articles(sort_name.lower())

    def __lt__(self, other):
        return self.name < other.name & self.artist.name < other.artist.name

    def __hash__(self):
        return hash((self.name, self.artist))
