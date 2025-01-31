from statistics import mean, median, mode, pstdev
from typing import List

import pandas as pd
from attrs import define

from matsugane import utils
from matsugane.data.lastfm import LastfmFetcher
from matsugane.music.album import Album
from matsugane.music.artist import Artist
from matsugane.music.track import UniversalTrack
from matsugane.music.treemap import NodePlays, NodeTracks, NodeType, TreemapNode

fetcher = LastfmFetcher()


@define
class UniversalTracks:
    tracks: List[UniversalTrack] = []

    def fetch_tracks(self):
        self.tracks = fetcher.fetch_recent_tracks()

    @property
    def unique_tracks(self) -> List[UniversalTrack]:
        return list(utils.remove_duplicates(self.tracks, key=lambda t: t.id))

    @property
    def total_tracks(self) -> int:
        return len(self.unique_tracks)

    @property
    def total_plays(self) -> int:
        return sum([track.plays for track in self.tracks])

    @property
    def total_artists(self) -> int:
        if not self.artists:
            return 0

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
    def average_plays_per_album(self) -> float:
        return self.total_plays / self.total_albums

    @property
    def artists(self) -> List[Artist]:
        """
        Returns a list of all artists from list of tracks
        :return: A unique list of artists
        """

        # First check if we have any tracks and return an empty list if not
        if not self.tracks:
            return []

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
        seen = set()
        albums = []
        for album in [track.album for track in self.tracks]:
            if album.id not in seen:
                seen.add(album.id)
                albums.append(album)
        return albums

    def tracks_by_artist(self, artist: Artist) -> List[UniversalTrack]:
        return list(
            set([track for track in self.tracks if track.artist.id == artist.id])
        )

    def total_tracks_by_artist(self, artist: Artist) -> int:
        return len(self.tracks_by_artist(artist))

    def total_plays_by_artist(self, artist: Artist) -> int:
        return sum([track.plays for track in self.tracks_by_artist(artist)])

    def albums_by_artist(self, artist: Artist) -> List[Album]:
        seen = set()
        albums = []
        for album in [
            track.album for track in self.tracks if track.artist.id == artist.id
        ]:
            if album.id not in seen:
                seen.add(album.id)
                albums.append(album)
        return albums

    def tracks_by_album(self, album: Album) -> List[UniversalTrack]:
        return list(set([track for track in self.tracks if track.album.id == album.id]))

    def total_tracks_by_album(self, album: Album) -> int:
        return len(self.tracks_by_album(album))

    def total_plays_by_album(self, album: Album) -> int:
        return sum([track.plays for track in self.tracks_by_album(album)])

    @property
    def tracks_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(
            columns=[
                "Title",  # pyright: ignore [reportArgumentType]
                "Artist",
                "Album",
                # 'Plays',
                "Played At",
            ]
        )
        for track in sorted(self.tracks, key=lambda x: x.played_at, reverse=True):
            df_track = {
                "Title": track.title,
                "Artist": track.artist.name,
                "Album": track.album.name,
                # 'Plays': track.plays,
                "Played At": utils.convert_ts_to_local_dt(track.played_at),
            }
            df.loc[len(df)] = df_track
        return df

    @property
    def treemap_data(self) -> TreemapNode:
        root_value = "Played Tracks"

        root = TreemapNode(
            node_type=NodeType.ROOT,
            value=root_value,
            sort_value=root_value.lower(),
            plays=NodePlays(self.total_plays),
            tracks=NodeTracks(self.total_tracks),
            parent="",
        )

        tm_artists = []
        for artist in self.artists:
            artist_node = TreemapNode(
                node_type=NodeType.ARTIST,
                value=artist.name,
                sort_value=artist.sort_name,
                tracks=NodeTracks(self.total_tracks_by_artist(artist)),
                plays=NodePlays(self.total_plays_by_artist(artist)),
                parent=root.value,
            )

            tm_albums = []
            for album in self.albums_by_artist(artist):
                album_node = TreemapNode(
                    node_type=NodeType.ALBUM,
                    value=album.name,
                    sort_value=album.sort_name,
                    tracks=NodeTracks(self.total_tracks_by_album(album)),
                    plays=NodePlays(self.total_plays_by_album(album)),
                    parent=artist_node.id,
                )

                tm_tracks = []
                for track in self.tracks_by_album(album):
                    track_node = TreemapNode(
                        node_type=NodeType.TRACK,
                        value=track.title,
                        sort_value=track.sort_name,
                        plays=NodePlays(track.plays),
                        parent=album_node.id,
                        tracks=NodeTracks(1),
                    )
                    tm_tracks.append(track_node)
                album_node.children = tm_tracks
                tm_albums.append(album_node)

            artist_node.children = tm_albums
            tm_artists.append(artist_node)
        tm_artists.sort(key=lambda x: x.sort_value)
        tm_artists.sort(key=lambda x: x.plays, reverse=True)

        root.children = tm_artists

        return root

    @property
    def treemap_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=["ids", "labels", "parents", "plays"])  # pyright: ignore [reportArgumentType]
        for node in sorted(self.treemap_data.children, key=lambda x: x.sort_value):
            df_artist = {
                "ids": node.id,
                "labels": node.value,
                "parents": node.parent,
                "plays": sum([child.plays for child in node.children])
                if node.children
                else node.plays,
            }
            df.loc[len(df)] = df_artist
            for album in sorted(node.children, key=lambda x: x.sort_value):
                df_album = {
                    "ids": album.id,
                    "labels": album.value,
                    "parents": album.parent,
                    "plays": album.plays,
                }
                df.loc[len(df)] = df_album
                for track in sorted(album.children, key=lambda x: x.sort_value):
                    df_track = {
                        "ids": track.id,
                        "labels": track.value,
                        "parents": track.parent,
                        "plays": track.plays,
                    }
                    df.loc[len(df)] = df_track

        return df
