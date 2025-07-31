from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import joblib
import pandas as pd
import numpy as np
import re


MODEL_PATHS = MODEL_PATH = os.path.join('..', 'MachineLearning', 'savedModels', 'xgboost_classifier.joblib')
LOG_FILE = "click_logs.json"
try:
    model = joblib.load(MODEL_PATH)
    print("✅ ML Model loaded successfully.")
except FileNotFoundError:
    print(f"❌ Error: Model file not found at {MODEL_PATH}")
    model = None

# Define the exact feature names in the order the model was trained on
MODEL_FEATURES = ['total_events', 'mouse_distance', 'session_duration_ms', 'avg_velocity', 'click_count']
# Define the mapping from prediction number to label (0=human, 1=bot)
LABEL_MAPPING = {0: 'Bot', 1: 'Human'}

#Feature engineering function
def create_feature_vector(session_data: dict):
    """Calculates a feature vector from the raw session data."""
    features = {'session_id': session_data.get("session_id")}
    
    # The real-time data from your tracker is already in a clean list format
    coords = session_data.get('mousemove_total_behaviour', [])
    times = session_data.get('mousemove_times', [])
    actions = session_data.get('total_behaviour', [])

    features['total_events'] = len(actions)
    features['mouse_distance'] = 0
    if len(coords) > 1:
        total_dist = 0
        for i in range(1, len(coords)):
            x1, y1 = coords[i-1]['x'], coords[i-1]['y']
            x2, y2 = coords[i]['x'], coords[i]['y']
            total_dist += np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        features['mouse_distance'] = total_dist
    
    features['session_duration_ms'] = 0
    features['avg_velocity'] = 0
    if len(times) > 1:
        duration_ms = times[-1] - times[0]
        features['session_duration_ms'] = duration_ms
        if duration_ms > 0:
            features['avg_velocity'] = features.get('mouse_distance', 0) / (duration_ms / 1000.0)
    
    features['click_count'] = sum(1 for action in actions if action.startswith('c'))
        
    return features

#Main Flask app

app = Flask(__name__)
CORS(app)

# Ensure the log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def home():
    return "Click fraud tracker backend is running. Listening at http://localhost:5000"

# @app.route('/log-visit', methods=['POST'])
# def log_visit():
#     data = request.get_json()

#     log_entry = {
#         "timestamp": datetime.now().isoformat(),
#         "ip": request.remote_addr,
#         "userAgent": request.headers.get("User-Agent"),
#         "session_id": data.get("session_id"),
#         "total_behaviour": data.get("total_behaviour", []),
#         "mousemove_times": data.get("mousemove_times", []),
#         "mousemove_total_behaviour": data.get("mousemove_total_behaviour", []),
#         "Mousemove_visited_urls": data.get("Mousemove_visited_urls", 0)  # ✅ New field
#     }

#     print(f"[{log_entry['timestamp']}] Session: {log_entry['session_id']} from {log_entry['ip']}")
#     print(f"  UA: {log_entry['userAgent']}")
#     print(f"  Mouse movements: {len(log_entry['mousemove_total_behaviour'])} points")
#     print(f"  Behaviour entries: {len(log_entry['total_behaviour'])}")
#     print(f"  Unique hovered URLs: {log_entry['Mousemove_visited_urls']}")

#     # Save to file
#     with open(LOG_FILE, 'r+') as f:
#         logs = json.load(f)
#         logs.append(log_entry)
#         f.seek(0)
#         json.dump(logs, f, indent=2)

#     return jsonify({"status": "ok"})

@app.route('/log-visit', methods=['POST'])
def log_visit():
    if not model:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500

    # --- Receive Data ---
    session_data = request.get_json()

    # --- Engineer Features ---
    feature_dict = create_feature_vector(session_data)
    features_for_prediction = pd.DataFrame([feature_dict])[MODEL_FEATURES]

    # --- Make Prediction ---
    prediction_numeric = model.predict(features_for_prediction)
    prediction_label = LABEL_MAPPING.get(prediction_numeric[0], 'Unknown')
    
    print(f"Session {session_data.get('session_id')} classified as: {prediction_label}")

    # --- Log the Enriched Data ---
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ip": request.remote_addr,
        "userAgent": request.headers.get("User-Agent"),
        "session_id": session_data.get("session_id"),
        "prediction": prediction_label,  # Add the prediction to the log
        "details": session_data # Store the raw interaction data
    }
    
    try:
        with open(LOG_FILE, 'r+') as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Error writing to log file: {e}")
        return jsonify({"status": "error", "message": "Failed to write log"}), 500

    return jsonify({"status": "ok", "prediction": prediction_label})

# if __name__ == '__main__':
#     print(" Backend is running. Listening at: http://localhost:5000")
#     app.run(debug=True, port=5000)

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
        
        dashboard_data = [
            {
                "session_id": log.get("session_id"),
                "timestamp": log.get("timestamp"),
                "prediction": log.get("prediction")
            }
            for log in logs
        ]
        
        return jsonify(sorted(dashboard_data, key=lambda x: x['timestamp'], reverse=True))

    except Exception as e:
        print(f"Error reading log file: {e}")
        return jsonify({"status": "error", "message": "Could not retrieve logs"}), 500


if __name__ == '__main__':
    print("✅ Backend is running. Listening at: http://localhost:5000")
    app.run(debug=True, port=5000)