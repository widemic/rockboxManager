import os
import json
import logging

CACHE_FILE = "metadata_cache.json"

def load_cache():
    """Load the metadata cache from a JSON file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logging.warning("Cache file is corrupted. Starting with a new cache.")
                return {}
    return {}

def save_cache(cache):
    """Save the metadata cache to a JSON file."""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_file_metadata_from_cache(cache, filepath):
    """Check if metadata for a file is cached and still valid (based on modification time)."""
    if filepath in cache:
        cached_entry = cache[filepath]
        last_modified_time = os.path.getmtime(filepath)
        if cached_entry["mtime"] == last_modified_time:
            return cached_entry["metadata"]
    return None

def update_file_metadata_in_cache(cache, filepath, metadata):
    """Update the cache with new metadata for a file."""
    last_modified_time = os.path.getmtime(filepath)
    cache[filepath] = {
        "mtime": last_modified_time,
        "metadata": metadata
    }
def clear_cache():
    """Clear the metadata cache by removing the cache file."""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        logging.info(f"Cache cleared: {CACHE_FILE}")
    else:
        logging.info("Cache file not found.")