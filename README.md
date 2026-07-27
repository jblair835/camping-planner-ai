# Camping Planner AI

Camping Planner AI is a modular Python project that generates camping plans,
meal schedules, grocery lists, gear checklists, park information, safety tips,
and more. It is designed to be easy to extend, with each feature stored in its
own module.

## Features
- Meal selection based on camping style
- Grocery list generation
- Camp kitchen checklist
- Budget estimator
- Park information tools (national, state, permits, trails)
- Weather, terrain, wildlife, and gear tools
- Safety tools (fire rules, first aid, Leave No Trace)

## Project Structure
camping_planner_ai/
│
├── app/               # Main application entry points
├── core/              # All functional modules
│   ├── food/
│   ├── budget/
│   ├── safety/
│   ├── weather.py
│   ├── driving.py
│   ├── terrain.py
│   ├── wildlife.py
│   ├── packing.py
│   ├── gear.py
│   └── season.py
│
├── meals/             # Meal data dictionaries
├── utils/             # Shared helpers, validators, formatters
└── tests/             # Unit tests

## Running the App
Run the main application:

