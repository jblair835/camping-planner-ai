def get_camping_gear_list(style: str, num_people: int) -> str:
    """Return a basic gear list based on camping style."""

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

    if style.lower() == "rv":
        base.extend(["RV hookups", "Extension cords", "Leveling blocks"])

    if style.lower() == "backpacking":
        base.extend(["Ultralight tent", "Compact stove", "Water filter"])

    return "Gear List:\n" + "\n".join(f"- {item}" for item in base)
