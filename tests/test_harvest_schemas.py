"""Row-schema equivalence tests for the TheAudioDB scraper.

Relocated verbatim (assertions untouched) from metadatarr's
test_scrapers_batch2.py, keeping only the tests for the scraper that lives in
this package, re-pointed at pyaudiodb.harvest.*. These lock the exact
flat-row shape the scraper emits (the contract the LeData datasets depend on)
against a realistic upstream sample, so a future engine change can't
silently alter the output schema.
"""
from __future__ import annotations

from harvestkit.engine import all_sources

from pyaudiodb.harvest.audiodb_artists import AudioDBArtistsSource


def test_audiodb_map_row_schema():
    src = AudioDBArtistsSource()
    a = {
        "idArtist": "111",
        "strArtist": "Nirvana",
        "strMusicBrainzID": "mb-x",
        "strArtistAlternate": None,
        "intFormedYear": "1987",
        "intBornYear": None,
        "intDiedYear": "1994",
        "strCountry": "United States",
        "strCountryCode": "US",
        "strStyle": "Grunge",
        "strGenre": "Rock",
        "strMood": "Angst",
        "strWebsite": "nirvana.com",
        "strFacebook": None,
        "strTwitter": None,
        "strBiographyEN": "x" * 700,
        "intMembers": "3",
        "strLabel": "DGC",
        "strGender": "Male",
        "strArtistLogo": None,
        "strArtistThumb": None,
        "strArtistBanner": None,
        "strArtistFanart": None,
    }
    row = src.map_row(a)
    assert row["adb_id"] == "111"
    assert row["name"] == "Nirvana"
    assert len(row["biography_en"]) == 600
    assert set(row) == {
        "adb_id", "mb_id", "name", "alternate_name", "formed_year", "born_year",
        "disbanded_year", "country", "country_code", "style", "genre", "mood",
        "website", "facebook", "twitter", "biography_en", "members", "label",
        "gender", "logo_url", "thumb_url", "banner_url", "fanart_url",
    }


def test_audiodb_map_row_drops_without_name_or_id():
    assert AudioDBArtistsSource().map_row({"idArtist": "1", "strArtist": ""}) is None
    assert AudioDBArtistsSource().map_row({"idArtist": None, "strArtist": "X"}) is None


def test_audiodb_fetch_seed_stage_seeds_queue(monkeypatch):
    src = AudioDBArtistsSource()
    src._html_get = lambda url: '<a href="/artist/111-nirvana">Nirvana</a><a href="/artist/222-pearl-jam">Pearl Jam</a>'
    rows, cursor = src.fetch({"stage": "seed", "queue": []})
    assert rows == []
    assert cursor == {"stage": "crawl", "queue": ["111", "222"]}


def test_audiodb_fetch_crawl_stage_pops_and_expands_queue(monkeypatch):
    src = AudioDBArtistsSource()
    src._api_get = lambda path, params: {"artists": [{"idArtist": "111", "strArtist": "Nirvana"}]}
    src._html_get = lambda url: '<a href="/artist/333-foo-fighters">Foo Fighters</a>'
    rows, cursor = src.fetch({"stage": "crawl", "queue": ["111"]})
    assert len(rows) == 1
    assert rows[0]["name"] == "Nirvana"
    assert cursor == {"stage": "crawl", "queue": ["333"]}


def test_audiodb_fetch_crawl_stage_finishes_without_fill():
    src = AudioDBArtistsSource()
    src.do_fill = False
    rows, cursor = src.fetch({"stage": "crawl", "queue": []})
    assert rows == []
    assert cursor is None


def test_audiodb_fetch_crawl_stage_moves_to_fill():
    src = AudioDBArtistsSource()
    src.do_fill = True
    rows, cursor = src.fetch({"stage": "crawl", "queue": []})
    assert rows == []
    assert cursor["stage"] == "fill"


def test_pyaudiodb_scraper_is_registered():
    reg = all_sources()
    assert reg.get("audiodb_artists") is AudioDBArtistsSource
