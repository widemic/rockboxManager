import os
import logging
from rockbox_db_manager import metadata
from rockbox_db_manager.cache import load_cache

SUPPORTED_FORMATS = (".mp3", ".flac", ".wav", ".ogg", ".wma", ".aac", ".m4a", ".alac", ".aiff", ".ape", ".wv", ".mod", ".spc")

def scan_music_directory(directory, show_songs=False, exclude=None, only_artist=None, only_album=None):
    """Scans the directory for supported audio files and filters by artist, album, and exclusion rules."""
    music_files = []
    exclude = exclude or []
    logging.basicConfig(level=logging.DEBUG)  # Ensure logging is configured
    logging.info(f"Scanning directory: {directory}")

    # Ensure the directory path is correctly formatted
    directory = os.path.abspath(directory.strip('"'))  # Remove any extraneous quotes
    if not os.path.isdir(directory):
        logging.error(f"Error: {directory} is not a valid directory.")
        return music_files

    for root, dirs, files in os.walk(directory):
        # Exclude directories
        if any(ex_dir in root for ex_dir in exclude):
            continue
        for file in files:
            # Exclude specific file types
            if file.lower().endswith(SUPPORTED_FORMATS) and not any(file.lower().endswith(ext) for ext in exclude):
                full_path = os.path.join(root, file)
                logging.debug(f"Processing file: {full_path}")

                try:
                    # Extract metadata for the file
                    file_metadata = metadata.extract_full_metadata(full_path, load_cache())
                    
                    # Apply artist and album filters
                    if only_artist and only_artist not in file_metadata[1]:
                        continue
                    if only_album and file_metadata[2] != only_album:
                        continue

                    music_files.append(full_path)
                    
                    if show_songs:
                        print(f"Found song: {full_path}")
                
                except Exception as e:
                    logging.error(f"Failed to process file {file}: {e}")
    
    logging.info(f"Total files found: {len(music_files)}")
    return music_files