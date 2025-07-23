# ml_pipeline/scripts/fix_json_format_robust.py
import json
import os

# --- CORRECTED FILE PATHS ---
files_to_fix = [
    'ml_pipeline/data/raw/mouse_movements/humans/mouse_movements_humans.json',
    'ml_pipeline/data/raw/mouse_movements/bots/mouse_movements_advanced_bots.json',
    'ml_pipeline/data/raw/mouse_movements/bots/mouse_movements_moderate_bots.json'
]

def format_json_file(file_path):
    """
    Reads a file containing multiple JSON objects (one per line) and
    rewrites it as a single, valid JSON array.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Skipping.")
        return

    print(f"Robustly fixing format for: {file_path} ...")

    valid_sessions = []
    with open(file_path, 'r') as f:
        for line in f:
            # Ignore empty lines
            if not line.strip():
                continue
            try:
                # Try to load each line as a separate JSON object
                valid_sessions.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"  - Warning: Skipping malformed line in {os.path.basename(file_path)}")
                continue

    # Now, overwrite the original file with the correctly formatted array
    with open(file_path, 'w') as f:
        json.dump(valid_sessions, f, indent=4) # indent=4 makes it human-readable

    print(f"Successfully formatted {file_path} with {len(valid_sessions)} valid objects.")


if __name__ == "__main__":
    for path in files_to_fix:
        format_json_file(path)
    print("\nAll files have been formatted.")