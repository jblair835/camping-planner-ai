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
