def get_packing_suggestions(num_days: int, season: str) -> str:
    """Return packing suggestions based on trip length and season."""
    return (
        f"Packing suggestions for {num_days} days in {season}:\n"
        "- Layered clothing\n"
        "- Extra socks\n"
        "- Warm sleeping gear\n"
        "- Sunscreen & bug spray\n"
        "- Reusable water containers\n"
        "- Personal medications\n"
        "- Weather-appropriate outerwear"
    )
