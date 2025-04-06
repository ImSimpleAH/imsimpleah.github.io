from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # 🔓 Allow cross-origin access (GitHub Pages needs this)

# File to store events
events_file = 'events.json'

# Make sure the events file exists
if not os.path.exists(events_file):
    with open(events_file, 'w') as f:
        json.dump([], f)

@app.route('/')
def home():
    return '28th CAD Events API is running!'


# GET /events → Return all saved events
@app.route('/events', methods=['GET'])
def get_events():
    with open(events_file, 'r') as f:
        events = json.load(f)
    return jsonify(events)

# POST /events → Add a new event
@app.route('/events', methods=['POST'])
def add_event():
    data = request.json
    with open(events_file, 'r+') as f:
        events = json.load(f)
        events.append(data)
        f.seek(0)
        json.dump(events, f, indent=2)
    return jsonify({"message": "Event added"}), 201

# ✅ IMPORTANT: Bind to 0.0.0.0 and use PORT from Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render provides PORT env var
    app.run(host='0.0.0.0', port=port)
