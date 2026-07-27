import random
from meals.simple import SIMPLE_MEALS
from meals.gourmet import GOURMET_MEALS
from meals.backpacking import BACKPACKING_MEALS
from meals.barfood import BARFOOD_MEALS


def select_meals(num_days: int, style: str) -> str:
    """Select camping meals for a given number of days and camping style."""

    style_key = style.lower()

    if style_key in ["luxury", "rv", "cabin"]:
        meals = GOURMET_MEALS
    elif style_key == "backpacking":
        meals = BACKPACKING_MEALS
    elif style_key in ["barfood", "pub", "bar"]:
        meals = BARFOOD_MEALS
    else:
        meals = SIMPLE_MEALS

    lines = [f"Selected meals for {num_days} days ({style} style):", ""]

    for day in range(1, num_days + 1):
        lines.append(f"Day {day}:")
        lines.append(f"- Breakfast: {random.choice(meals['breakfast'])}")
        lines.append(f"- Lunch: {random.choice(meals['lunch'])}")
        lines.append(f"- Dinner: {random.choice(meals['dinner'])}")
        lines.append("")

    return "\n".join(lines)
