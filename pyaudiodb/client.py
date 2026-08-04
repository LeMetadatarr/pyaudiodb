from typing import List, Optional

from .version import __version__
from .transport import make_session

# Canonical user-agent string for this client. Keeping this in one place
# means a version bump doesn't need to touch the client constructor.
_USER_AGENT = f"pyaudiodb/{__version__}"

from .models import (
    AudioDBArtist,
    AudioDBAlbum,
    AudioDBTrack,
)


class AudioDBClient:
    """Client for TheAudioDB free API (key=123).

    All endpoints are read-only and require no authentication.  The free key
    ``123`` is the public key documented at theaudiodb.com/api_guide.php.
    """

    BASE = "https://www.theaudiodb.com/api/v1/json/123"

    def __init__(self, user_agent: str = _USER_AGENT):
        self._session = make_session()
        self._session.headers["User-Agent"] = user_agent
        self._session.headers["Accept"] = "application/json"

    def _get(self, path: str, **params) -> dict:
        try:
            r = self._session.get(f"{self.BASE}/{path}", params=params, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception:
            return {}

    # ------------------------------------------------------------------
    # Artist
    # ------------------------------------------------------------------

    def search_artist(self, name: str) -> List[AudioDBArtist]:
        data = self._get("search.php", s=name)
        return [AudioDBArtist.model_validate(a) for a in (data.get("artists") or [])]

    def get_artist(self, audiodb_id: str) -> Optional[AudioDBArtist]:
        data = self._get("artist.php", i=audiodb_id)
        artists = data.get("artists") or []
        return AudioDBArtist.model_validate(artists[0]) if artists else None

    def get_artist_by_mbid(self, mbid: str) -> Optional[AudioDBArtist]:
        data = self._get("artist-mb.php", i=mbid)
        artists = data.get("artists") or []
        return AudioDBArtist.model_validate(artists[0]) if artists else None

    # ------------------------------------------------------------------
    # Album
    # ------------------------------------------------------------------

    def search_album(self, artist: str, album: Optional[str] = None) -> List[AudioDBAlbum]:
        params = {"s": artist}
        if album:
            params["a"] = album
        data = self._get("searchalbum.php", **params)
        return [AudioDBAlbum.model_validate(a) for a in (data.get("album") or [])]

    def get_album(self, audiodb_id: str) -> Optional[AudioDBAlbum]:
        data = self._get("album.php", i=audiodb_id)
        albums = data.get("album") or []
        return AudioDBAlbum.model_validate(albums[0]) if albums else None

    def get_album_by_mbid(self, mbid: str) -> Optional[AudioDBAlbum]:
        data = self._get("album-mb.php", i=mbid)
        albums = data.get("album") or []
        return AudioDBAlbum.model_validate(albums[0]) if albums else None

    def discography(self, artist: str) -> List[AudioDBAlbum]:
        """Lightweight discography — returns album name + year only (free tier)."""
        data = self._get("discography.php", s=artist)
        out = []
        for raw in data.get("album") or []:
            try:
                out.append(AudioDBAlbum.model_validate(raw))
            except Exception:
                pass
        return out

    # ------------------------------------------------------------------
    # Track
    # ------------------------------------------------------------------

    def search_track(self, artist: str, title: str) -> List[AudioDBTrack]:
        data = self._get("searchtrack.php", s=artist, t=title)
        return [AudioDBTrack.model_validate(t) for t in (data.get("track") or [])]

    def get_track(self, audiodb_id: str) -> Optional[AudioDBTrack]:
        data = self._get("track.php", h=audiodb_id)
        tracks = data.get("track") or []
        return AudioDBTrack.model_validate(tracks[0]) if tracks else None

    def get_track_by_mbid(self, mbid: str) -> Optional[AudioDBTrack]:
        data = self._get("track-mb.php", i=mbid)
        tracks = data.get("track") or []
        return AudioDBTrack.model_validate(tracks[0]) if tracks else None
