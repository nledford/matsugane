from dataclasses import field
from typing import List

import pandas as pd
from pydantic import BaseModel

from data.lastfm import LastfmFetcher
from music.album import Album
from music.artist import Artist
from music.track import UniversalTrack
from music.treemap import TreemapNode, NodeType

fetcher = LastfmFetcher()

class UniversalTracks(BaseModel):
    tracks: List[UniversalTrack] = field(default_factory=list)

    @staticmethod
    def build() -> "UniversalTracks":
        ut = UniversalTracks()
        ut.fetch_tracks()
        return ut

    def fetch_tracks(self):
        self.tracks = fetcher.fetch_recent_tracks()

    # @property
    # def tracks(self) -> List[UniversalTrack]:
    #     return self.__tracks

    @property
    def total_tracks(self) -> int:
        return len(self.tracks)

    @property
    def total_plays(self) -> int:
        return sum([track.plays for track in self.tracks])

    @property
    def total_artists(self) -> int:
        return len(self.artists)

    @property
    def total_albums(self) -> int:
        return len(self.albums)

    @property
    def artists(self) -> List[Artist]:
        """
        Returns a list of all artists from list of tracks
        :return: A unique list of artists
        """
        return list(set([track.artist for track in self.tracks]))

    @property
    def albums(self) -> List[Album]:
        return list(set([track.album for track in self.tracks]))

    def tracks_by_artist(self, artist: Artist) -> List[UniversalTrack]:
        return list(set([track for track in self.tracks if track.artist == artist]))

    def total_tracks_by_artist(self, artist: Artist) -> int:
        return len(self.tracks_by_artist(artist))

    def total_plays_by_artist(self, artist: Artist) -> int:
        return sum([track.plays for track in self.tracks_by_artist(artist)])

    def albums_by_artist(self, artist: Artist) -> List[Album]:
        return list(set([track.album for track in self.tracks if track.artist == artist]))

    def tracks_by_album(self, album: Album) -> List[UniversalTrack]:
        return list(set([track for track in self.tracks if track.album == album]))

    def total_tracks_by_album(self, album: Album) -> int:
        return len(self.tracks_by_album(album))

    def total_plays_by_album(self, album: Album) -> int:
        return sum([track.plays for track in self.tracks_by_album(album)])

    @property
    def treemap_data(self) -> TreemapNode:
        # df["Total Plays"] = f'Total Plays | {len(artists)} artists | {len(tracks)} tracks | {sum(plays)} plays'
        root_value = f'Played Tracks | {self.total_artists} artists | {self.total_albums} albums | {self.total_tracks} tracks | {self.total_plays} plays'

        root = TreemapNode(node_type=NodeType.ROOT,
                           value=root_value,
                           sort_value=root_value.lower(),
                           plays=self.total_plays,
                           tracks=self.total_tracks,
                           parent='', )

        tm_artists = []
        for artist in self.artists:
            artist_node = TreemapNode(node_type=NodeType.ARTIST,
                                      value=artist.name,
                                      sort_value=artist.sort_name,
                                      tracks=self.total_tracks_by_artist(artist),
                                      plays=self.total_plays_by_artist(artist),
                                      parent=root_value)

            tm_albums = []
            for album in self.albums_by_artist(artist):
                album_node = TreemapNode(node_type=NodeType.ALBUM,
                                         value=album.name,
                                         sort_value=album.sort_name,
                                         tracks=self.total_tracks_by_album(album),
                                         plays=self.total_plays_by_album(album),
                                         parent=artist_node.id)
                tm_albums.append(album_node)

            artist_node.children = tm_albums
            tm_artists.append(artist_node)
        tm_artists.sort(key=lambda x: x.sort_value)
        tm_artists.sort(key=lambda x: x.plays, reverse=True)

        root.children = tm_artists

        return root

    @property
    def treemap_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=['ids', 'labels', 'parents', 'plays'])
        for node in sorted(self.treemap_data.children, key=lambda x: x.sort_value):
            df_artist = {
                'ids': node.id,
                'labels': node.value,
                'parents': node.parent,
                'plays': sum([child.plays for child in node.children]) if node.children else node.plays,
            }
            df.loc[len(df)] = df_artist
            for album in sorted(node.children, key=lambda x: x.sort_value):
                df_album = {
                    'ids': album.id,
                    'labels': album.value,
                    'parents': album.parent,
                    'plays': album.plays,
                }
                df.loc[len(df)] = df_album

        return df
