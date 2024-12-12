from pydantic import BaseModel

import utils
from music.artist import Artist


class Album(BaseModel):
    name: str
    artist: Artist

    @property
    def sort_name(self) -> str:
        return utils.remove_articles(self.name.lower())

    def __lt__(self, other):
        return self.name < other.name & self.artist.name < other.artist.name

    def __hash__(self):
        return hash((self.name, self.artist))
