# ml_pipeline/process_data.py
import pandas as pd
import json
import os
from tqdm import tqdm
from src.feature_engineering import get_mouse_features

print("Starting data processing from labeled folders...")

# --- 1. Define Paths ---
RAW_DATA_PATH = 'ml_pipeline/data/raw/mouse_movements/'
PROCESSED_DATA_PATH = 'ml_pipeline/data/processed/'
OUTPUT_FILE = os.path.join(PROCESSED_DATA_PATH, 'features.csv')

# --- THIS SECTION IS CORRECTED ---
# This dictionary now maps your exact folder and file names to the labels.
FILE_LABEL_MAP = {
    os.path.join(RAW_DATA_PATH, 'humans/mouse_movements_humans.json'): 0,
    os.path.join(RAW_DATA_PATH, 'bots/mouse_movements_advanced_bots.json'): 1,
    os.path.join(RAW_DATA_PATH, 'bots/mouse_movements_moderate_bots.json'): 1
}

# --- 2. Process Each Aggregated File ---
all_features_list = []

for file_path, label in FILE_LABEL_MAP.items():
    if not os.path.exists(file_path):
        print(f"Warning: File not found, skipping: {file_path}")
        continue

    print(f"Processing file: {file_path}")
    with open(file_path, 'r') as f:
        try:
            # Load the entire file, which is a list of session objects
            sessions_list = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Could not decode JSON from {file_path}. Error: {e}. Skipping.")
            continue

    # Iterate through each session dictionary in the list
    for session_data in tqdm(sessions_list, desc=f"Extracting from {os.path.basename(file_path)}"):
        features = get_mouse_features(session_data)
        
        if features:
            features['session_id'] = session_data.get('session_id', 'unknown_session')
            features['is_bot'] = label  # Assign the label based on the file
            all_features_list.append(features)

# --- 3. Create and Save the Final DataFrame ---
if not all_features_list:
    print("\nProcessing complete, but no valid sessions with enough mouse data were found.")
    print("An empty 'features.csv' will not be created. Please check your data.")
else:
    # Ensure the output directory exists
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    final_df = pd.DataFrame(all_features_list)
    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nProcessing complete!")
    print(f"Final dataset with {len(final_df)} sessions saved to: {OUTPUT_FILE}")