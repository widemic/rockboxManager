from mutagen import File
import os
import logging
from rockbox_db_manager.cache import get_file_metadata_from_cache, update_file_metadata_in_cache

def get_text(metadata_field):
    """Helper function to extract text from mutagen metadata objects."""
    if metadata_field:
        if isinstance(metadata_field, list):
            return metadata_field[0]
        return str(metadata_field)
    return "Unknown"

def extract_full_metadata(file, cache, verbose=False):
    """Extract full metadata including title, artist, album, genre, etc., with caching."""
    cached_metadata = get_file_metadata_from_cache(cache, file)
    
    if cached_metadata:
        if verbose:  # Only log when verbose is True
            logging.info(f"Using cached metadata for {file}")
        return cached_metadata

    try:
        audio = File(file)
        title = get_text(audio.get("TIT2", "Unknown Title"))
        artist = get_text(audio.get("TPE1", "Unknown Artist"))
        album = get_text(audio.get("TALB", "Unknown Album"))
        genre = get_text(audio.get("TCON", "Unknown Genre"))
        filename = os.path.basename(file)
        composer = get_text(audio.get("TCOM", "Unknown Composer"))
        comment = get_text(audio.get("COMM", "Unknown Comment"))
        albumartist = get_text(audio.get("TPE2", None))
        grouping = get_text(audio.get("TIT1", None))

        metadata = (title, artist.split(", "), album, genre, filename, composer, comment, albumartist, grouping)
        
        # Update cache
        update_file_metadata_in_cache(cache, file, metadata)
        return metadata
    
    except Exception as e:
        logging.error(f"Error extracting metadata from file {file}: {e}")
        return "Unknown Title", ["Unknown Artist"], "Unknown Album", "Unknown Genre", os.path.basename(file), "Unknown Composer", "Unknown Comment", "Unknown", "Unknown"