import streamlit as st
import requests
from datetime import date

import requests

st.title("🧳 AI Travel Planner")

with st.form("trip_form"):
    destination = st.text_input("Destination")
    comments = st.text_area("Preferences")
    from_date = st.date_input("Start Date", value=date.today())
    to_date = st.date_input("End Date", value=date.today())
    travel_style = st.selectbox("Travel Style", ["Relaxation", "Adventure", "Cultural"])
    group_type = st.selectbox("Group Type", ["Solo", "Couple", "Family"])
    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    duration = (to_date - from_date).days or 1
    payload = {
        "destination": destination,
        "duration": duration,
        "month": from_date.strftime("%B"),
        "comments": comments,
        "travel_style": travel_style,
        "group_type": group_type
    }
    

    try:

        response = requests.post("http://localhost:5000/generate_itinerary", json=payload)
        # result = response.json()
            
        if response.status_code == 200:
            result = response.json()
            st.markdown(result.get("itinerary", "No itinerary generated."))
        else:
            st.error(f"Error from server: {response.status_code} - {response.text}")
            result = None
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        result = None