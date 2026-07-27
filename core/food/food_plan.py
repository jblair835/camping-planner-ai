def generate_food_plan(num_days: int, num_people: int, style: str) -> str:
    """Generate a simple food plan summary."""

    return (
        f"Food Plan:\n"
        f"- {num_days} days of meals\n"
        f"- {num_people} people\n"
        f"- Style: {style}\n"
        f"- Includes breakfast, lunch, dinner, and snacks\n"
        f"- Uses selected meals and grocery list"
    )
