import argparse
from rockbox_db_manager import database, scanner, sync, cache

def prompt_if_missing(args):
    """Prompt the user for missing arguments interactively."""
    
    if not args.db_file:
        args.db_file = input("Enter the path to the output directory for the database files: ")
        
    if not args.music_dir:
        args.music_dir = input("Enter the path to the music directory: ")

    if not args.config:
        args.config = input("Enter the path to the configuration file (or press Enter to use default 'config.json'): ") or "config.json"

    return args

def main():
    parser = argparse.ArgumentParser(
        description="Rockbox Database Manager - A tool to manage your Rockbox music database"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Command to scan music directory
    scan_parser = subparsers.add_parser("scan", help="Scan a music directory for audio files")
    scan_parser.add_argument("directory", help="Path to the music directory")
    
    # Command to create/update the database
    db_parser = subparsers.add_parser("create-db", help="Create or update the Rockbox database")
    db_parser.add_argument("db_file", help="Path to the output directory for database files")
    db_parser.add_argument("music_dir", help="Path to the music directory")
    db_parser.add_argument("--config", default="config.json", help="Path to the configuration file for tag mappings")
    db_parser.add_argument("--verbose", action="store_true", help="Enable detailed logging for file processing")
    db_parser.add_argument("--show-songs", action="store_true", help="Display each song found during scanning")    
    db_parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without generating database files")
    db_parser.add_argument("--exclude", nargs='+', help="Exclude specific file types or directories")
    db_parser.add_argument("--only-artist", help="Filter and generate database only for a specific artist")
    db_parser.add_argument("--only-album", help="Filter and generate database only for a specific album")

    # Other commands
    subparsers.add_parser("clear-cache", help="Clear the metadata cache")
    subparsers.add_parser("list-supported-formats", help="List supported audio formats")
    subparsers.add_parser("validate", help="Validate the generated Rockbox database files")
    subparsers.add_parser("stats", help="Show statistics about the database")
    subparsers.add_parser("list-tags", help="List all available tags in the music files")
    
    # Command to sync database to Rockbox device
    sync_parser = subparsers.add_parser("sync", help="Sync the database to your Rockbox device")
    sync_parser.add_argument("source", help="Path to the source database file")
    sync_parser.add_argument("destination", help="Path to the Rockbox device directory")
    
    # Command to validate the database files
    validate_parser = subparsers.add_parser("validate", help="Validate the generated Rockbox database files")
    validate_parser.add_argument("db_dir", help="Path to the directory containing the generated .tcd files")

    # Command to list all tags in the music files
    list_tags_parser = subparsers.add_parser("list-tags", help="List all available tags in the music files")
    list_tags_parser.add_argument("music_dir", help="Path to the music directory")

    # Command to show stats about the database
    stats_parser = subparsers.add_parser("stats", help="Show statistics about the generated database")
    stats_parser.add_argument("db_dir", help="Path to the directory containing the generated .tcd files")
    
    # Command to clear the metadata cache
    clear_cache_parser = subparsers.add_parser("clear-cache", help="Clear the metadata cache")

    # Command to list supported formats
    list_formats_parser = subparsers.add_parser("list-supported-formats", help="List supported audio formats")

    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    if args.command == "scan":
        scanner.scan_music_directory(args.directory)
    
    elif args.command == "scan":
        scanner.scan_music_directory(args.directory)
    elif args.command == "sync":
        sync.sync_database(args.source, args.destination)
    elif args.command == "validate":
        database.validate_database(args.db_dir)
    elif args.command == "list-tags":
        database.list_tags(args.music_dir)
    elif args.command == "stats":
        database.show_stats(args.db_dir)
    elif args.command == "clear-cache":
        cache.clear_cache() 
    elif args.command == "list-supported-formats":
        scanner.list_supported_formats()
    