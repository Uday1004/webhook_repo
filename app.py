# app.py
from flask import Flask, request, jsonify
from db import events_collection
from events_handler import parse_event

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    data = request.json

    parsed = parse_event(event_type, data)
    if parsed:
        events_collection.insert_one(parsed)
        return jsonify({"status": "saved"}), 200
    else:
        return jsonify({"status": "ignored"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    events = list(events_collection.find({}, {"_id": 0}))
    return jsonify(events), 200

if __name__ == "__main__":
    app.run(port=5000)
