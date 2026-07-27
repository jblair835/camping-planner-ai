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
