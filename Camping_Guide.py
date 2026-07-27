# ============================
#   CAMPING PLANNING CREW AI
#   (KOA + National & State Parks)
# ============================

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import requests
import random

# ---------------------------
# USER INPUT
# ---------------------------
location = input("Where do you want to camp (park name or region)? ")
origin = input("Where are you driving from (city or region)? ")
num_people = int(input("How many people are camping? "))
num_days = int(input("How many days will you camp? "))
camp_style = input("Camping style (tent, RV, cabin, backpacking)? ")
season = input("Season or month of your trip? ")
experience_level = input("Experience level (beginner, intermediate, advanced)? ")






@tool
def grocery_list_from_meals(meal_plan: str, num_people: int) -> str:
    """Generate a grocery list based on the selected meals."""
    ingredients = {
        "Oatmeal": ["Oatmeal packets", "Brown sugar", "Dried fruit"],
        "Eggs & tortillas": ["Eggs", "Tortillas", "Cheese"],
        "Fruit & granola": ["Granola", "Apples", "Bananas"],
        "Sandwiches": ["Bread", "Lunch meat", "Cheese", "Mustard"],
        "Wraps": ["Tortillas", "Lettuce", "Chicken", "Ranch"],
        "Trail mix + jerky": ["Trail mix", "Jerky"],
        "Foil packet veggies + sausage": ["Sausage", "Bell peppers", "Onions", "Foil"],
        "Grilled chicken + rice": ["Chicken", "Rice", "Seasoning"],
        "Chili + cornbread": ["Canned chili", "Cornbread mix"],
        "Pancakes": ["Pancake mix", "Syrup"],
        "Breakfast burritos": ["Eggs", "Tortillas", "Salsa"],
        "French toast": ["Bread", "Eggs", "Cinnamon"],
        "Chicken salad wraps": ["Chicken", "Tortillas", "Mayo"],
        "Charcuterie board": ["Crackers", "Cheese", "Salami"],
        "Veggie hummus sandwiches": ["Bread", "Hummus", "Veggies"],
        "Dutch oven stew": ["Stew meat", "Potatoes", "Carrots"],
        "Campfire fajitas": ["Chicken", "Bell peppers", "Tortillas"],
        "BBQ ribs + potatoes": ["Ribs", "Potatoes", "BBQ sauce"],
        "Instant oatmeal": ["Instant oatmeal", "Dried fruit"],
        "Protein bars": ["Protein bars"],
        "Tuna packets + crackers": ["Tuna packets", "Crackers"],
        "Freeze-dried meals": ["Freeze-dried meals"],
        "Instant ramen + dehydrated veggies": ["Ramen", "Dehydrated veggies"]
    }

    grocery = {}

    for line in meal_plan.splitlines():
        for meal, items in ingredients.items():
            if meal in line:
                for item in items:
                    grocery[item] = grocery.get(item, 0) + num_people

    output = "Grocery List:\n"
    for item, qty in grocery.items():
        output += f"- {item}: {qty}\n"

    return output

# ---------------------------
# CAMP KITCHEN CHECKLIST
# ---------------------------

@tool
def camp_kitchen_checklist(style: str) -> str:
    """Provide a camp kitchen checklist based on camping style."""
    base = [
        "Camp stove or grill",
        "Fuel canisters or propane",
        "Lighter/matches",
        "Cookware (pan, pot)",
        "Cutting board",
        "Knife",
        "Spatula & tongs",
        "Plates/bowls",
        "Cups/mugs",
        "Eating utensils",
        "Trash bags",
        "Dish soap",
        "Sponge/scrubber",
        "Cooler & ice",
        "Food storage containers",
        "Aluminum foil",
        "Paper towels",
    ]

    extras = []
    if style.lower() in ["rv", "cabin", "luxury"]:
        extras.extend(["Electric skillet", "Coffee maker", "Extra storage bins"])

    if style.lower() == "backpacking":
        extras.extend(["Lightweight pot", "Titanium spork", "Compact stove"])

    checklist = "\n".join(f"- {item}" for item in base + extras)
    return f"Camp Kitchen Checklist ({style} style):\n{checklist}"

# ---------------------------
# BUDGET TOOLS
# ---------------------------

@tool
def camp_budget(num_days: int, num_people: int, campsite_fee: float, food_cost_per_day: float, fuel_cost: float) -> str:
    """Estimate a simple camping budget."""
    campsite_total = campsite_fee * num_days
    food_total = food_cost_per_day * num_days * num_people
    total = campsite_total + food_total + fuel_cost
    return (
        f"Camping budget estimate for {num_people} people over {num_days} days:\n"
        f"- Campsite fees: ${campsite_total:.2f}\n"
        f"- Food: ${food_total:.2f}\n"
        f"- Fuel: ${fuel_cost:.2f}\n"
        f"\nTotal Estimated Cost: ${total:.2f}"
    )

# ---------------------------
# SAFETY & ETHICS TOOLS
# ---------------------------

@tool
def fire_rules(location_hint: str) -> str:
    """Provide general campfire rules."""
    return (
        f"Fire rules near {location_hint}: "
        "Check current fire restrictions. Use designated fire rings, keep fires small, "
        "never leave them unattended, and fully extinguish before leaving."
    )


@tool
def first_aid_tips() -> str:
    """Provide basic first-aid tips."""
    return (
        "Basic first-aid tips:\n"
        "- Treat cuts and scrapes promptly\n"
        "- Watch for signs of dehydration and heat exhaustion\n"
        "- Know how to handle minor burns and sprains\n"
        "- Seek help for serious injuries or allergic reactions"
    )


@tool
def leave_no_trace() -> str:
    """Summarize Leave No Trace principles."""
    return (
        "Leave No Trace principles:\n"
        "- Plan ahead and prepare\n"
        "- Travel and camp on durable surfaces\n"
        "- Dispose of waste properly\n"
        "- Leave what you find\n"
        "- Minimize campfire impacts\n"
        "- Respect wildlife\n"
        "- Be considerate of other visitors"
    )

# ---------------------------
# LLM
# ---------------------------

llm = LLM(model="llama3.2", provider="ollama")

# ---------------------------
# AGENTS
# ---------------------------

destination_scout = Agent(
    role="Destination Scout",
    goal="Recommend a suitable KOA, state park, or national park camping area.",
    backstory=(
        "You specialize in matching campers with great campgrounds and parks. "
        "You consider driving distance, season, group size, and experience level."
    ),
    llm=llm,
    tools=[
        park_summary, koa_info, state_park_info, national_park_info,
        driving_distance, camp_weather, best_season_to_camp, terrain_info, permit_requirements
    ],
    verbose=True
)

trail_planner = Agent(
    role="Trail & Activity Planner",
    goal="Create a balanced day-by-day camping plan with hikes, camp time, and highlights.",
    backstory="You design outdoor days that mix hiking, relaxing at camp, and exploring nearby features.",
    llm=llm,
    tools=[trail_highlights, campground_highlights, wildlife_info],
    verbose=True
)

gear_budget_reviewer = Agent(
    role="Gear & Budget Reviewer",
    goal="Review gear, food, kitchen setup, and costs to ensure the trip is safe and affordable.",
    backstory="You think practically about what people need and how much it will cost.",
    llm=llm,
    tools=[
        camping_gear_list,
        food_plan,
        meal_selector,
        grocery_list_from_meals,
        camp_kitchen_checklist,
        camp_budget
    ],
    verbose=True
)

safety_advisor = Agent(
    role="Outdoor Safety Advisor",
    goal="Provide safety guidance, fire rules, first-aid tips, and Leave No Trace advice.",
    backstory="You care deeply about keeping campers safe and protecting nature.",
    llm=llm,
    tools=[fire_rules, first_aid_tips, leave_no_trace, weather_risks, wildlife_info],
    verbose=True
)

camp_calendar_scheduler = Agent(
    role="Camping Calendar Scheduler",
    goal="Convert the camping plan into structured calendar events.",
    backstory="You turn camping plans into clear, scheduled days with activities and reminders.",
    llm=llm,
    verbose=True
)

# ---------------------------
# TASKS
# ---------------------------

destination_task = Task(
    description=(
        f"User wants to camp near {location}.\n"
        f"Driving from: {origin}.\n"
        f"Group size: {num_people} people.\n"
        f"Trip length: {num_days} days.\n"
        f"Camping style: {camp_style}.\n"
        f"Season: {season}.\n"
        f"Experience level: {experience_level}.\n\n"
        "Recommend a KOA, state park, or national park area suitable for this group. "
        "Consider driving distance, terrain, season, and experience level.\n\n"
        "Output format:\n"
        "Camping Destination Recommendation:\n"
        "- Area: <park or campground name>\n"
        "- Why it fits: <reason>\n"
        "- Highlights: <3 bullet points>\n"
    ),
    expected_output="A clear camping destination recommendation with reasons.",
    agent=destination_scout
)

itinerary_task = Task(
    description=(
        f"Create a detailed {num_days}-day camping plan for the recommended area "
        f"for {num_people} people with {camp_style} style.\n"
        "Include daily structure: drive/arrival (day 1), camp setup, hikes, meals, "
        "relaxation time, and departure.\n"
    ),
    expected_output="A structured day-by-day camping itinerary.",
    agent=trail_planner,
    context=[destination_task]
)

gear_budget_task = Task(
    description=(
        f"Review the camping itinerary for {num_days} days and {num_people} people.\n"
        "Generate a meal plan, grocery list, camp kitchen checklist, gear list, "
        "and a basic budget including campsite fees, food, and fuel.\n"
    ),
    expected_output="Gear list, food plan, grocery list, kitchen checklist, and budget estimate.",
    agent=gear_budget_reviewer,
    context=[itinerary_task]
)

safety_task = Task(
    description=(
        f"Provide safety guidance for camping near {location} in {season} "
        f"for {num_people} people with {experience_level} experience.\n"
        "Include fire rules, wildlife safety, weather risks, first-aid basics, "
        "and Leave No Trace reminders.\n"
    ),
    expected_output="Safety tips and ethical camping guidance.",
    agent=safety_advisor,
    context=[gear_budget_task]
)

calendar_task = Task(
    description=(
        f"Convert the {num_days}-day camping itinerary into calendar-ready events.\n"
        "For each day, create entries like:\n"
        "[{{title, date, start_time, end_time, description}}]\n"
        "Include drive/arrival, camp setup, main hike/activity, meals, and departure.\n"
    ),
    expected_output="A JSON-like list of calendar events.",
    agent=camp_calendar_scheduler,
    context=[itinerary_task]
)

# ---------------------------
# CREW
# ---------------------------

crew = Crew(
    agents=[
        destination_scout,
        trail_planner,
        gear_budget_reviewer,
        safety_advisor,
        camp_calendar_scheduler
    ],
    tasks=[
        destination_task,
        itinerary_task,
        gear_budget_task,
        safety_task,
        calendar_task
    ],
    process=Process.sequential,
    verbose=True
)

# ---------------------------
# RUN
# ---------------------------

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n\n===== CAMPING PLAN OUTPUT =====\n")
    print(result)