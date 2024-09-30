import struct

def read_binary_tcd_file(filepath):
    """Read and analyze the binary structure of a .tcd file."""
    with open(filepath, 'rb') as f:
        content = f.read()
        print(f"File: {filepath}, Size: {len(content)} bytes")

        idx = 0
        while idx < len(content):
            try:
                # Assuming the first 4 bytes represent the length of the following string
                entry_len = struct.unpack('<I', content[idx:idx+4])[0]
                idx += 4
                entry = content[idx:idx+entry_len].decode('utf-8', errors='ignore')
                idx += entry_len
                print(f"Entry (Length: {entry_len}): {entry}")
            except Exception as e:
                print(f"Failed to parse at index {idx}: {e}")
                break

