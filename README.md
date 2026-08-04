# pyaudiodb

TheAudioDB artist bulk harvester (HTML seed + free JSON API + graph-walk)
grouped onto the [harvestkit](https://github.com/LeMetadatarr/harvestkit)
resumable-harvest engine. Extracted from
[metadatarr](https://github.com/TigreGotico/metadatarr)'s scraper collection
into its own standalone package.

Also ships a real-time query client (`from pyaudiodb import AudioDBClient`) alongside the bulk harvester.

## Sources

| Scraper | Registry name | Source |
| --- | --- | --- |
| `audiodb_artists` | `audiodb_artists` | TheAudioDB, seed + BFS graph-walk + optional `--fill` probe (no API key) |

TheAudioDB is Cloudflare-guarded, so the scraper prefers `unblock_requests`'
`CloudflareSession` when available and falls back to plain `requests`
otherwise — install the `stealth` extra for reliable access.

## Install

```bash
pip install pyaudiodb
# or, for the HuggingFace publisher (via harvestkit):
pip install "pyaudiodb[hf]"
# recommended — this source is Cloudflare-guarded:
pip install "pyaudiodb[stealth]"
```

## Usage

```bash
# list every registered scraper
pyaudiodb-harvest --list

# harvest the source (resumable — safe to Ctrl-C and rerun)
pyaudiodb-harvest audiodb_artists --output ~/.cache/metadatarr/scrapers/

# after the graph-walk queue empties, sequentially probe unlinked IDs
pyaudiodb-harvest audiodb_artists --fill
```

Every scraper is a `harvestkit.engine.Source` subclass: checkpoint/dedup/
pagination/throttle are handled by the shared engine, each module only
answers `initial_cursor()` and `fetch(cursor)`. See
[harvestkit](https://github.com/LeMetadatarr/harvestkit) for the full engine
API.

## License

Apache-2.0
