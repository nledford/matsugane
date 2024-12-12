from dataclasses import field
from typing import List

from pydantic import BaseModel

from data.lastfm import LastfmFetcher
from music.album import Album
from music.artist import Artist
from music.track import UniversalTrack
from music.treemap import TreemapNode, NodeType


class UniversalTracks(BaseModel):
    tracks: List[UniversalTrack] = field(default_factory=list)

    def fetch_tracks(self):
        fetcher = LastfmFetcher()
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
    def artists(self) -> List[Artist]:
        """
        Returns a list of all artists from list of tracks
        :return: A unique list of artists
        """
        return list(set([track.artist for track in self.tracks]))

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
        root = TreemapNode(node_type=NodeType.ROOT,
                           value='Tracks',
                           sort_value='tracks',
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
                                      parent='Total Plays')

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
