import pandas as pd
import os

base_path = r'd:\AF\ad_fraud\MachineLearning\phase1'

annotations_path = os.path.join(base_path, 'annotations/humans_and_advanced_bots')

train_df_labels = pd.read_csv(os.path.join(annotations_path,'train'), sep=' ', names=['session_id','label'])
test_df_labels = pd.read_csv(os.path.join(annotations_path,'test'), sep=' ', names=['session_id','label'])

print("Train labels loaded:")
print(train_df_labels.head())
print ("\n")

#========  PART 2=========
# import os
import json
import re
import ast

# def parse_mouse_data_from_file(session_id: str, data_subset_folder: str, base_path: str):



def parse_mouse_data_from_file(session_id: str, data_subset_folder: str, base_path: str):
    """
    Reads and parses the mouse movement JSON file.
    Safely extracts coordinates, timestamps, and user actions.
    """
    file_path = os.path.join(base_path, 'data', 'mouse_movements', data_subset_folder, session_id, 'mouse_movements.json')

    try:
        with open(file_path, 'r') as f:
            text_data = f.read()
            # Handle some broken formatting
            text_data = text_data.replace('}"', '},"')

        data = json.loads(text_data)

        # === Coordinates ===
        coords_str = data.get('mousemove_total_behaviour', '').strip()
        try:
            # Match coordinate pairs like [123, 456]
            coord_pairs = re.findall(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', coords_str)
            coords = [(int(x), int(y)) for x, y in coord_pairs]
        except Exception as e:
            print(f"Coordinate parse error for session {session_id}: {e}")
            coords = []

        # === Timestamps ===
        times_str = data.get('mousemove_times', '').strip('{}()[] \n')
        try:
            times = [int(t) for t in times_str.split(',') if t.strip().isdigit()]
        except Exception as e:
            print(f"Timestamp parse error for session {session_id}: {e}")
            times = []

        # === Actions (clicks, moves, etc.) ===
        actions_str = data.get('total_behaviour', '')
        try:
            actions = re.findall(r'c\(\w\)|m\(\d+,\d+\)', actions_str)
        except Exception as e:
            print(f"Action parse error for session {session_id}: {e}")
            actions = []

        return {
            'session_id': session_id,
            'coordinates': coords,
            'timestamps': times,
            'actions': actions
        }

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not parse file for session {session_id}. Error: {e}")
        return None

    """
    Parses mouse movement data from a JSON file for a given session.

    Args:
        session_id (str): The session ID to look up.
        data_subset_folder (str): Sub-folder inside 'mouse_movements' (e.g., 'humans_and_advanced_bots').
        base_path (str): Base path to the 'phase1' folder.

    Returns:
        dict: Parsed mouse data with session_id, coordinates, timestamps, and actions.
    """
    file_path = os.path.join(base_path, 'data', 'mouse_movements', data_subset_folder, session_id, 'mouse_movements.json')
    
    try:
        with open(file_path, 'r') as f:
            text_data = f.read()

            # Fix malformed JSON
            if '}"' in text_data:
                text_data = text_data.replace('}"', '},"')

            data = json.loads(text_data)

        # === Coordinates ===
        coords_str = data.get('mousemove_total_behaviour', '').strip()

        # Fix format: replace curly braces with square brackets
        if coords_str.startswith('{') and coords_str.endswith('}'):
            coords_str = coords_str.replace('{', '[').replace('}', ']')

        try:
            coords = ast.literal_eval(coords_str)
            coords = [
                tuple(map(int, c))
                for c in coords
                if isinstance(c, (list, tuple)) and len(c) == 2
            ]
        except (ValueError, SyntaxError, TypeError):
            coords = []

        # === Timestamps ===
        times_str = data.get('mousemove_times', '')
        times_str = re.sub(r'[{}()\[\]]', '', times_str)
        timestamps = [int(t.strip()) for t in times_str.split(',') if t.strip().isdigit()]

        # === Actions ===
        actions_str = data.get('total_behaviour', '')
        actions = re.findall(r'c\(\w\)|m\(\d+,\d+\)', actions_str)

        return {
            'session_id': session_id,
            'coordinates': coords,
            'timestamps': timestamps,
            'actions': actions
        }

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not parse file for session {session_id}. Error: {e}")
        return None

# === Try the function ===
first_session_id = train_df_labels['session_id'].iloc[0]

parsed_data = parse_mouse_data_from_file(
    session_id=first_session_id,
    data_subset_folder='humans_and_advanced_bots',  # or 'humans_and_moderate_bots'
    base_path=base_path
)

if parsed_data:
    print(f"\nSuccessfully Parsed Session: {parsed_data['session_id']}")
    print(f"First Coordinate: {parsed_data['coordinates'][:1]}")
    print(f"First Timestamp: {parsed_data['timestamps'][:1]}")
    print(f"First Action: {parsed_data['actions'][:1]}")
else:
    print("Failed to parse session.")


print("\n--- Feature Engineering ---")


import numpy as np

def create_feature_vector(session_id: str, parsed_data: dict):
    """Calculates a vector of features from the parsed data of a single session."""
    
    features = {'session_id': session_id}
    
    if parsed_data:
        coords = parsed_data['coordinates']
        times = parsed_data['timestamps']
        actions = parsed_data['actions']

        
        features['total_events'] = len(actions)
        features['mouse_distance'] = 0
        if len(coords) > 1:
            # Calculating total distance traveled by the mouse
            total_dist = 0
            for i in range(1, len(coords)):
                x1, y1 = coords[i-1]
                x2, y2 = coords[i]
                total_dist += np.sqrt((x2 - x1)**2 + (y2 - y1)**2)# euclidean distance
            features['mouse_distance'] = total_dist
        
        # Time-based features
        features['session_duration_ms'] = 0
        features['avg_velocity'] = 0
        if len(times) > 1:
            duration_ms = times[-1] - times[0]
            features['session_duration_ms'] = duration_ms
            # Velocity calculation
            if duration_ms > 0:
                features['avg_velocity'] = features['mouse_distance'] / (duration_ms / 1000.0) # pixels/sec
        
        # Action-based features
        features['click_count'] = sum(1 for action in actions if action.startswith('c'))

    else:
        # If no data was parsed, fill features with 0
        features['total_events'] = 0
        features['mouse_distance'] = 0
        features['session_duration_ms'] = 0
        features['avg_velocity'] = 0
        features['click_count'] = 0
        
    return features

#
print("\n--- Starting feature engineering for all training sessions... ---")

training_features_list = []
# Loop over each session ID in the training labels DataFrame
for session_id in train_df_labels['session_id']:
    
    parsed_data = parse_mouse_data_from_file(
        session_id=session_id,
        data_subset_folder='humans_and_advanced_bots',
        base_path=base_path
    )
    
    
    session_features = create_feature_vector(session_id, parsed_data)
    training_features_list.append(session_features)


features_df = pd.DataFrame(training_features_list)
# pd.set_option('display.max_columns', None)  

print("\n--- Feature Engineering Complete! ---")
print("Here are the first 5 rows of your new feature DataFrame:")
print(features_df.head())



#====Saving=====
base_path = r'd:\AF\ad_fraud\MachineLearning'
output_dir = os.path.join(base_path, 'ProcessedPhase1')
os.makedirs(output_dir, exist_ok=True)

# Save training features
train_features_path = os.path.join(output_dir, 'train_features.csv')
features_df.to_csv(train_features_path, index=False)
print(f"\nTraining features saved to: {train_features_path}")

# Also save labels for model training later
train_labels_path = os.path.join(output_dir, 'train_labels.csv')
train_df_labels.to_csv(train_labels_path, index=False)
print(f"Training labels saved to: {train_labels_path}")

