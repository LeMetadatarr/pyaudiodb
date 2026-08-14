# Dataset

This repo produces the `audiodb_artists` dataset: a JSONL dump of music-artist metadata from TheAudioDB. The harvester seeds from the chart page, walks related-artist links in a breadth-first graph crawl, and optionally probes sequential IDs with `--fill`. No API key is required.

One row represents one artist.

## Format

The output is a JSONL file at `{output_dir}/audiodb_artists.jsonl`. Each line is a flat JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `adb_id` | string | TheAudioDB artist ID |
| `mb_id` | string or null | MusicBrainz ID |
| `name` | string | Artist name |
| `alternate_name` | string or null | Alternate name |
| `formed_year` | integer or null | Year formed |
| `born_year` | integer or null | Year born |
| `disbanded_year` | integer or null | Year disbanded or died |
| `country` | string or null | Country |
| `country_code` | string or null | Country code |
| `style` | string or null | Style |
| `genre` | string or null | Genre |
| `mood` | string or null | Mood |
| `website` | string or null | Website URL |
| `facebook` | string or null | Facebook URL |
| `twitter` | string or null | Twitter URL |
| `biography_en` | string or null | English biography, capped at 600 characters |
| `members` | integer or null | Number of members |
| `label` | string or null | Record label |
| `gender` | string or null | Gender |
| `logo_url` | string or null | Logo image URL |
| `thumb_url` | string or null | Thumbnail image URL |
| `banner_url` | string or null | Banner image URL |
| `fanart_url` | string or null | Fan-art image URL |

## How to generate

Install the package:

```bash
pip install pyaudiodb
```

The source is Cloudflare-guarded, so the `stealth` extra is recommended:

```bash
pip install "pyaudiodb[stealth]"
```

Harvest artists:

```bash
pyaudiodb-harvest audiodb_artists --output ~/.cache/metadatarr/scrapers/
```

After the graph walk finishes, probe unlinked IDs:

```bash
pyaudiodb-harvest audiodb_artists --fill --output ~/.cache/metadatarr/scrapers/
```

Python equivalent:

```python
from pathlib import Path
from pyaudiodb.harvest.audiodb_artists import AudioDBArtistsSource

src = AudioDBArtistsSource()
src.run(Path.home() / ".cache/metadatarr/scrapers")
```

## Publish on Hugging Face

Yes, with caveats. The dataset is a rich source of music-artist metadata, genre/style/mood labels, and MusicBrainz cross-links. Before publishing, confirm that redistribution of scraped text and image URLs complies with TheAudioDB terms of service.

## ML tasks served

- Music genre, style, and mood classification.
- Artist similarity and recommendation.
- Entity linking between TheAudioDB and MusicBrainz.
- Biography summarization and metadata enrichment.
- Temporal analysis of artist formation and disbandment dates.
