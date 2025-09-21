from flask import Flask, request, jsonify
from langgraph_workflow import build_langgraph_workflow
from gemini_utils import generate_seed_itinerary, get_enriched_attractions
from firebase_init import db
from datetime import datetime

app = Flask(__name__)
graph = build_langgraph_workflow()


@app.route("/")
def home():
    return "AI Travel Agent is live!"


@app.route("/generate_itinerary", methods=["POST"])
def generate_itinerary():
    data = request.json
    preferences = {
        "destination": data.get("destination"),
        "duration": int(data.get("duration", 3)),
        "month": data.get("month", "December"),
        "travel_style": data.get("travel_style", "Relaxation"),
        "group_type": data.get("group_type", "Couple"),
        "comments": data.get("comments", "")
    }

    # seed = generate_seed_itinerary(preferences)
    seed = get_enriched_attractions(preferences)
    state = {
        "preferences": preferences,
        "preferences_text": "\n".join([f"{k}: {v}" for k, v in preferences.items()]),
        "itinerary": seed,
        "activity_suggestions": "",
        "useful_links": [],
        "weather_forecast": "",
        "packing_list": "",
        "food_culture_info": "",
        "chat_history": [],
        "user_question": "",
        "chat_response": ""
    }

    result = graph.invoke(state)
    # db.collection("trip_logs").add({
    #     "timestamp": datetime.utcnow().isoformat(),
    #     "preferences": preferences,
    #     "itinerary": result.get("itinerary", "")
    # })

    # Filter out empty fields before storing
    doc = {
        "timestamp": datetime.utcnow().isoformat()
    }
    for key, value in result.items():
        if value not in ("", [], {}, None):
            doc[key] = value

    db.collection("trip_logs").add(doc)


    return jsonify(result)