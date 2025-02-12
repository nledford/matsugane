from matsugane import utils
from matsugane.data.lastfm import LastfmTrack

test_title = "Limelight"
test_artist = "Rush"
test_album = "Moving Pictures"
test_timestamp = "1494824400"

test_track = LastfmTrack(
    title=test_title,
    artist=test_artist,
    album=test_album,
    played_at=test_timestamp,
)


def test_build_sort_name():
    assert utils.build_sort_name("BAND-MAID") == "band-maid"
    assert utils.build_sort_name("The Beatles") == "beatles"
    assert utils.build_sort_name("A Fine Frenzy") == "fine frenzy"
    assert utils.build_sort_name("Rush") == "rush"
    assert utils.build_sort_name("Moving Pictures") == "moving pictures"


def test_lastfm_track():
    new_track = LastfmTrack(
        title="Limelight",
        artist="Rush",
        album="Moving Pictures",
        played_at="1494824400",
    )

    assert new_track.title == test_track.title
    assert new_track.title != "limelight"
    assert new_track.title != "COOKIES!"

    assert new_track.sort_title == utils.build_sort_name(test_title)
    assert new_track.sort_title != "Limelight"
    assert new_track.sort_title != "FUN!"

    assert (
        new_track.track_id
        == f"track-{utils.build_sort_name(test_title)}-{utils.build_sort_name(test_artist)}-{utils.build_sort_name(test_album)}"
    )
    assert (
        new_track.play_id
        == f"track-{utils.build_sort_name(test_title)}-{utils.build_sort_name(test_artist)}-{utils.build_sort_name(test_album)}-{test_timestamp}"
    )

    assert new_track.artist == test_artist
    assert new_track.artist_sort_name == utils.build_sort_name(test_artist)
