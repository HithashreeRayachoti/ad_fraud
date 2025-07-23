# ml_pipeline/scripts/fix_json_format.py
import os

# --- FINAL CORRECTED FILE PATHS ---
# These now match your exact file names.
files_to_fix = [
    'ml_pipeline/data/raw/mouse_movements/humans/mouse_movements_humans.json',
    'ml_pipeline/data/raw/mouse_movements/bots/mouse_movements_advanced_bots.json',
    'ml_pipeline/data/raw/mouse_movements/bots/mouse_movements_moderate_bots.json'
]

def format_json_file(file_path):
    """
    Reads a file containing multiple JSON objects and rewrites it as a single
    JSON array, making it valid.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Skipping.")
        return

    print(f"Fixing format for: {file_path} ...")

    with open(file_path, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.write('[\n')
        content = ',\n'.join([line.strip() for line in lines if line.strip()])
        f.write(content)
        f.write('\n]')

    print(f"Successfully formatted {file_path}")


if __name__ == "__main__":
    # Assumes you run it from the root 'adfraud_kpmg' directory.
    for path in files_to_fix:
        format_json_file(path)
    print("\nAll files checked and formatted.")