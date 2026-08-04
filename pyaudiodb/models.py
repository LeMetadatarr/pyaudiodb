"""Pydantic models returned by :class:`pyaudiodb.client.AudioDBClient`.

Extracted verbatim from metadatarr's ``models.py`` (AudioDB* classes). This
module has no dependency on metadatarr.
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class AudioDBArtist(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str = Field(alias="idArtist")
    name: str = Field(alias="strArtist")
    label: Optional[str] = Field(None, alias="strLabel")
    label_id: Optional[str] = Field(None, alias="idLabel")
    genre: Optional[str] = Field(None, alias="strGenre")
    style: Optional[str] = Field(None, alias="strStyle")
    mood: Optional[str] = Field(None, alias="strMood")
    biography: Optional[str] = Field(None, alias="strBiography")
    country: Optional[str] = Field(None, alias="strCountry")
    country_code: Optional[str] = Field(None, alias="strCountryCode")
    formed_year: Optional[int] = Field(None, alias="intFormedYear")
    gender: Optional[str] = Field(None, alias="strGender")
    members: Optional[int] = Field(None, alias="intMembers")
    thumb_url: Optional[str] = Field(None, alias="strArtistThumb")
    logo_url: Optional[str] = Field(None, alias="strArtistLogo")
    fanart_url: Optional[str] = Field(None, alias="strArtistFanart")
    musicbrainz_id: Optional[str] = Field(None, alias="strMusicBrainzID")

    @field_validator("formed_year", "members", mode="before")
    @classmethod
    def _coerce_int(cls, v):
        try:
            return int(v) if v not in (None, "") else None
        except (TypeError, ValueError):
            return None


class AudioDBAlbum(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str = Field(alias="idAlbum")
    artist_id: Optional[str] = Field(None, alias="idArtist")
    label_id: Optional[str] = Field(None, alias="idLabel")
    name: str = Field(alias="strAlbum")
    artist: Optional[str] = Field(None, alias="strArtist")
    year: Optional[int] = Field(None, alias="intYearReleased")
    genre: Optional[str] = Field(None, alias="strGenre")
    style: Optional[str] = Field(None, alias="strStyle")
    label: Optional[str] = Field(None, alias="strLabel")
    release_format: Optional[str] = Field(None, alias="strReleaseFormat")
    description: Optional[str] = Field(None, alias="strDescription")
    thumb_url: Optional[str] = Field(None, alias="strAlbumThumb")
    back_url: Optional[str] = Field(None, alias="strAlbumBack")
    score: Optional[float] = Field(None, alias="intScore")
    musicbrainz_id: Optional[str] = Field(None, alias="strMusicBrainzID")
    musicbrainz_artist_id: Optional[str] = Field(None, alias="strMusicBrainzArtistID")
    wikidata_id: Optional[str] = Field(None, alias="strWikidataID")
    discogs_id: Optional[str] = Field(None, alias="strDiscogsID")
    allmusic_id: Optional[str] = Field(None, alias="strAllMusicID")

    @field_validator("year", mode="before")
    @classmethod
    def _coerce_int(cls, v):
        try:
            return int(v) if v not in (None, "") else None
        except (TypeError, ValueError):
            return None


class AudioDBTrack(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str = Field(alias="idTrack")
    album_id: Optional[str] = Field(None, alias="idAlbum")
    artist_id: Optional[str] = Field(None, alias="idArtist")
    title: str = Field(alias="strTrack")
    artist: Optional[str] = Field(None, alias="strArtist")
    album: Optional[str] = Field(None, alias="strAlbum")
    track_number: Optional[int] = Field(None, alias="intTrackNumber")
    duration_ms: Optional[int] = Field(None, alias="intDuration")
    genre: Optional[str] = Field(None, alias="strGenre")
    mood: Optional[str] = Field(None, alias="strMood")
    style: Optional[str] = Field(None, alias="strStyle")
    theme: Optional[str] = Field(None, alias="strTheme")
    description: Optional[str] = Field(None, alias="strDescriptionEN")
    thumb_url: Optional[str] = Field(None, alias="strTrackThumb")
    music_vid_url: Optional[str] = Field(None, alias="strMusicVid")
    music_vid_director: Optional[str] = Field(None, alias="strMusicVidDirector")
    music_vid_company: Optional[str] = Field(None, alias="strMusicVidCompany")
    music_vid_views: Optional[int] = Field(None, alias="intMusicVidViews")
    score: Optional[float] = Field(None, alias="intScore")
    musicbrainz_id: Optional[str] = Field(None, alias="strMusicBrainzID")
    musicbrainz_album_id: Optional[str] = Field(None, alias="strMusicBrainzAlbumID")
    musicbrainz_artist_id: Optional[str] = Field(None, alias="strMusicBrainzArtistID")

    @property
    def duration_seconds(self) -> Optional[float]:
        return self.duration_ms / 1000.0 if self.duration_ms else None

    @field_validator("track_number", "duration_ms", "music_vid_views", mode="before")
    @classmethod
    def _coerce_int(cls, v):
        try:
            return int(v) if v not in (None, "") else None
        except (TypeError, ValueError):
            return None
