
# Rockbox Database Manager

A Python tool to generate and manage the Rockbox music database (`.tcd` files) for your music collection.

## Features

- Scans your music directory for supported audio files (`.mp3`, `.flac`, `.wav`, `.ogg`, `.wma`, `.aac`, `.m4a`, `.alac`, `.aiff`, `.ape`, `.wv`, `.mod`, `.spc`).
- Extracts metadata from audio files and generates Rockbox-compatible database files.
- Supports caching of metadata to speed up subsequent runs.
- Interactive CLI with options for verbose logging, displaying found songs, and more.
- Configurable tag mappings and default values for metadata fields.
- Exclude specific file types or directories from scanning.
- Filter by artist or album to only generate the database for specific tracks.

## Requirements

- Python 3.x
- Mutagen (`pip install mutagen`)
- tqdm for progress bars (`pip install tqdm`)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd rockbox-database-manager
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Create or Update Rockbox Database

```bash
python main.py create-db /path/to/output /path/to/music --config /path/to/config.json [--verbose] [--show-songs] [--dry-run] [--exclude .flac /excluded/dir] [--only-artist "Artist Name"] [--only-album "Album Name"]
```

- `db_file`: Path to the output directory for generated `.tcd` files.
- `music_dir`: Path to the directory containing your music files.
- `--config`: Path to the configuration file (default: `config.json`).
- `--verbose`: Enable detailed logging, including file processing and cache usage.
- `--show-songs`: Display each song found during the scanning process.
- `--dry-run`: Show which files would be processed without generating any database files.
- `--exclude`: Exclude specific file types or directories from the scan.
- `--only-artist`: Filter and generate the database only for a specific artist.
- `--only-album`: Filter and generate the database only for a specific album.

### Validate the Generated Database

```bash
python main.py validate /path/to/output
```

- Validates that all necessary `.tcd` files have been generated and are correctly formatted.

### List Available Tags

```bash
python main.py list-tags /path/to/music
```

- Lists all available tags in the scanned music files.

### Show Database Statistics

```bash
python main.py stats /path/to/output
```

- Displays statistics about the generated database, such as the number of artists, albums, tracks, and the size of the `.tcd` files.

### Sync Database to Rockbox Device

```bash
python main.py sync /path/to/source /path/to/rockbox/device
```

- Synchronizes the generated `.tcd` files to your Rockbox device.

### Clear Metadata Cache

```bash
python main.py clear-cache
```

- Clears the metadata cache (`metadata_cache.json`).

### List Supported Audio Formats

```bash
python main.py list-supported-formats
```

- Displays all the audio formats supported by Rockbox.

## Configuration

The tool uses a `config.json` file to customize tag mappings and default values for metadata fields. You can modify this file to suit your tagging preferences.

### Example `config.json`

```json
{
    "mappings": {
        "grouping": "title"
    },
    "default_values": {
        "artist": "Unknown Artist",
        "album": "Unknown Album",
        "title": "Unknown Title",
        "albumartist": "Unknown Album Artist"
    },
    "chunk_size": 1000
}
```

- **Mappings**: Customize how specific tags (like `grouping` or `albumartist`) are mapped to other tags (e.g., mapping `grouping` to `title`).
- **Default Values**: Specify default values for metadata fields if they are missing in a file.
- **Chunk Size**: Define the number of entries per file chunk, if needed.

## Metadata Caching

To speed up subsequent runs, the tool caches metadata for each music file in a file called `metadata_cache.json`. The cache stores metadata along with the file's last modification time (`mtime`). If a file hasn't changed since the last run, the cached metadata is reused instead of re-extracting it.

- **Cache File**: `metadata_cache.json`
- **How it works**: During the first run, the tool extracts and caches metadata. On subsequent runs, if a file hasn't changed, the cached metadata is used to avoid reprocessing.

## Supported Audio Formats

The following audio formats are supported for metadata extraction:

- `.mp3`
- `.flac`
- `.wav`
- `.ogg`
- `.wma`
- `.aac`
- `.m4a`
- `.alac`
- `.aiff`
- `.ape`
- `.wv`
- `.mod`
- `.spc`

## License

This project is licensed under the MIT License.
