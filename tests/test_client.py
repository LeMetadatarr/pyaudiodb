"""Network-free smoke test for the real-time TheAudioDB query client.

The client's ``_get`` is monkeypatched to return a captured sample API
response, so parsing is exercised without ever touching the network.
"""
from __future__ import annotations

from pyaudiodb import AudioDBClient, AudioDBArtist, AudioDBAlbum, AudioDBTrack

_SAMPLE_ARTIST = {
    "idArtist": "111239",
    "strArtist": "Coldplay",
    "strGenre": "Alternative Rock",
    "strCountry": "United Kingdom",
    "intFormedYear": "1996",
    "intMembers": "4",
    "strMusicBrainzID": "cc197bad-dc9c-440d-a5b5-d52ba2e14234",
}

_SAMPLE_ALBUM = {
    "idAlbum": "2107743",
    "idArtist": "111239",
    "strAlbum": "Parachutes",
    "strArtist": "Coldplay",
    "intYearReleased": "2000",
    "strGenre": "Alternative Rock",
}

_SAMPLE_TRACK = {
    "idTrack": "32131313",
    "idAlbum": "2107743",
    "idArtist": "111239",
    "strTrack": "Yellow",
    "strArtist": "Coldplay",
    "intTrackNumber": "4",
    "intDuration": "266000",
}


def _client_with_fake_get(payload):
    client = AudioDBClient()

    def _fake_get(path, **params):
        return payload

    client._get = _fake_get
    return client


def test_search_artist_parses():
    client = _client_with_fake_get({"artists": [_SAMPLE_ARTIST]})
    artists = client.search_artist("Coldplay")
    assert len(artists) == 1
    assert isinstance(artists[0], AudioDBArtist)
    assert artists[0].id == "111239"
    assert artists[0].name == "Coldplay"
    assert artists[0].formed_year == 1996


def test_get_album_parses():
    client = _client_with_fake_get({"album": [_SAMPLE_ALBUM]})
    album = client.get_album("2107743")
    assert isinstance(album, AudioDBAlbum)
    assert album.name == "Parachutes"
    assert album.year == 2000


def test_search_track_parses():
    client = _client_with_fake_get({"track": [_SAMPLE_TRACK]})
    tracks = client.search_track("Coldplay", "Yellow")
    assert len(tracks) == 1
    assert isinstance(tracks[0], AudioDBTrack)
    assert tracks[0].title == "Yellow"
    assert tracks[0].duration_seconds == 266.0


def test_get_artist_missing_returns_none():
    client = _client_with_fake_get({"artists": None})
    assert client.get_artist("does-not-exist") is None
