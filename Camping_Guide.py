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

# ---------------------------
# CORE INFO TOOLS
# ---------------------------

@tool
def park_summary(park_name: str) -> str:
    """Fetch a summary for a park or campground using Wikipedia API."""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{park_name.replace(' ', '_')}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("extract", "No summary available.")
    except Exception as e:
        return f"Error fetching park summary: {e}"


@tool
def koa_info(location_hint: str) -> str:
    """Provide generic KOA campground info based on a region."""
    return (
        f"KOA campgrounds near {location_hint}: "
        "Expect RV sites, tent sites, cabins, restrooms, showers, and family-friendly amenities."
    )


@tool
def state_park_info(location_hint: str) -> str:
    """Provide generic state park camping info."""
    return (
        f"State park camping near {location_hint}: "
        "Typically offers designated campsites, restrooms, picnic areas, and marked trails."
    )


@tool
def national_park_info(location_hint: str) -> str:
    """Provide generic national park camping info."""
    return (
        f"National park camping near {location_hint}: "
        "Expect campgrounds with limited amenities, stunning scenery, and stricter rules."
    )

# ---------------------------
# DRIVING & TERRAIN TOOLS
# ---------------------------

@tool
def driving_distance(origin: str, destination: str) -> str:
    """Estimate driving distance between origin and destination."""
    return (
        f"Estimated driving distance from {origin} to {destination}: "
        "Between 1 and 6 hours depending on exact locations."
    )


@tool
def estimated_drive_time(distance_hint: str) -> str:
    """Provide a rough drive time description."""
    return (
        f"Drive time based on {distance_hint}: "
        "Plan for rest stops, fuel, and possible traffic."
    )


@tool
def terrain_info(location_hint: str) -> str:
    """Describe typical terrain for camping in the area."""
    return (
        f"Terrain around {location_hint}: "
        "Could include forests, hills, rivers, or desert. Check specific park maps for details."
    )

# ---------------------------
# WEATHER & SEASON TOOLS
# ---------------------------

@tool
def camp_weather(location_hint: str) -> str:
    """Return a simple camping weather summary."""
    sample_weather = [
        "Cool nights, warm days.",
        "Hot and dry during the day, cooler at night.",
        "Chilly and possibly rainy.",
        "Mild temperatures with occasional wind.",
        "Cold nights, moderate days.",
        "Variable weather—pack layers."
    ]
    return f"Camping weather near {location_hint}: {random.choice(sample_weather)}"


@tool
def weather_risks(location_hint: str) -> str:
    """Describe potential weather-related risks."""
    return (
        f"Weather risks near {location_hint}: "
        "Watch for storms, high winds, extreme heat or cold, and check forecasts before departure."
    )


@tool
def best_season_to_camp(location_hint: str, season_hint: str = "") -> str:
    """Suggest the best season to camp."""
    base = (
        f"Best seasons to camp near {location_hint}: "
        "Typically spring and fall for comfortable temperatures and fewer bugs."
    )
    if season_hint:
        return base + f" You mentioned {season_hint}; verify local conditions for that time."
    return base

# ---------------------------
# CAMPGROUND & TRAIL TOOLS
# ---------------------------

@tool
def campground_highlights(location_hint: str) -> str:
    """Describe typical campground highlights."""
    return (
        f"Campground highlights near {location_hint}: "
        "Scenic views, nearby trails, picnic areas, fire rings, and access to water or restrooms."
    )


@tool
def trail_highlights(location_hint: str) -> str:
    """Describe typical trail options."""
    return (
        f"Trail highlights near {location_hint}: "
        "Short nature walks, moderate day hikes, and possibly longer backcountry routes."
    )


@tool
def wildlife_info(location_hint: str) -> str:
    """Provide general wildlife info."""
    return (
        f"Wildlife near {location_hint}: "
        "Expect common animals like deer, birds, small mammals, and possibly bears or coyotes. "
        "Store food properly and never feed wildlife."
    )


@tool
def permit_requirements(location_hint: str) -> str:
    """Describe typical permit requirements."""
    return (
        f"Permits near {location_hint}: "
        "Check park or campground websites for reservation requirements, fire permits, and backcountry permits."
    )

# ---------------------------
# GEAR, FOOD, PACKING TOOLS
# ---------------------------

@tool
def camping_gear_list(style: str, season_hint: str, num_people: int) -> str:
    """Generate a basic camping gear list."""
    base = [
        "Tent or shelter",
        "Sleeping bags and pads",
        "Camp stove or grill",
        "Fuel",
        "Cookware and utensils",
        "Cooler and food storage",
        "Headlamps/flashlights",
        "First-aid kit",
        "Water containers or filter",
        "Multi-tool or knife",
        "Fire starter (where allowed)",
        "Trash bags (pack it out)"
    ]
    extras = []
    if style.lower() == "rv":
        extras.append("RV hookups, leveling blocks, extra hoses and cables")
    if style.lower() == "backpacking":
        extras.append("Lightweight gear, trekking poles, compact food, bear canister if needed")
    if "winter" in season_hint.lower() or "cold" in season_hint.lower():
        extras.append("Extra insulation layers, winter-rated sleeping bags, snow-ready footwear")

    list_text = "\n".join(f"- {item}" for item in base + extras)
    return (
        f"Camping gear list for {num_people} people, style: {style}, season: {season_hint}:\n"
        f"{list_text}"
    )


@tool
def food_plan(num_days: int, num_people: int) -> str:
    """Suggest a simple camping food plan."""
    return (
        f"Food plan for {num_people} people over {num_days} days:\n"
        "- Easy breakfasts (oatmeal, eggs, fruit)\n"
        "- Simple lunches (sandwiches, wraps, trail mix)\n"
        "- Camp dinners (grilled items, one-pot meals, foil packets)\n"
        "- Snacks (nuts, bars, jerky)\n"
        "- Plenty of water and electrolyte drinks\n"
        "Adjust quantities based on appetite and activity level."
    )


@tool
def packing_suggestions_camping(style: str, season_hint: str, experience: str) -> str:
    """Provide packing suggestions based on camping style, season, and experience."""
    base = "Pack layers, sturdy footwear, and weather-appropriate clothing."
    if "summer" in season_hint.lower():
        base += " Include sun protection, bug spray, and light breathable fabrics."
    if "winter" in season_hint.lower() or "cold" in season_hint.lower():
        base += " Include thermal layers, hats, gloves, and insulated boots."
    if style.lower() == "backpacking":
        base += " Focus on lightweight, compact gear."
    if experience.lower() == "beginner":
        base += " Double-check essentials: shelter, warmth, food, water, navigation, and first-aid."
    return base

# ---------------------------
# MEAL SELECTOR & GROCERY LIST
# ---------------------------

@tool
def meal_selector(num_days: int, style: str) -> str:
    """Select camping meals based on number of days and camping style."""
    simple_meals = {
        "breakfast": ["Oatmeal", "Eggs & tortillas", "Fruit & granola"],
        "lunch": ["Sandwiches", "Wraps", "Trail mix + jerky"],
        "dinner": ["Foil packet veggies + sausage", "Grilled chicken + rice", "Chili + cornbread"],
    }

    gourmet_meals = {
        "breakfast": ["Pancakes", "Breakfast burritos", "French toast"],
        "lunch": ["Chicken salad wraps", "Charcuterie board", "Veggie hummus sandwiches"],
        "dinner": ["Dutch oven stew", "Campfire fajitas", "BBQ ribs + potatoes"],
    }

    backpacking_meals = {
        "breakfast": ["Instant oatmeal", "Protein bars"],
        "lunch": ["Tuna packets + crackers", "Freeze-dried meals"],
        "dinner": ["Freeze-dried entrees", "Instant ramen + dehydrated veggies"],
    }

    if style.lower() in ["luxury", "rv", "cabin"]:
        meals = gourmet_meals
    elif style.lower() in ["backpacking"]:
        meals = backpacking_meals
    else:
        meals = simple_meals

    output = f"Selected meals for {num_days} days ({style} style):\n\n"
    for day in range(1, num_days + 1):
        output += (
            f"Day {day}:\n"
            f"- Breakfast: {random.choice(meals['breakfast'])}\n"
            f"- Lunch: {random.choice(meals['lunch'])}\n"
            f"- Dinner: {random.choice(meals['dinner'])}\n\n"
        )
    return output


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