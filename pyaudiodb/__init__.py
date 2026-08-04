"""pyaudiodb — TheAudioDB artist bulk harvester, grouped on harvestkit.

Importing this package imports :mod:`pyaudiodb.harvest`, which in turn
imports the scraper module so it registers itself with
:mod:`harvestkit.engine` (``@register``).
"""
from pyaudiodb.version import __version__

import pyaudiodb.harvest  # noqa: F401  (import for @register side effects)

from pyaudiodb.client import AudioDBClient
from pyaudiodb.models import (
    AudioDBArtist,
    AudioDBAlbum,
    AudioDBTrack,
)

__all__ = [
    "__version__",
    "AudioDBClient",
    "AudioDBArtist",
    "AudioDBAlbum",
    "AudioDBTrack",
]
