# ml_pipeline/src/feature_engineering.py
import numpy as np
import pandas as pd
import re

def get_mouse_features(session_data):
    """
    Calculates behavioral features from raw mouse tracking data for a single session.
    """
    # --- THIS IS THE CORRECTED LINE ---
    # Use 'mousemove_total_behaviour' to match your JSON files
    coords_str = re.findall(r'm\(\d+,\d+\)', session_data['mousemove_total_behaviour'])

    if len(coords_str) < 5:
        return None 

    coords = [tuple(map(int, re.findall(r'\d+', s))) for s in coords_str]
    times = np.array([int(t) for t in session_data['mousemove_times'].split(',') if t])

    min_len = min(len(coords), len(times))
    if min_len < 5:
        return None
    coords, times = coords[:min_len], times[:min_len]

    df = pd.DataFrame(coords, columns=['x', 'y'])
    df['time'] = times
    df['time_diff'] = df['time'].diff().fillna(0)
    df['dist_diff'] = np.sqrt(df['x'].diff().pow(2) + df['y'].diff().pow(2)).fillna(0)

    df.loc[df.time_diff == 0, 'time_diff'] = 0.001

    velocities = (df['dist_diff'] / df['time_diff']).fillna(0)
    accelerations = (velocities.diff() / df['time_diff']).fillna(0)

    total_duration = df['time'].iloc[-1] - df['time'].iloc[0]

    features = {
        'avg_velocity': velocities.mean(),
        'std_velocity': velocities.std(),
        'max_velocity': velocities.max(),
        'avg_abs_acceleration': accelerations.abs().mean(),
        'total_distance': df['dist_diff'].sum(),
        'num_clicks': session_data['mousemove_total_behaviour'].count('cl('),
        'num_movements': len(coords),
        'duration_seconds': total_duration / 1000, # Timestamps appear to be in milliseconds
    }
    return features