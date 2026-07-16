import os
import streamlit as st
from crewai import Agent, Task, Crew

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(page_title="Camping Planner AI", layout="wide")

# ============================================================
# SEQUOIA BACKGROUND + RUSTIC THEME
# ============================================================

st.markdown("""
<style>

    /* Full-page faded background image */
    .main, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #F4EFE6 !important;
        background-image: url('/attachments/gTbAQpmh7niZLBDeCMkQy.png') !important;
        background-size: cover !important;
        background-attachment: fixed !important;
        background-position: center !important;
        opacity: 0.25 !important;
    }

    /* Transparent overlay so background shows through */
    [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"] {
        background: transparent !important;
    }

    .pine-top {
        background-image: url('/attachments/gTbAQpmh7niZLBDeCMkQy.png');
        background-size: cover;
        background-position: top;
        height: 140px;
        opacity: 0.35;
        border-bottom: 4px solid #C97B3A;
    }

    .rustic-header {
        background-image: url('/attachments/gTbAQpmh7niZLBDeCMkQy.png');
        background-size: cover;
        background-position: center;
        padding: 4rem 1rem;
        border-bottom: 6px solid #C97B3A;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        opacity: 0.45;
    }

    .rustic-header::after {
        content: "";
        display: block;
        height: 90px;
        background: radial-gradient(circle at center, rgba(201,123,58,0.45), rgba(0,0,0,0));
        margin-top: -40px;
    }

    .stButton>button {
        background-color: #C97B3A;
        color: #F4EFE6;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        border: none;
        font-family: serif;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .stButton>button:hover {
        background-color: #A8642F;
        color: white;
    }

    .rustic-card {
        background-color: rgba(227, 220, 207, 0.85);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
        border-left: 6px solid #C97B3A;
        margin-bottom: 1.5rem;
    }

    h2 {
        color: #C97B3A !important;
        font-family: serif !important;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="pine-top"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="rustic-header">
    <h1 style="text-align:center; color:#F4EFE6; font-family:serif; font-size:3rem;">
        🏕️ Camping Planner AI
    </h1>
    <p style="text-align:center; color:#F4EFE6; font-size:1.2rem; font-family:serif;">
        Plan your perfect outdoor adventure under the towering Sequoias
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CREWAI CONFIG
# ============================================================

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["OTEL_SDK_DISABLED"] = "true"

# Agents (CrewAI 1.15.2 requires llm string names)
planner_agent = Agent(
    role="Camping Planner",
    goal="Create detailed camping trip plans",
    backstory="You are an expert outdoor guide with decades of wilderness experience.",
    llm="groq/llama-3.1-8b-instant"
)

packing_agent = Agent(
    role="Packing Expert",
    goal="Create packing lists based on season and experience",
    backstory="You specialize in wilderness gear and survival essentials.",
    llm="groq/llama-3.1-8b-instant"
)

weather_agent = Agent(
    role="Weather Forecaster",
    goal="Provide weather forecasts for camping trips",
    backstory="You analyze weather patterns for outdoor safety.",
    llm="groq/llama-3.1-8b-instant"
)

gear_agent = Agent(
    role="Gear Specialist",
    goal="Recommend camping gear",
    backstory="You know every piece of gear needed for any terrain.",
    llm="groq/llama-3.1-8b-instant"
)

# ============================================================
# TASK FUNCTIONS
# ============================================================

def run_planner(season, experience, location):
    task = Task(
        description=f"Create a camping plan for a {experience} camper in {season}. Region: {location}.",
        expected_output="A detailed daily itinerary including campsite recommendations and safety notes.",
        agent=planner_agent
    )
    crew = Crew(tasks=[task], agents=[planner_agent])
    return crew.kickoff().raw

def run_packing_list(season, experience):
    task = Task(
        description=f"Create a packing list for a {experience} camper in {season}.",
        expected_output="A categorized checklist of clothing, survival gear, food, and essentials.",
        agent=packing_agent
    )
    crew = Crew(tasks=[task], agents=[packing_agent])
    return crew.kickoff().raw

def run_weather(season, location):
    task = Task(
        description=f"Provide a weather forecast for camping in {season} in {location}.",
        expected_output="A summary of temperatures, rain likelihood, and climate warnings.",
        agent=weather_agent
    )
    crew = Crew(tasks=[task], agents=[weather_agent])
    return crew.kickoff().raw

def run_gear(season, experience):
    task = Task(
        description=f"Recommend camping gear for a {experience} camper in {season}.",
        expected_output="A bulleted list of essential gear brands, types, and tools.",
        agent=gear_agent
    )
    crew = Crew(tasks=[task], agents=[gear_agent])
    return crew.kickoff().raw

# ============================================================
# SESSION STATE
# ============================================================

for key in ["plan", "packing", "weather", "gear"]:
    if f"result_{key}" not in st.session_state:
        st.session_state[f"result_{key}"] = None

# ============================================================
# MAIN TABS
# ============================================================

st.markdown("## 🌲 Your Camping Dashboard")

tab_plan, tab_packing, tab_weather, tab_gear = st.tabs(
    ["🧭 Trip Plan", "🎒 Packing List", "🌦️ Weather", "🪵 Gear"]
)

# ============================================================
# TAB 1 — TRIP PLAN (inputs moved here)
# ============================================================

with tab_plan:
    st.markdown('<div class="rustic-card">', unsafe_allow_html=True)

    st.subheader("🌿 Trip Settings")

    season = st.selectbox("Season or month", [
        "Spring", "March", "April", "May",
        "Summer", "June", "July", "August",
        "Fall", "September", "October", "November",
        "Winter", "December", "January", "February"
    ])

    experience = st.selectbox("Experience level", ["Beginner", "Intermediate", "Advanced"])
    location = st.text_input("Preferred region (optional)")

    if st.button("Generate Trip Plan"):
        with st.spinner("Creating your custom camping plan..."):
            st.session_state.result_plan = run_planner(season, experience, location)
        st.success("Camping plan generated!")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.result_plan:
        st.markdown('<div class="rustic-card">', unsafe_allow_html=True)
        st.write(st.session_state.result_plan)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 2 — PACKING LIST
# ============================================================

with tab_packing:
    st.markdown('<div class="rustic-card">', unsafe_allow_html=True)

    if st.button("Generate Packing List"):
        with st.spinner("Building your packing list..."):
            st.session_state.result_packing = run_packing_list(season, experience)
        st.success("Packing list generated!")

    if st.session_state.result_packing:
        st.write(st.session_state.result_packing)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 3 — WEATHER
# ============================================================

with tab_weather:
    st.markdown('<div class="rustic-card">', unsafe_allow_html=True)

    if st.button("Get Weather Forecast"):
        with st.spinner("Fetching weather forecast..."):
            st.session_state.result_weather = run_weather(season, location)
        st.success("Weather forecast generated!")

    if st.session_state.result_weather:
        st.write(st.session_state.result_weather)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 4 — GEAR
# ============================================================

with tab_gear:
    st.markdown('<div class="rustic-card">', unsafe_allow_html=True)

    if st.button("Generate Gear Recommendations"):
        with st.spinner("Gathering gear recommendations..."):
            st.session_state.result_gear = run_gear(season, experience)
        st.success("Gear recommendations generated!")

    if st.session_state.result_gear:
        st.write(st.session_state.result_gear)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style="text-align:center; padding:2rem; color:#3B2F2F; font-family:serif;">
    <em>Made with ❤️ under the towering Sequoias</em>
</div>
""", unsafe_allow_html=True)
