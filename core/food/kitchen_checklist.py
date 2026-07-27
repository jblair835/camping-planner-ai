def get_kitchen_checklist(style: str) -> str:
    """Provide a camp kitchen checklist based on camping style."""

    base_items = [
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

    extras: list[str] = []
    style_key = style.lower()

    if style_key in ["rv", "cabin", "luxury"]:
        extras.extend(["Electric skillet", "Coffee maker", "Extra storage bins"])
    elif style_key == "backpacking":
        extras.extend(["Lightweight pot", "Titanium spork", "Compact stove"])

    checklist_lines = [f"Camp Kitchen Checklist ({style} style):"]
    checklist_lines.extend(f"- {item}" for item in base_items + extras)

    return "\n".join(checklist_lines)
