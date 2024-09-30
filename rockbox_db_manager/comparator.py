import os
import filecmp

def compare_databases(working_db_dir, generated_db_dir):
    """Compare files in the working and generated Rockbox databases."""
    for tcd_file in os.listdir(working_db_dir):
        working_file = os.path.join(working_db_dir, tcd_file)
        generated_file = os.path.join(generated_db_dir, tcd_file)

        if not os.path.exists(generated_file):
            print(f"Missing generated file: {tcd_file}")
            continue

        # Compare the contents of the files
        if filecmp.cmp(working_file, generated_file, shallow=False):
            print(f"{tcd_file} is identical.")
        else:
            print(f"{tcd_file} differs between the working and generated databases.")
