"""pyaudiodb.harvest — the TheAudioDB bulk scraper.

Importing this package imports the scraper module below, which registers it
with :mod:`harvestkit.engine` (via ``@register``) as a side effect. Run it
from the command line with ``pyaudiodb-harvest <name>`` (see :func:`main`),
or ``python -m harvestkit <name>`` after importing this package to populate
the registry.
"""
from __future__ import annotations

import sys

from pyaudiodb.harvest import (
    audiodb_artists,
)

__all__ = [
    "audiodb_artists",
    "main",
]


def main(argv=None) -> int:
    """Dispatch a registered scraper by name.

        pyaudiodb-harvest <name> [--output DIR] [--delay S] [--limit N]
        pyaudiodb-harvest --list

    Every module in this package is already imported (and thus registered)
    by the time this runs, since importing :mod:`pyaudiodb.harvest` itself
    imports them all.
    """
    from harvestkit.engine import all_sources, get_source, run_cli

    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in ("--list", "-l", "list"):
        for name in sorted(all_sources()):
            print(name)
        return 0

    name, rest = argv[0], argv[1:]
    try:
        source_cls = get_source(name)
    except KeyError:
        print(f"unknown scraper: {name!r}. Use --list to see available ones.",
              file=sys.stderr)
        return 2
    return run_cli(source_cls, rest)


if __name__ == "__main__":
    raise SystemExit(main())
