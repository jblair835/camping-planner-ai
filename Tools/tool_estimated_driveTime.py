def estimated_drive_time(distance_hint: str) -> str:
    """Provide a rough drive time description."""
    return (
        f"Drive time based on {distance_hint}: "
        "Plan for rest stops, fuel, and possible traffic."
    )
    