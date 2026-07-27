import streamlit as st
import requests

# ---------------------------------------------------------
# Streamlit Page Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Camping Planner AI",
    page_icon="🏕️",
    layout="centered",
)

st.title("🏕️ Camping Planner AI")
st.write("Plan your perfect outdoor adventure with AI-powered trip guidance.")

# ---------------------------------------------------------
# Sidebar Inputs
# ---------------------------------------------------------
st.sidebar.header("Trip Settings")

location = st.sidebar.text_input("📍 Location")
origin = st.sidebar.text_input("🚗 Origin")
num_people = st.sidebar.number_input("👥 Number of People", min_value=1, step=1)
num_days = st.sidebar.number_input("📅 Number of Days", min_value=1, step=1)
camp_style = st.sidebar.selectbox("⛺ Camping Style", ["tent", "rv", "cabin", "backpacking"])
season = st.sidebar.text_input("🌤️ Season or Month")
experience_level = st.sidebar.selectbox("🎒 Experience Level", ["beginner", "intermediate", "advanced"])

# ---------------------------------------------------------
# IMPORTANT: Replace this with YOUR forwarded Codespaces URL
# ---------------------------------------------------------
API_URL = "https://friendly-succotash-wrq7r5pp7rpw35w5p-8000.app.github.dev/plan"

# ---------------------------------------------------------
# Generate Button
# ---------------------------------------------------------
if st.button("Generate Camping Plan"):
    payload = {
        "location": location,
        "origin": origin,
        "num_people": num_people,
        "num_days": num_days,
        "camp_style": camp_style,
        "season": season,
        "experience_level": experience_level
    }

    with st.spinner("Generating your camping plan..."):
        try:
            response = requests.post(API_URL, json=payload)
        except Exception as e:
            st.error("Could not reach the FastAPI server.")
            st.write(e)
            st.stop()

    # ---------------------------------------------------------
    # Response Handling
    # ---------------------------------------------------------
    if response.status_code == 200:
        st.success("Your camping plan is ready!")
        st.json(response.json())
    else:
        st.error("Something went wrong.")
        st.write("Server response:")
        st.write(response.text)
