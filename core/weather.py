def camp_weather(location_hint: str) -> str:
    """Return a simple camping weather summary."""
    sample_weather = [
        "Cool nights, warm days.",
        "Hot and dry during the day, cooler at night.",
        "Chilly and possibly rainy.",
        "Mild temperatures with occasional wind.",
        "Cold nights, moderate days.",
        "Variable weather—pack layers."
    ]
    return f"Camping weather near {location_hint}: {random.choice(sample_weather)}"