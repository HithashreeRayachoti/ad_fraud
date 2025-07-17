from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

LOG_FILE = "click_logs.json"

# Ensure the log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def home():
    return "Click fraud tracker backend is running. Listening at http://localhost:5000"

@app.route('/log-visit', methods=['POST'])
def log_visit():
    data = request.get_json()

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ip": request.remote_addr,
        "userAgent": request.headers.get("User-Agent"),
        "session_id": data.get("session_id"),
        "total_behaviour": data.get("total_behaviour", []),
        "mousemove_times": data.get("mousemove_times", []),
        "mousemove_total_behaviour": data.get("mousemove_total_behaviour", []),
        "Mousemove_visited_urls": data.get("Mousemove_visited_urls", 0)  # ✅ New field
    }

    print(f"[{log_entry['timestamp']}] Session: {log_entry['session_id']} from {log_entry['ip']}")
    print(f"  UA: {log_entry['userAgent']}")
    print(f"  Mouse movements: {len(log_entry['mousemove_total_behaviour'])} points")
    print(f"  Behaviour entries: {len(log_entry['total_behaviour'])}")
    print(f"  Unique hovered URLs: {log_entry['Mousemove_visited_urls']}")

    # Save to file
    with open(LOG_FILE, 'r+') as f:
        logs = json.load(f)
        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, indent=2)

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("✅ Backend is running. Listening at: http://localhost:5000")
    app.run(debug=True, port=5000)
