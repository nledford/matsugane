from lastfm_stats.music.album import Album, AlbumName
from lastfm_stats.music.artist import Artist, ArtistName
from lastfm_stats.music.track import PlayedAt, TrackTitle, UniversalTrack

test_timestamp = '1494824400'

test_artist = Artist(name=ArtistName("Rush"))
test_album = Album(name=AlbumName("Moving Pictures"), artist=test_artist)
test_track = UniversalTrack(title=TrackTitle("Limelight"),
                            artist=test_artist,
                            album=test_album,
                            plays=1,
                            played_at=PlayedAt(test_timestamp))


def test_track_title():
    assert test_track.title == "Limelight"


def test_album_name():
    assert test_track.album.name == "Moving Pictures"


def test_album_sort_name():
    assert test_album.sort_name == "moving pictures"
    assert test_album.sort_name != "Moving pictures"
    assert test_album.sort_name != "moving picture"


def test_album_artist():
    assert test_album.artist.name == 'Rush'
