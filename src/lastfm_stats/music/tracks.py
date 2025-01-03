from dataclasses import field
from statistics import median, mode, pstdev, mean
from typing import List

import pandas as pd
from pydantic import BaseModel

from lastfm_stats import utils
from lastfm_stats.data.lastfm import LastfmFetcher
from lastfm_stats.music.album import Album
from lastfm_stats.music.artist import Artist
from lastfm_stats.music.track import UniversalTrack
from lastfm_stats.music.treemap import NodePlays, NodeTracks, TreemapNode, NodeType

fetcher = LastfmFetcher()


class UniversalTracks(BaseModel):
    tracks: List[UniversalTrack] = field(default_factory=list)

    @staticmethod
    def build(initialize_data: bool = True) -> "UniversalTracks":
        ut = UniversalTracks()
        if initialize_data:
            ut.fetch_tracks()
        return ut

    def fetch_tracks(self):
        self.tracks = fetcher.fetch_recent_tracks()

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
    def average_plays_per_artist(self) -> float:
        return mean(self.artist_plays)

    @property
    def median_plays_per_artist(self) -> float:
        return median(self.artist_plays)

    @property
    def mode_plays_per_artist(self) -> float:
        return mode(self.artist_plays)

    @property
    def artist_plays_std_dev(self) -> float:
        return pstdev(self.artist_plays)

    @property
    def average_tracks_per_artist(self) -> float:
        return self.total_tracks / self.total_artists

    @property
    def average_albums_per_artist(self) -> float:
        return self.total_albums / self.total_artists

    @property
    def artists(self) -> List[Artist]:
        """
        Returns a list of all artists from list of tracks
        :return: A unique list of artists
        """
        seen = set()
        artists = []
        for artist in [track.artist for track in self.tracks]:
            if artist.id not in seen:
                seen.add(artist.id)
                artists.append(artist)
        return artists

    @property
    def artist_plays(self) -> List[int]:
        plays = []
        for artist in self.artists:
            plays.append(self.total_plays_by_artist(artist))
        return plays

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
        return list(set([track.album for track in self.tracks if track.artist.id == artist.id]))

    def tracks_by_album(self, album: Album) -> List[UniversalTrack]:
        return list(set([track for track in self.tracks if track.album.id == album.id]))

    def total_tracks_by_album(self, album: Album) -> int:
        return len(self.tracks_by_album(album))

    def total_plays_by_album(self, album: Album) -> int:
        return sum([track.plays for track in self.tracks_by_album(album)])

    @property
    def tracks_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=['Title',  # pyright: ignore [reportArgumentType]
                                   'Artist',
                                   'Album',
                                   # 'Plays',
                                   'Played At'])
        for track in sorted(self.tracks, key=lambda x: x.played_at, reverse=True):
            df_track = {
                'Title': track.title,
                'Artist': track.artist.name,
                'Album': track.album.name,
                # 'Plays': track.plays,
                'Played At': utils.convert_ts_to_local_dt(track.played_at),
            }
            df.loc[len(df)] = df_track
        return df

    @property
    def treemap_data(self) -> TreemapNode:
        root_value = 'Played Tracks'

        root = TreemapNode(node_type=NodeType.ROOT,
                           value=root_value,
                           sort_value=root_value.lower(),
                           plays=NodePlays(self.total_plays),
                           tracks=NodeTracks(self.total_tracks),
                           parent='', )

        tm_artists = []
        for artist in self.artists:
            artist_node = TreemapNode(node_type=NodeType.ARTIST,
                                      value=artist.name,
                                      sort_value=artist.sort_name,
                                      tracks=NodeTracks(self.total_tracks_by_artist(artist)),
                                      plays=NodePlays(self.total_plays_by_artist(artist)),
                                      parent=root.value)

            tm_albums = []
            for album in self.albums_by_artist(artist):
                album_node = TreemapNode(node_type=NodeType.ALBUM,
                                         value=album.name,
                                         sort_value=album.sort_name,
                                         tracks=NodeTracks(self.total_tracks_by_album(album)),
                                         plays=NodePlays(self.total_plays_by_album(album)),
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
        df = pd.DataFrame(columns=['ids', 'labels', 'parents', 'plays'])  # pyright: ignore [reportArgumentType]
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
