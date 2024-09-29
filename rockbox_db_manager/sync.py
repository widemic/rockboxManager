import shutil
import os

def sync_database(source, destination):
    """Copies the database to the Rockbox device."""
    if os.path.exists(source):
        shutil.copy(source, destination)
        print(f"Database synced to {destination}")
    else:
        print(f"Source database file {source} not found.")