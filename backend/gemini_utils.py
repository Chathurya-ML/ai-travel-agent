
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import requests
import ast
import json
import re
import os
from dotenv import load_dotenv


# 🔧 Initialize Gemini
vertexai.init(project="aitravelagent-472709", location="us-central1")
model = GenerativeModel("gemini-2.5-flash")

load_dotenv()


GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# 🧠 Generate structured itinerary using Gemini
def generate_seed_itinerary(preferences):
    prompt = (
        f"You're a travel planner. For the given user destination {preferences['destination']}, "
        "generate a list of key places to visit as a Python-style dictionary.\n"
        "Each key should be the name of the place.\n"
        "Each value should be another dictionary with:\n"
        "- open_time (in 12-hour format with AM/PM)\n"
        "- close_time (in 12-hour format with AM/PM)\n"
        "- estimated visit_duration (e.g. '2 hrs')\n"
        "- description (brief)\n"
        "- category (e.g. museum, park, historical site)\n"
        "If the place is open 24 hours, set open_time to '12:00 AM' and close_time to '11:59 PM'."
        "I strictly dont want any inline comments in the output.\n"
        "No additional text, just the dictionary."
    )
    return model.generate_content(prompt).text

# 🧩 Parse Gemini's Python-style dictionary output
def parse_itinerary_seed(seed_text):
    if seed_text.startswith("python"):
        seed_text = seed_text.split("python", 1)[-1].strip()
    if "=" in seed_text:
            seed_text = seed_text.split("=", 1)[-1].strip()
    print("Seed text before parsing:", seed_text)
    seed_text = re.sub(r"#.*", "", seed_text)
    seed_text = re.sub(r",\s*([}\]])", r"\1", seed_text)
    seed_text = seed_text.replace("'''", "").replace('"""', "")
    try:
        parsed_dict = ast.literal_eval(seed_text)
    except Exception as e:
        print("Parsing error:", e)
        parsed_dict = {}
    return parsed_dict

# 📍 Build full pairwise distance matrix from Gemini-generated attractions
def build_distance_matrix(attraction_names):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    matrix = {}

    for origin in attraction_names:
        params = {
            "origins": origin,
            "destinations": "|".join(attraction_names),
            "key": GOOGLE_MAPS_API_KEY
        }
        response = requests.get(url, params=params)
        elements = response.json().get("rows", [])[0].get("elements", [])

        matrix[origin] = {}
        for i, element in enumerate(elements):
            if element.get("status") == "OK":
                matrix[origin][attraction_names[i]] = {
                    "distance_text": element["distance"]["text"],
                    "distance_value": element["distance"]["value"],
                    "duration_text": element["duration"]["text"],
                    "duration_value": element["duration"]["value"]
                }
            else:
                matrix[origin][attraction_names[i]] = None
    return matrix

# 🖨️ Format parsed itinerary for readable output
def format_itinerary(parsed_dict):
    return json.dumps(parsed_dict, indent=2, ensure_ascii=False)

# 🔗 Main enrichment function
def get_enriched_attractions(preferences):
    itinerary_text = generate_seed_itinerary(preferences)
    print("Raw itinerary text:", itinerary_text)
    parsed_places = parse_itinerary_seed(itinerary_text)
    print(parsed_places)
    attraction_names = list(parsed_places.keys())
    
    distance_matrix = build_distance_matrix(attraction_names)

    metadata = {
        "attractions": [{"name": name} for name in attraction_names],
        "itinerary_seed": parsed_places,
        "distances": distance_matrix
    }

    prompt = (
        f"""
        You're an expert travel planner. Based on the following attractions and their {metadata} , generate a 1-day itinerary that:

        - Minimizes total travel distance between places
        - Ensures each place is visited within its open hours
        - Includes estimated visit durations
        - Starts at 9:00 AM and ends by 6:00 PM
        - Includes travel time between stops
        - Prioritizes places based on the user's preferences: {preferences['comments']}
        - Ignore any distances where the origin and destination are the same (e.g., 'British Museum' to 'British Museum'). Only consider travel between different places.
        - Prioritize routes with the shortest duration_text values when sequencing visits.
        - Respect each place’s open and close times, and ensure the visit duration fits within that window.
        - manage to cover all these places according to given number of days, if the days are less, cut down on some less priority places, if days are more try to add shopping and more such activities.preferences.preferences.
        
        Your tone of writing should be friendly and engaging, as if you're personally guiding the user through their day.
        """
    )
    return model.generate_content(prompt).text