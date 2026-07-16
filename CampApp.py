import streamlit as st
from crewai import Agent, Task, Crew
from litellm import completion

# ============================================================
# RUSTIC / OUTDOORSY UI MAKEOVER
# ============================================================

st.set_page_config(page_title="Camping Planner AI", layout="wide")

st.markdown("""
<style>

    /* Global parchment background */
    .main {
        background-color: #F4EFE6;
        background-image: url('https://images.unsplash.com/photo-1501785888041-af3ef285b470');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    /* Pine needles + pinecone fade at top */
    .pine-top {
        background-image: url('https://images.unsplash.com/photo-1519681393784-d120267933ba');
        background-size: cover;
        background-position: top;
        height: 140px;
        opacity: 0.9;
        border-bottom: 4px solid #C97B3A;
    }

    /* Starlit sky through trees header */
    .rustic-header {
        background-image: url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee');
        background-size: cover;
        background-position: center;
        padding: 4rem 1rem;
        border-bottom: 6px solid #C97B3A;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
    }

    /* Firepit glow under header */
    .rustic-header::after {
        content: "";
        display: block;
        height: 90px;
        background: radial-gradient(circle at center, rgba(201,123,58,0.45), rgba(0,0,0,0));
        margin-top: -40px;
    }

    /* Rustic buttons */
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

    /* Rustic card style */
    .rustic-card {
        background-color: #E3DCCF;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
        border-left: 6px solid #C97B3A;
        margin-bottom: 1.5rem;
    }

    /* Section headers */
    h2 {
        color: #C97B3A !important;
        font-family: serif !important;
    }

</style>
""", unsafe_allow_html=True)

# ---------- Pine needle fade ----------
st.markdown('<div class="pine-top"></div>', unsafe_allow_html=True)

# ---------- Starlit sky header ----------
st.markdown("""
<div class="rustic-header">
    <h1 style="text-align:center; color:#F4EFE6; font-family:serif; font-size:3rem;">
        🏕️ Camping Planner AI
    </h1>
    <p style="text-align:center; color:#F4EFE6; font-size:1.2rem; font-family:serif;">
        Plan your perfect outdoor adventure under the stars
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR — USER INPUTS
# ============================================================

st.sidebar.header("🌿 Trip Settings")

season = st.sidebar.selectbox("Season or month", ["August", "September", "October"])
experience = st.sidebar.selectbox("Experience level", ["Beginner", "Intermediate", "Advanced"])
location = st.sidebar.text_input("Preferred region (optional)")

submit = st.sidebar.button("Generate Trip Plan")

# ============================================================
# CREWAI 1.15.x — GROQ VIA LITELLM
# ============================================================

groq_api_key = st.secrets["GROQ_API_KEY"]

def groq_llm(prompt: str) -> str:
    """LiteLLM wrapper for Groq."""
    response = completion(
        model="groq/llama3-8b-8192",
        api_key=groq_api_key,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# ---------- Agents ----------
planner_agent = Agent(
    role="Camping Planner",
    goal="Create detailed camping trip plans",
    backstory="You are an expert outdoor guide with decades of wilderness experience.",
    llm=groq_llm
)

packing_agent = Agent(
    role="Packing Expert",
    goal="Create packing lists based on season and experience",
    backstory="You specialize in wilderness gear and survival essentials.",
    llm=groq_llm
)

weather_agent = Agent(
    role="Weather Forecaster",
    goal="Provide weather forecasts for camping trips",
    backstory="You analyze weather patterns for outdoor safety.",
    llm=groq_llm
)

gear_agent = Agent(
    role="Gear Specialist",
    goal="Recommend camping gear",
    backstory="You know every piece of gear needed for any terrain.",
    llm=groq_llm
)

# ---------- Tasks / Runner functions ----------
def run_planner():
    task = Task(
        description=f"Create a camping plan for a {experience} camper in {season}. Region: {location}.",
        agent=planner_agent
    )
    crew = Crew(tasks=[task], agents=[planner_agent])
    return crew.run()

def run_packing_list():
    task = Task(
        description=f"Create a packing list for a {experience} camper in {season}.",
        agent=packing_agent
    )
    crew = Crew(tasks=[task], agents=[packing_agent])
    return crew.run()

def run_weather():
    task = Task(
        description=f"Provide a weather forecast for camping in {season} in {location}.",
        agent=weather_agent
    )
    crew = Crew(tasks=[task], agents=[weather_agent])
    return crew.run()

def run_gear():
    task = Task(
        description=f"Recommend camping gear for a {experience} camper in {season}.",
        agent=gear_agent
    )
    crew = Crew(tasks=[task], agents=[gear_agent])
    return crew.run()

# ============================================================
# MAIN CONTENT — TABS
# ============================================================

st.markdown("## 🌲 Your Camping Dashboard")

tab_plan, tab_packing, tab_weather, tab_gear = st.tabs(
    ["🧭 Trip Plan", "🎒 Packing List", "🌦️ Weather", "🪵 Gear"]
)

# ---------- Trip Plan Tab ----------
with tab_plan:
    st.markdown('<div class="rustic-card">', unsafe_allow_html=True)
    if submit:
        with st.spinner("Generating your camping plan..."):
            result = run_planner()
        st.success("Camping plan generated!")
        st.write(result)
    else:
        st.write("Fill out the trip settings on the left and click **Generate Trip Plan**.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Packing List Tab ----------
with tab_packing:
    st.markdown('<div class="rustic-card">', unsafe_allow_html=True)
    if st.button("Generate Packing List"):
        with st.spinner("Generating packing list..."):
            packing_list = run_packing_list()
        st.success("Packing list generated!")
        st.write(packing_list)
    else:
        st.write("Click **Generate Packing List** to get a gear checklist.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Weather Tab ----------
with tab_weather:
    st.markdown('<div class="rustic-card">', unsafe_allow_html=True)
    if st.button("Get Weather Forecast"):
        with st.spinner("Fetching weather forecast..."):
            weather = run_weather()
        st.success("Weather forecast generated!")
        st.write(weather)
    else:
        st.write("Click **Get Weather Forecast** to see conditions for your trip.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Gear Tab ----------
with tab_gear:
    st.markdown('<div class="rustic-card">', unsafe_allow_html=True)
    if st.button("Generate Gear Recommendations"):
        with st.spinner("Generating gear recommendations..."):
            gear = run_gear()
        st.success("Gear recommendations generated!")
        st.write(gear)
    else:
        st.write("Click **Generate Gear Recommendations** for tailored gear suggestions.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style="text-align:center; padding:2rem; color:#3B2F2F; font-family:serif;">
    <em>Made with ❤️ under the tall pines</em>
</div>
""", unsafe_allow_html=True)
