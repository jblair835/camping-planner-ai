import streamlit as st
import requests

st.title("Camping Planner AI")

location = st.text_input("Location")
origin = st.text_input("Origin")
num_people = st.number_input("Number of People", min_value=1, step=1)
num_days = st.number_input("Number of Days", min_value=1, step=1)
camp_style = st.selectbox("Camping Style", ["tent", "rv", "cabin", "backpacking"])
season = st.text_input("Season or Month")
experience_level = st.selectbox("Experience Level", ["beginner", "intermediate", "advanced"])

API_URL = "https://friendly-succotash-wrq7r5pp7rpw35w5p-8000.app.github.dev/plan"

if st.button("Generate Plan"):
    payload = {
        "location": location,
        "origin": origin,
        "num_people": num_people,
        "num_days": num_days,
        "camp_style": camp_style,
        "season": season,
        "experience_level": experience_level
    }

    try:
        response = requests.post(API_URL, json=payload)
    except Exception as e:
        st.error("Could not reach FastAPI.")
        st.write(e)
        st.stop()

    if response.status_code == 200:
        st.success("Camping Plan Generated!")
        st.json(response.json())
    else:
        st.error("Error from server:")
        st.write(response.text)
