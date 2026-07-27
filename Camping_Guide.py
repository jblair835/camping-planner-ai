# ============================
#   CAMPING PLANNING CREW AI
# ============================

import os

from crewai import Agent, Task, Crew, Process, LLM

# Parks
from parks.summary import get_park_summary
from parks.national import get_national_park_info
from parks.state import get_state_park_info
from parks.permits import get_permit_requirements
from parks.trail_highlights import get_trail_highlights

# Driving & Weather
from core.driving import get_driving_distance, get_estimated_drive_time
from core.weather import get_weather_forecast
from core.safety.weather_risks import get_weather_risks

# Terrain & Wildlife
from core.terrain import get_terrain_info
from core.wildlife import get_wildlife_info

# Gear & Packing
from core.gear import get_camping_gear_list
from core.packing import get_packing_suggestions

# Food Tools
from core.food.meal_selector import select_meals
from core.food.grocery_list import generate_grocery_list
from core.food.kitchen_checklist import get_kitchen_checklist
from core.food.food_plan import generate_food_plan

# Budget
from core.budget.budget_estimator import estimate_budget

# Safety
from core.safety.fire_rules import get_fire_rules
from core.safety.first_aid import get_first_aid_tips
from core.safety.leave_no_trace import get_leave_no_trace_summary

# Calendar & Reports
from utils.calendar_export import export_to_ics
from utils.report import generate_pdf_report

import json

llm = LLM(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    provider="openai"
)


def run_guide(
    location: str,
    origin: str,
    num_people: int,
    num_days: int,
    camp_style: str,
    season: str,
    experience_level: str,
    json_output: bool = False,
    export_calendar: bool = False,
    export_pdf: bool = False,
) -> str:
    """Run the full Camping Planner AI workflow."""

    destination_scout = Agent(
        role="Destination Scout",
        goal="Recommend a suitable KOA, state park, or national park camping area.",
        backstory="You specialize in matching campers with great campgrounds and parks.",
        llm=llm,
        tools=[
            get_park_summary,
            get_state_park_info,
            get_national_park_info,
            get_driving_distance,
            get_weather_forecast,
            get_terrain_info,
            get_permit_requirements,
        ],
        verbose=True,
    )

    trail_planner = Agent(
        role="Trail & Activity Planner",
        goal="Create a balanced day-by-day camping plan.",
        backstory="You design outdoor days that mix hiking, relaxing, and exploring.",
        llm=llm,
        tools=[get_trail_highlights, get_wildlife_info],
        verbose=True,
    )

    gear_budget_reviewer = Agent(
        role="Gear & Budget Reviewer",
        goal="Review gear, food, kitchen setup, and costs.",
        backstory="You think practically about what people need and how much it will cost.",
        llm=llm,
        tools=[
            get_camping_gear_list,
            generate_food_plan,
            select_meals,
            generate_grocery_list,
            get_kitchen_checklist,
            estimate_budget,
        ],
        verbose=True,
    )

    safety_advisor = Agent(
        role="Outdoor Safety Advisor",
        goal="Provide safety guidance, fire rules, first-aid tips, and Leave No Trace advice.",
        backstory="You care deeply about keeping campers safe and protecting nature.",
        llm=llm,
        tools=[
            get_fire_rules,
            get_first_aid_tips,
            get_leave_no_trace_summary,
            get_weather_risks,
            get_wildlife_info,
        ],
        verbose=True,
    )

    camp_calendar_scheduler = Agent(
        role="Camping Calendar Scheduler",
        goal="Convert the camping plan into structured calendar events.",
        backstory="You turn camping plans into clear, scheduled days.",
        llm=llm,
        verbose=True,
    )

    destination_task = Task(
        description=(
            f"User wants to camp near {location}.\n"
            f"Driving from: {origin}.\n"
            f"Group size: {num_people}.\n"
            f"Trip length: {num_days} days.\n"
            f"Camping style: {camp_style}.\n"
            f"Season: {season}.\n"
            f"Experience level: {experience_level}.\n\n"
            "Recommend a KOA, state park, or national park area."
        ),
        expected_output="A clear camping destination recommendation.",
        agent=destination_scout,
    )

    itinerary_task = Task(
        description=(
            f"Create a detailed {num_days}-day camping plan "
            f"for {num_people} people with {camp_style} style."
        ),
        expected_output="A structured day-by-day itinerary.",
        agent=trail_planner,
        context=[destination_task],
    )

    gear_budget_task = Task(
        description=(
            f"Review the itinerary and generate a meal plan, grocery list, "
            "kitchen checklist, gear list, and budget."
        ),
        expected_output="Gear list, food plan, grocery list, kitchen checklist, and budget.",
        agent=gear_budget_reviewer,
        context=[itinerary_task],
    )

    safety_task = Task(
        description=(
            f"Provide safety guidance for camping near {location} in {season} "
            f"for {num_people} people."
        ),
        expected_output="Safety tips and ethical camping guidance.",
        agent=safety_advisor,
        context=[gear_budget_task],
    )

    calendar_task = Task(
        description=(
            f"Convert the {num_days}-day itinerary into calendar-ready events."
        ),
        expected_output="A JSON-like list of calendar events.",
        agent=camp_calendar_scheduler,
        context=[itinerary_task],
    )

    crew = Crew(
        agents=[
            destination_scout,
            trail_planner,
            gear_budget_reviewer,
            safety_advisor,
            camp_calendar_scheduler,
        ],
        tasks=[
            destination_task,
            itinerary_task,
            gear_budget_task,
            safety_task,
            calendar_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    if json_output:
        return json.dumps({"camping_plan": result}, indent=2)

    if export_pdf:
        generate_pdf_report(result)

    if export_calendar:
        try:
            events = json.loads(result)
            export_to_ics(events)
        except Exception:
            pass

    return result
