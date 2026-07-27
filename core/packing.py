def packing_suggestions_camping(style: str, season_hint: str, experience: str) -> str:
    """Provide packing suggestions based on camping style, season, and experience."""
    base = "Pack layers, sturdy footwear, and weather-appropriate clothing."
    if "summer" in season_hint.lower():
        base += " Include sun protection, bug spray, and light breathable fabrics."
    if "winter" in season_hint.lower() or "cold" in season_hint.lower():
        base += " Include thermal layers, hats, gloves, and insulated boots."
    if style.lower() == "backpacking":
        base += " Focus on lightweight, compact gear."
    if experience.lower() == "beginner":
        base += " Double-check essentials: shelter, warmth, food, water, navigation, and first-aid."
    return base