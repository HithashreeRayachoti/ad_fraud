from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import joblib
import pandas as pd
import numpy as np

# ---- Configuration ----
MODEL_PATH = os.path.join('..', 'MachineLearning', 'savedModels', 'xgboost_classifier.joblib')
LOG_FILE = "click_logs.json"

# ---- Load ML Model ----
try:
    model = joblib.load(MODEL_PATH)
    print("ML Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    model = None

# ---- Feature list and label mapping ----
MODEL_FEATURES = ['total_events', 'mouse_distance', 'session_duration_ms', 'avg_velocity', 'click_count']
LABEL_MAPPING = {0: 'Bot', 1: 'Human'}

# ---- Feature engineering ----
def create_feature_vector(session_data: dict):
    features = {'session_id': session_data.get("session_id")}
    
    coords = session_data.get('mousemove_total_behaviour', [])
    times = session_data.get('mousemove_times', [])
    actions = session_data.get('total_behaviour', [])

    features['total_events'] = len(actions)
    
    # Mouse distance
    features['mouse_distance'] = 0
    if len(coords) > 1:
        total_dist = sum(
            np.sqrt((coords[i]['x'] - coords[i - 1]['x']) ** 2 + (coords[i]['y'] - coords[i - 1]['y']) ** 2)
            for i in range(1, len(coords))
        )
        features['mouse_distance'] = total_dist
    
    # Duration & velocity
    features['session_duration_ms'] = 0
    features['avg_velocity'] = 0
    if len(times) > 1:
        duration_ms = times[-1] - times[0]
        features['session_duration_ms'] = duration_ms
        if duration_ms > 0:
            features['avg_velocity'] = features['mouse_distance'] / (duration_ms / 1000.0)
    
    # Click count
    features['click_count'] = sum(1 for action in actions if action.startswith('c'))
        
    return features

# ---- Flask App ----
app = Flask(__name__)
CORS(app)

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def home():
    return "Click fraud tracker backend is running at http://localhost:5000"

# ---- Log Visit Endpoint ----
@app.route('/log-visit', methods=['POST'])
def log_visit():
    if not model:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500

    session_data = request.get_json()

    # --- Feature Engineering ---
    feature_dict = create_feature_vector(session_data)
    features_df = pd.DataFrame([feature_dict])[MODEL_FEATURES]

    # --- Idle Session Detection ---
    is_idle = (
        feature_dict["total_events"] == 0 and
        feature_dict["mouse_distance"] == 0 and
        feature_dict["click_count"] == 0
    )

    # --- Prediction Logic ---
    if is_idle:
        prediction_label = "Human"
        log_reason = "Idle override (no interaction)"
        print(f"Session {session_data.get('session_id')} classified as: Human (idle override)")
    else:
        prediction_numeric = model.predict(features_df)
        prediction_label = LABEL_MAPPING.get(prediction_numeric[0], 'Unknown')
        log_reason = "Predicted via model"
        print(f"Session {session_data.get('session_id')} classified as: {prediction_label}")

    # --- Log Entry ---
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ip": request.remote_addr,
        "userAgent": request.headers.get("User-Agent"),
        "session_id": session_data.get("session_id"),
        "prediction": prediction_label,
        "log_reason": log_reason,
        "details": session_data
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

# ---- Serve Filtered Dashboard Logs ----
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

# ✅ Serve full raw JSON for direct use in dashboard.jsx
@app.route('/click_logs.json')
def serve_click_logs():
    return send_from_directory(os.path.dirname(__file__), 'click_logs.json', mimetype='application/json')

# ---- Run the app ----
if __name__ == '__main__':
    print("Backend is running. Listening at: http://localhost:5000")
    app.run(debug=True, port=5000)
