from crewai_tools import tool

@tool
def get_camping_gear_list(num_people: int, num_days: int, camp_style: str) -> dict:
    """
    Generate a camping gear list based on group size, trip length, and camping style.
    Returns a JSON-serializable dictionary CrewAI can use.
    """

    base = [
        "Tent",
        "Sleeping bags",
        "Sleeping pads",
        "Headlamps",
        "Water bottles",
        "First-aid kit",
        "Multi-tool",
        "Rain gear",
        "Warm layers",
    ]

    # Corrected: use camp_style, not style
    if camp_style.lower() == "rv":
        base.extend(["RV hookups", "Extension cords", "Leveling blocks"])

    if camp_style.lower() == "backpacking":
        base.extend(["Ultralight tent", "Compact stove", "Water filter"])

    # CrewAI requires JSON-safe output
    return {
        "gear_list": base,
        "num_people": num_people,
        "num_days": num_days,
        "camp_style": camp_style
    }
