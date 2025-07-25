import os
import pandas as pd
import numpy as np
import json
import re

# === Paths ===
base_path = r'd:\AF\ad_fraud\MachineLearning\phase1'
annotations_path = os.path.join(base_path, 'annotations/humans_and_advanced_bots')
test_df_labels = pd.read_csv(os.path.join(annotations_path, 'test'), sep=' ', names=['session_id', 'label'])

# === Parsing Function ===
def parse_mouse_data_from_file(session_id: str, data_subset_folder: str, base_path: str):
    file_path = os.path.join(base_path, 'data', 'mouse_movements', data_subset_folder, session_id, 'mouse_movements.json')

    try:
        with open(file_path, 'r') as f:
            text_data = f.read()
            text_data = text_data.replace('}"', '},"')
        data = json.loads(text_data)

        coords_str = data.get('mousemove_total_behaviour', '').strip()
        coord_pairs = re.findall(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', coords_str)
        coords = [(int(x), int(y)) for x, y in coord_pairs]

        times_str = data.get('mousemove_times', '').strip('{}()[] \n')
        times = [int(t) for t in times_str.split(',') if t.strip().isdigit()]

        actions_str = data.get('total_behaviour', '')
        actions = re.findall(r'c\(\w\)|m\(\d+,\d+\)', actions_str)

        return {
            'session_id': session_id,
            'coordinates': coords,
            'timestamps': times,
            'actions': actions
        }

    except Exception as e:
        print(f"Error in session {session_id}: {e}")
        return None

# === Feature Engineering Function ===
def create_feature_vector(session_id: str, parsed_data: dict):
    features = {'session_id': session_id}
    if parsed_data:
        coords = parsed_data['coordinates']
        times = parsed_data['timestamps']
        actions = parsed_data['actions']

        features['total_events'] = len(actions)
        features['mouse_distance'] = sum(
            np.sqrt((coords[i][0] - coords[i-1][0]) ** 2 + (coords[i][1] - coords[i-1][1]) ** 2)
            for i in range(1, len(coords))
        ) if len(coords) > 1 else 0

        if len(times) > 1:
            duration_ms = times[-1] - times[0]
            features['session_duration_ms'] = duration_ms
            features['avg_velocity'] = features['mouse_distance'] / (duration_ms / 1000.0) if duration_ms > 0 else 0
        else:
            features['session_duration_ms'] = 0
            features['avg_velocity'] = 0

        features['click_count'] = sum(1 for action in actions if action.startswith('c'))
    else:
        features.update({
            'total_events': 0,
            'mouse_distance': 0,
            'session_duration_ms': 0,
            'avg_velocity': 0,
            'click_count': 0,
        })

    return features

# === Process All Test Sessions ===
print("Extracting features for test set...")
test_features_list = []
for session_id in test_df_labels['session_id']:
    parsed = parse_mouse_data_from_file(session_id, 'humans_and_advanced_bots', base_path)
    feats = create_feature_vector(session_id, parsed)
    test_features_list.append(feats)

test_features_df = pd.DataFrame(test_features_list)

# === Save Features & Labels ===
output_dir = os.path.join(base_path, '..', 'ProcessedPhase1')
os.makedirs(output_dir, exist_ok=True)

test_features_df.to_csv(os.path.join(output_dir, 'test_features.csv'), index=False)
test_df_labels.to_csv(os.path.join(output_dir, 'test_labels.csv'), index=False)

print("Test data parsed and saved successfully.")
