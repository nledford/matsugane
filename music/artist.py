import cutlet
from pydantic import BaseModel

import utils

# TODO move to database?
hiragana_name_overrides = {
    'あいみょん': 'Aimyon'
}

katsu = cutlet.Cutlet()


class Artist(BaseModel):
    name: str

    @property
    def id(self) -> str:
        return utils.hash_string(f'artist-{self.name.lower()}')

    @property
    def sort_name(self) -> str:
        if self.name in hiragana_name_overrides:
            sort_name = hiragana_name_overrides[self.name]
        elif utils.has_unicode_group(self.name):
            sort_name = katsu.romaji(self.name)
        elif utils.string_is_hiragana(self.name):
            sort_name = katsu.romaji(self.name)
        else:
            sort_name = self.name

        return utils.remove_articles(sort_name.lower())

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)
