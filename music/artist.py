from pydantic import BaseModel

import utils


class Artist(BaseModel):
    name: str

    @property
    def id(self) -> str:
        return utils.hash_string(f'artist-{self.name.lower()}')

    @property
    def sort_name(self) -> str:
        return utils.remove_articles(self.name.lower())

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)