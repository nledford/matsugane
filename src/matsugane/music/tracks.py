from typing import List

from attrs import define, field

from matsugane import utils
from matsugane.data.lastfm import LastfmFetcher, LastfmTrack
from matsugane.music.album import Album, AlbumName
from matsugane.music.artist import Artist, ArtistName
from matsugane.music.track import TrackTitle, UniversalTrack

fetcher = LastfmFetcher()


@define
class Node:
    id: str
    name: str
    children: List["Node"] = field(factory=lambda: [])


@define
class UniversalTracks:
    lastfm_tracks: List[LastfmTrack] = []
    last_updated: str = field(default=utils.get_last_refresh())
    _tracks: List[Artist] = []

    @staticmethod
    async def build(fetch_tracks: bool = False) -> "UniversalTracks":
        ut = UniversalTracks()
        if fetch_tracks:
            await ut.fetch_tracks()
        return ut

    async def fetch_tracks(self):
        self.lastfm_tracks = await fetcher.fetch_recent_tracks()
        self.last_updated = utils.get_last_refresh()

    @property
    def artists(self) -> List[Artist]:
        raw_artists = set([track.artist for track in self.lastfm_tracks])

        artists = []

        for raw_artist in raw_artists:
            artist = Artist(ArtistName(raw_artist))
            albums = self.albums_by_artist(artist)
            artist._albums = albums
            artists.append(artist)

        return sorted(artists, key=lambda a: a.sort_name)

    def albums_by_artist(self, artist: Artist) -> List[Album]:
        raw_albums = set(
            [track.album for track in self.lastfm_tracks if track.artist == artist.name]
        )
        albums = []
        for raw_album in raw_albums:
            album = Album(AlbumName(raw_album))
            album._tracks = self.tracks_by_album(artist, album)
            albums.append(album)

        return sorted(albums, key=lambda a: a.sort_name)

    def tracks_by_album(self, artist: Artist, album: Album) -> List[UniversalTrack]:
        raw_tracks = set(
            [
                track
                for track in self.lastfm_tracks
                if track.artist == artist.name and track.album == album.name
            ]
        )

        plays_dict = dict()
        played_at_dict: dict[str, List[str]] = dict()
        for raw_track in raw_tracks:
            plays_dict[raw_track.title] = plays_dict.get(raw_track.title, 0) + 1
            played_at_dict.setdefault(raw_track.title, [])
            played_at_dict[raw_track.title].append(raw_track.played_at)

        tracks = []
        for raw_track in raw_tracks:
            track = UniversalTrack(
                TrackTitle(raw_track.title),
                plays=plays_dict[raw_track.title],
                played_at=played_at_dict[raw_track.title],
            )
            tracks.append(track)
        return sorted(tracks, key=lambda t: t.sort_name)

    # @property
    # def unique_tracks(self) -> List[UniversalTrack]:
    #     return list(utils.remove_duplicates(self.lastfm_tracks, key=lambda t: t.id))
    #
    # @property
    # def total_tracks(self) -> int:
    #     return len(self.unique_tracks)
    #
    # @property
    # def total_plays(self) -> int:
    #     return sum([track.plays for track in self.lastfm_tracks])
    #
    # @property
    # def total_artists(self) -> int:
    #     if not self.artists:
    #         return 0
    #
    #     return len(self.artists)
    #
    # @property
    # def total_albums(self) -> int:
    #     if not self.albums:
    #         return 0
    #
    #     return len(self.albums)
    #
    # @property
    # def is_empty(self) -> bool:
    #     return self.total_tracks <= 0 or len(self.lastfm_tracks) == 0
    #
    # @property
    # def plays_per_artist_stats(self) -> Stats:
    #     return Stats(self.artist_plays)
    #
    # @property
    # def plays_per_album_stats(self) -> Stats:
    #     return Stats(self.album_plays)
    #
    # @property
    # def artists(self) -> List[Artist]:
    #     """
    #     Returns a list of all artists from list of tracks
    #     :return: A unique list of artists
    #     """
    #
    #     # First check if we have any tracks and return an empty list if not
    #     if not self.lastfm_tracks:
    #         return []
    #
    #     seen = set()
    #     artists = []
    #     for artist in [track.artist for track in self.lastfm_tracks]:
    #         if artist.id not in seen:
    #             seen.add(artist.id)
    #             artists.append(artist)
    #     return artists
    #
    # @property
    # def artist_plays(self) -> List[int]:
    #     plays = []
    #     for artist in self.artists:
    #         plays.append(self.total_plays_by_artist(artist))
    #     return plays
    #
    #
    # @property
    # def albums(self) -> List[Album]:
    #     seen = set()
    #     albums = []
    #     for album in [track.album for track in self.lastfm_tracks]:
    #         if album.id not in seen:
    #             seen.add(album.id)
    #             albums.append(album)
    #     return albums
    #
    # @property
    # def album_plays(self) -> List[int]:
    #     plays = []
    #     for album in self.albums:
    #         plays.append(self.total_plays_by_album(album))
    #     return plays
    #
    # def tracks_by_artist(self, artist: Artist) -> List[UniversalTrack]:
    #     return list(
    #         set([track for track in self.lastfm_tracks if track.artist.id == artist.id])
    #     )
    #
    # def total_tracks_by_artist(self, artist: Artist) -> int:
    #     return len(self.tracks_by_artist(artist))
    #
    # def total_plays_by_artist(self, artist: Artist) -> int:
    #     return sum([track.plays for track in self.tracks_by_artist(artist)])
    #
    # def albums_by_artist(self, artist: Artist) -> List[Album]:
    #     seen = set()
    #     albums = []
    #     for album in [
    #         track.album for track in self.lastfm_tracks if track.artist.id == artist.id
    #     ]:
    #         if album.id not in seen:
    #             seen.add(album.id)
    #             albums.append(album)
    #     return albums
    #
    # def tracks_by_album(self, album: Album) -> List[UniversalTrack]:
    #     return list(set([track for track in self.lastfm_tracks if track.album.id == album.id]))
    #
    # def total_tracks_by_album(self, album: Album) -> int:
    #     return len(self.tracks_by_album(album))
    #
    # def total_plays_by_album(self, album: Album) -> int:
    #     return sum([track.plays for track in self.tracks_by_album(album)])
