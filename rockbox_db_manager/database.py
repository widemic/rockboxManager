import logging
import os
from tqdm import tqdm
import struct
from rockbox_db_manager import metadata, scanner
from rockbox_db_manager.config import load_config, get_mapping, get_default_value
from rockbox_db_manager.cache import save_cache, load_cache

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("rockbox_db_manager.log"),
        logging.StreamHandler()
    ]
)
def validate_database(db_dir):
    """Validate the generated .tcd files."""
    required_files = [f"database_{i}.tcd" for i in range(9)] + ["database_idx.tcd"]
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(db_dir, f))]
    
    if missing_files:
        logging.error(f"Missing files: {missing_files}")
        return False
    logging.info("All required files are present.")
    return True

def list_tags(music_dir):
    """List all available tags in the music files."""
    music_files = scanner.scan_music_directory(music_dir)
    tags = set()
    
    for file in music_files:
        try:
            _, artists, album, genre, _, composer, comment, albumartist, grouping = metadata.extract_full_metadata(file)
            tags.update(["artist", "album", "genre", "composer", "comment", "albumartist", "grouping"])
        except Exception as e:
            logging.error(f"Failed to process file {file}: {e}")
    
    logging.info(f"Available tags: {', '.join(tags)}")

def show_stats(db_dir):
    """Show statistics about the generated database."""
    stats = {}
    
    for i in range(9):
        filepath = os.path.join(db_dir, f"database_{i}.tcd")
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                content = f.read()
                stats[f"database_{i}.tcd"] = len(content)
    
    stats["database_idx.tcd"] = os.path.getsize(os.path.join(db_dir, "database_idx.tcd"))
    
    logging.info("Database Stats:")
    for file, size in stats.items():
        logging.info(f"{file}: {size} bytes")
# Helper functions for writing binary data
def write_int(f, value):
    """Write an integer in little-endian format."""
    f.write(struct.pack('<I', value))

def write_string(f, value):
    """Write a string as a length-prefixed byte array."""
    if not isinstance(value, str):
        value = str(value)  # Ensure it's a string
    encoded = value.encode('utf-8')
    write_int(f, len(encoded))
    f.write(encoded)

def clean_metadata(metadata_value, default_value):
    """Clean the metadata value and return either a valid value or a default."""
    return metadata_value.strip() if metadata_value and metadata_value.strip() else default_value

def create_tag_file(tag_file, tag_data):
    """Creates a tag-specific .tcd file with the provided metadata."""
    logging.info(f"Creating tag file: {tag_file}")
    try:
        with open(tag_file, 'wb') as f:
            for entry in tag_data:
                write_string(f, entry)
    except Exception as e:
        logging.error(f"Failed to create tag file {tag_file}: {e}")

from tqdm import tqdm

def create_rockbox_tagcache(output_dir, music_files, config_file, verbose=False):
    """Generates Rockbox .tcd files for all tags based on music files metadata and configurable mappings."""
    # Initialize the cache
    cache = load_cache()

    config = load_config(config_file)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logging.info(f"Generating tagcache files in: {output_dir}")

    # Paths for tag files
    tag_files = {
        'artist': os.path.join(output_dir, 'database_0.tcd'),
        'album': os.path.join(output_dir, 'database_1.tcd'),
        'genre': os.path.join(output_dir, 'database_2.tcd'),
        'title': os.path.join(output_dir, 'database_3.tcd'),
        'filename': os.path.join(output_dir, 'database_4.tcd'),
        'composer': os.path.join(output_dir, 'database_5.tcd'),
        'comment': os.path.join(output_dir, 'database_6.tcd'),
        'albumartist': os.path.join(output_dir, 'database_7.tcd'),
        'grouping': os.path.join(output_dir, 'database_8.tcd')
    }
    
    # Initialize tag data storage
    tag_data = {key: set() for key in tag_files}  # Use sets to avoid duplicate entries
    
    # Add progress bar for large libraries
    for file in tqdm(music_files, desc="Processing files"):
        try:
            title, artists, album, genre, filename, composer, comment, albumartist, grouping = metadata.extract_full_metadata(file, cache, verbose=verbose)
            
            if verbose:
                logging.info(f"Processing file: {file}")
            
            # Clean metadata before processing
            title = clean_metadata(title, get_default_value(config, 'title'))
            album = clean_metadata(album, get_default_value(config, 'album'))
            filename = clean_metadata(filename, filename)  # filename should not default
            composer = clean_metadata(composer, get_default_value(config, 'composer'))
            comment = clean_metadata(comment, get_default_value(config, 'comment'))
            albumartist = clean_metadata(albumartist, get_default_value(config, 'albumartist'))
            grouping = clean_metadata(grouping, title)  # If grouping is missing, use the title
            
            # Use configurable mappings
            title = grouping if get_mapping(config, 'grouping') == 'title' else title
            
            # Write each artist separately, clean each artist string
            for artist in artists:
                cleaned_artist = clean_metadata(artist, get_default_value(config, 'artist'))
                tag_data['artist'].add(cleaned_artist)
            
            tag_data['album'].add(album)
            tag_data['genre'].add(clean_metadata(genre, "Unknown Genre"))
            tag_data['title'].add(title)
            tag_data['filename'].add(filename)
            tag_data['composer'].add(composer)
            tag_data['comment'].add(comment)
            tag_data['albumartist'].add(albumartist)
            tag_data['grouping'].add(grouping)
        
        except Exception as e:
            logging.error(f"Failed to process file {file}: {e}")

    # Write data to individual tag files
    for tag, filepath in tag_files.items():
        create_tag_file(filepath, tag_data[tag])

    # Save the updated cache after processing
    save_cache(cache)

    logging.info(f"Tagcache files generated in {output_dir}")

def create_master_index_file(output_dir, num_entries):
    """Creates the master index file (database_idx.tcd) for all tracks."""
    index_file = os.path.join(output_dir, 'database_idx.tcd')
    
    logging.info(f"Creating master index file: {index_file}")
    
    try:
        with open(index_file, 'wb') as f:
            # Write the number of entries
            write_int(f, num_entries)
            
            # Placeholder: Write index data for each entry (custom format)
            for i in range(num_entries):
                write_int(f, i)  # Placeholder for real index data
        logging.info(f"Master index file created successfully: {index_file}")
    except Exception as e:
        logging.error(f"Failed to create master index file: {e}")

def create_rockbox_database(output_dir, music_dir, config_file, verbose=False, show_songs=False, dry_run=False, exclude=None, only_artist=None, only_album=None):
    """Main function to create Rockbox database files."""
    
    logging.info(f"Starting database generation for music directory: {music_dir}")
    
    try:
        music_files = scanner.scan_music_directory(music_dir, show_songs=show_songs, exclude=exclude, only_artist=only_artist, only_album=only_album)
        
        if not music_files:
            logging.error(f"No supported audio files found in the directory: {music_dir}. Please check the directory or use the --exclude option if needed.")
            return
        
        if dry_run:
            print(f"Dry run: Files to be processed:")
            for file in music_files:
                print(file)
            return

        # Generate tagcache files
        create_rockbox_tagcache(output_dir, music_files, config_file, verbose=verbose)
        create_master_index_file(output_dir, len(music_files))
        
        logging.info("Rockbox database generation complete.")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}. Please check the provided paths.")
    except PermissionError as e:
        logging.error(f"Permission error: {e}. Please ensure you have access to the specified files or directories.")
    except Exception as e:
        logging.error(f"Unexpected error during database generation: {e}")