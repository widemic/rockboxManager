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