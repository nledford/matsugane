from typing import List

from attrs import define, field

from matsugane import utils
from matsugane.data.lastfm import LastfmFetcher
from matsugane.music.album import Album
from matsugane.music.artist import Artist
from matsugane.music.stats import Stats
from matsugane.music.track import UniversalTrack

fetcher = LastfmFetcher()


@define
class UniversalTracks:
    tracks: List[UniversalTrack] = []
    last_updated: str = field(default=utils.get_last_refresh())

    @staticmethod
    async def build(fetch_tracks: bool = False) -> "UniversalTracks":
        ut = UniversalTracks()
        if fetch_tracks:
            await ut.fetch_tracks()
        return ut

    async def fetch_tracks(self):
        self.tracks = await fetcher.fetch_recent_tracks()
        self.last_updated = utils.get_last_refresh()

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
        if not self.albums:
            return 0

        return len(self.albums)

    @property
    def is_empty(self) -> bool:
        return self.total_tracks <= 0

    @property
    def plays_per_artist_stats(self) -> Stats:
        return Stats(self.artist_plays)

    @property
    def plays_per_album_stats(self) -> Stats:
        return Stats(self.album_plays)

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

    @property
    def album_plays(self) -> List[int]:
        plays = []
        for album in self.albums:
            plays.append(self.total_plays_by_album(album))
        return plays

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
