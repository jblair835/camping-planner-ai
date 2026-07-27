def estimate_budget(
    num_days: int,
    num_people: int,
    campsite_fee: float,
    food_cost_per_day: float,
    fuel_cost: float,
) -> str:
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
