#=============================
#   MY CAMPING APP
#=============================
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import requests
import random
import os

# ============================
#   STREAMLIT UI
# ============================

st.set_page_config(page_title="Camping Planner AI", layout="wide")
st.title("🏕️ Camping Planner AI")
st.write("Plan KOA, State Park, and National Park camping trips with AI-powered itineraries, meals, groceries, gear lists, safety tips, and more.")

# ---------------------------
# USER INPUT FIELDS
# ---------------------------

location = st.text_input("Where do you want to camp?")
origin = st.text_input("Where are you driving from?")
num_people = st.number_input("Number of people", min_value=1, step=1)
num_days = st.number_input("Number of days camping", min_value=1, step=1)
camp_style = st.selectbox("Camping style", ["Tent", "RV", "Cabin", "Backpacking"])
season = st.text_input("Season or month")
experience_level = st.selectbox("Experience level", ["Beginner", "Intermediate", "Advanced"])

st.divider()

# ============================
#   CLOUD LLM (GROQ)
# ============================

from crewai.llms import Groq

llm = Groq(
    model="llama3-8b-8192",
    api_key=st.secrets["GROQ_API_KEY"]
)

# ============================
#   CAMPING PLANNER TOOLS
# ============================

@tool
def park_summary(park_name: str) -> str:
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{park_name.replace(' ', '_')}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("extract", "No summary available.")
    except Exception as e:
        return f"Error fetching park summary: {e}"

@tool
def koa_info(location_hint: str) -> str:
    return f"KOA campgrounds near {location_hint}: RV sites, tent sites, cabins, showers, and family amenities."

@tool
def state_park_info(location_hint: str) -> str:
    return f"State park camping near {location_hint}: designated campsites, restrooms, picnic areas, and marked trails."

@tool
def national_park_info(location_hint: str) -> str:
    return f"National park camping near {location_hint}: limited amenities, stunning scenery, stricter rules."

@tool
def driving_distance(origin: str, destination: str) -> str:
    return f"Estimated driving distance from {origin} to {destination}: 1–6 hours depending on exact locations."

@tool
def estimated_drive_time(distance_hint: str) -> str:
    return f"Drive time based on {distance_hint}: plan for rest stops, fuel, and possible traffic."

@tool
def terrain_info(location_hint: str) -> str:
    return f"Terrain around {location_hint}: forests, hills, rivers, or desert depending on the park."

@tool
def camp_weather(location_hint: str) -> str:
    sample_weather = [
        "Cool nights, warm days.",
        "Hot and dry.",
        "Chilly and rainy.",
        "Mild with wind.",
        "Cold nights, moderate days."
    ]
    return f"Camping weather near {location_hint}: {random.choice(sample_weather)}"

@tool
def weather_risks(location_hint: str) -> str:
    return f"Weather risks near {location_hint}: storms, wind, heat, cold — check forecasts."

@tool
def best_season_to_camp(location_hint: str, season_hint: str = "") -> str:
    base = f"Best seasons to camp near {location_hint}: spring and fall."
    return base + (f" You mentioned {season_hint}." if season_hint else "")

@tool
def campground_highlights(location_hint: str) -> str:
    return f"Campground highlights near {location_hint}: scenic views, trails, picnic areas, fire rings."

@tool
def trail_highlights(location_hint: str) -> str:
    return f"Trail highlights near {location_hint}: nature walks, day hikes, backcountry routes."

@tool
def wildlife_info(location_hint: str) -> str:
    return f"Wildlife near {location_hint}: deer, birds, small mammals, possibly bears or coyotes."

@tool
def permit_requirements(location_hint: str) -> str:
    return f"Permits near {location_hint}: check park websites for reservations and fire permits."

@tool
def camping_gear_list(style: str, season_hint: str, num_people: int) -> str:
    base = [
        "Tent/shelter", "Sleeping bags", "Sleeping pads", "Camp stove", "Fuel",
        "Cookware", "Cooler", "Headlamps", "First-aid kit", "Water containers",
        "Knife", "Fire starter", "Trash bags"
    ]
    extras = []
    if style.lower() == "rv":
        extras.append("RV hookups, leveling blocks")
    if style.lower() == "backpacking":
        extras.append("Lightweight gear, trekking poles")
    if "cold" in season_hint.lower():
        extras.append("Winter-rated sleeping bags, insulated clothing")

    return "Gear List:\n" + "\n".join(f"- {i}" for i in base + extras)

@tool
def food_plan(num_days: int, num_people: int) -> str:
    return (
        f"Food plan for {num_people} people over {num_days} days:\n"
        "- Breakfasts: oatmeal, eggs, fruit\n"
        "- Lunches: sandwiches, wraps, trail mix\n"
        "- Dinners: grilled items, foil packets, one-pot meals\n"
        "- Snacks: nuts, bars, jerky\n"
        "- Drinks: water, electrolytes"
    )

@tool
def meal_selector(num_days: int, style: str) -> str:
    simple = {
        "breakfast": ["Oatmeal", "Eggs & tortillas", "Fruit & granola"],
        "lunch": ["Sandwiches", "Wraps", "Trail mix + jerky"],
        "dinner": ["Foil packet veggies + sausage", "Grilled chicken + rice", "Chili + cornbread"],
    }
    gourmet = {
        "breakfast": ["Pancakes", "Breakfast burritos", "French toast"],
        "lunch": ["Chicken salad wraps", "Charcuterie board"],
        "dinner": ["Dutch oven stew", "Campfire fajitas", "BBQ ribs + potatoes"],
    }
    backpacking = {
        "breakfast": ["Instant oatmeal", "Protein bars"],
        "lunch": ["Tuna packets + crackers"],
        "dinner": ["Freeze-dried meals", "Ramen + dehydrated veggies"],
    }

    if style.lower() in ["rv", "cabin", "luxury"]:
        meals = gourmet
    elif style.lower() == "backpacking":
        meals = backpacking
    else:
        meals = simple

    out = f"Selected meals for {num_days} days ({style}):\n\n"
    for d in range(1, num_days + 1):
        out += (
            f"Day {d}:\n"
            f"- Breakfast: {random.choice(meals['breakfast'])}\n"
            f"- Lunch: {random.choice(meals['lunch'])}\n"
            f"- Dinner: {random.choice(meals['dinner'])}\n\n"
        )
    return out

@tool
def grocery_list_from_meals(meal_plan: str, num_people: int) -> str:
    ingredients = {
        "Oatmeal": ["Oatmeal packets", "Brown sugar"],
        "Eggs & tortillas": ["Eggs", "Tortillas", "Cheese"],
        "Fruit & granola": ["Granola", "Apples"],
        "Sandwiches": ["Bread", "Lunch meat", "Cheese"],
        "Wraps": ["Tortillas", "Chicken"],
        "Trail mix + jerky": ["Trail mix", "Jerky"],
        "Foil packet veggies + sausage": ["Sausage", "Bell peppers", "Onions"],
        "Grilled chicken + rice": ["Chicken", "Rice"],
        "Chili + cornbread": ["Canned chili", "Cornbread mix"],
        "Pancakes": ["Pancake mix", "Syrup"],
        "Breakfast burritos": ["Eggs", "Tortillas", "Salsa"],
        "Dutch oven stew": ["Stew meat", "Potatoes", "Carrots"],
        "Campfire fajitas": ["Chicken", "Bell peppers", "Tortillas"],
        "BBQ ribs + potatoes": ["Ribs", "Potatoes"],
        "Freeze-dried meals": ["Freeze-dried meals"],
        "Ramen + dehydrated veggies": ["Ramen", "Dehydrated veggies"]
    }

    grocery = {}
    for line in meal_plan.splitlines():
        for meal, items in ingredients.items():
            if meal in line:
                for item in items:
                    grocery[item] = grocery.get(item, 0) + num_people

    return "Grocery List:\n" + "\n".join(f"- {i}: {q}" for i, q in grocery.items())

@tool
def camp_kitchen_checklist(style: str) -> str:
    base = [
        "Camp stove", "Fuel", "Cookware", "Cutting board", "Knife",
        "Spatula", "Plates", "Bowls", "Cups", "Utensils",
        "Trash bags", "Dish soap", "Sponge", "Cooler", "Ice"
    ]
    extras = []
    if style.lower() in ["rv", "cabin"]:
        extras.extend(["Coffee maker", "Electric skillet"])
    if style.lower() == "backpacking":
        extras.extend(["Lightweight pot", "Titanium spork"])

    return "Camp Kitchen Checklist:\n" + "\n".join(f"- {i}" for i in base + extras)

@tool
def camp_budget(num_days: int, num_people: int, campsite_fee: float, food_cost_per_day: float, fuel_cost: float) -> str:
    total = campsite_fee * num_days + food_cost_per_day * num_days * num_people + fuel_cost
    return (
        f"Budget Estimate:\n"
        f"- Campsite fees: ${campsite_fee * num_days:.2f}\n"
        f"- Food: ${food_cost_per_day * num_days * num_people:.2f}\n"
        f"- Fuel: ${fuel_cost:.2f}\n"
        f"Total: ${total:.2f}"
    )

@tool
def fire_rules(location_hint: str) -> str:
    return f"Fire rules near {location_hint}: use designated rings, keep fires small, extinguish fully."

@tool
def first_aid_tips() -> str:
    return "First-aid: treat cuts, watch dehydration, handle burns, seek help for serious injuries."

@tool
def leave_no_trace() -> str:
    return "Leave No Trace: plan ahead, camp on durable surfaces, pack out trash, respect wildlife."

# ============================
#   AGENTS
# ============================

destination_scout = Agent(
    role="Destination Scout",
    goal="Recommend a KOA, state park, or national park camping area.",
    backstory="You match campers with great campgrounds.",
    llm=llm,
    tools=[
        park_summary, koa_info, state_park_info, national_park_info,
        driving_distance, camp_weather, best_season_to_camp,
        terrain_info, permit_requirements
    ],
)

trail_planner = Agent(
    role="Trail Planner",
    goal="Create a day-by-day camping itinerary.",
    backstory="You design outdoor days with hikes and camp time.",
    llm=llm,
    tools=[trail_highlights, campground_highlights, wildlife_info],
)

gear_budget_reviewer = Agent(
    role="Gear & Budget Reviewer",
    goal="Provide gear list, meal plan, groceries, kitchen checklist, and budget.",
    backstory="You think practically about camping needs.",
    llm=llm,
    tools=[
        camping_gear_list, food_plan, meal_selector,
        grocery_list_from_meals, camp_kitchen_checklist, camp_budget
    ],
)

safety_advisor = Agent(
    role="Safety Advisor",
    goal="Provide safety guidance.",
    backstory="You keep campers safe.",
    llm=llm,
    tools=[fire_rules, first_aid_tips, leave_no_trace, weather_risks, wildlife_info],
)

calendar_scheduler = Agent(
    role="Calendar Scheduler",
    goal="Convert itinerary into calendar events.",
    backstory="You organize camping days.",
    llm=llm,
)

# ============================
#   TASKS
# ============================

destination_task = Task(
    description=(
        f"Recommend a camping area near {location} for {num_people} people "
        f"for {num_days} days in {season}."
    ),
    agent=destination_scout,
)

itinerary_task = Task(
    description=f"Create a {num_days}-day camping itinerary.",
    agent=trail_planner,
    context=[destination_task],
)

gear_budget_task = Task(
    description="Provide gear list, meal plan, grocery list, kitchen checklist, and budget.",
    agent=gear_budget_reviewer,
    context=[itinerary_task],
)

safety_task = Task(
    description="Provide safety guidance for the camping trip.",
    agent=safety_advisor,
    context=[gear_budget_task],
)

calendar_task = Task(
    description="Convert itinerary into calendar-ready events.",
    agent=calendar_scheduler,
    context=[itinerary_task],
)

# ============================
#   RUN PLANNER
# ============================

def run_planner():
    crew = Crew(
        agents=[
            destination_scout,
            trail_planner,
            gear_budget_reviewer,
            safety_advisor,
            calendar_scheduler
        ],
        tasks=[
            destination_task,
            itinerary_task,
            gear_budget_task,
            safety_task,
            calendar_task
        ],
        process=Process.sequential,
    )
    return crew.kickoff()

# ============================
#   STREAMLIT BUTTON
# ============================

if st.button("Generate Camping Plan"):
    with st.spinner("Generating your camping plan..."):
        result = run_planner()
    st.success("Camping plan generated!")
    st.write(result)
