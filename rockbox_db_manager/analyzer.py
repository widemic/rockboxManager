import os
import struct
import logging
import string

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Updated list of supported .tcd files based on the new information
SUPPORTED_TCD_FILES = [f"database_{i}.tcd" for i in range(9)] + ["database_12.tcd", "database_idx.tcd"]

def read_tcd_file(filepath):
    """Read and decode the binary data from a .tcd file."""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            logging.info(f"Read {len(content)} bytes from {os.path.basename(filepath)}")
            
            # Example: Decode binary data (this will depend on Rockbox's format)
            entries = []
            idx = 0
            while idx < len(content):
                try:
                    str_len = struct.unpack('<I', content[idx:idx+4])[0]  # Read the length (4 bytes)
                    idx += 4
                    entry = content[idx:idx+str_len].decode('utf-8', errors='ignore')
                    entries.append(entry)
                    idx += str_len
                except Exception as e:
                    logging.warning(f"Failed to parse entry at position {idx} in {filepath}: {e}")
                    break
            return entries
    except Exception as e:
        logging.error(f"Failed to read {filepath}: {e}")
        return []

def clean_text(text):
    """Remove non-printable characters from the text."""
    # Only keep printable characters (letters, digits, punctuation, whitespace)
    return ''.join(char if char in string.printable else '?' for char in text)

def analyze_database(db_dir, output_file):
    """Analyze all .tcd files in the directory and save the report to a file."""
    report = {}
    # Open the output file with utf-8 encoding to avoid encoding issues
    with open(output_file, 'w', encoding='utf-8') as out:
        for tcd_file in SUPPORTED_TCD_FILES:
            filepath = os.path.join(db_dir, tcd_file)
            if os.path.exists(filepath):
                logging.info(f"Analyzing {tcd_file}")
                entries = read_tcd_file(filepath)
                report[tcd_file] = entries
                logging.info(f"Found {len(entries)} entries in {tcd_file}")
            else:
                logging.warning(f"{tcd_file} not found in {db_dir}")
        
        # Write the report to the file with utf-8 encoding
        for tcd_file, entries in report.items():
            out.write(f"\n{tcd_file} contains {len(entries)} entries:\n")
            for entry in entries[:10]:  # Show the first 10 entries as a sample
                cleaned_entry = clean_text(entry)  # Clean the entry text
                out.write(f"  - {cleaned_entry}\n")
            if len(entries) > 10:
                out.write(f"  ...and {len(entries) - 10} more.\n")


