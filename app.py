from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
STORAGE_FILE = "match_data.json"

def store_data(data):
    if not os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "w") as f:
            json.dump([], f)

    with open(STORAGE_FILE, "r+") as f:
        try:
            matches = json.load(f)
        except:
            matches = []

        matches.append(data)
        f.seek(0)
        json.dump(matches, f, indent=2)
        f.truncate()

@app.route("/")
def index():
    return "✅ Model X API is running."

@app.route("/receive", methods=["POST"])
def receive():
    try:
        match = request.get_json()

        filtered = {
            "crawler_id": match.get("crawler_id"),
            "match_id": match.get("match_id"),
            "team": match.get("team"),
            "A": match.get("A"),
            "B": match.get("B"),
            "C": match.get("C"),
            "local_time": match.get("local_time"),
            "result": match.get("result", None),
            "timestamp": datetime.utcnow().isoformat()
        }

        store_data(filtered)
        return jsonify({"status": "✅ Stored", "match_id": filtered["match_id"]}), 200

    except Exception as e:
        return jsonify({"status": "❌ Error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
