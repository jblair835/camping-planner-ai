def best_season_to_camp(location_hint: str, season_hint: str = "") -> str:
    """Suggest the best season to camp."""
    base = (
        f"Best seasons to camp near {location_hint}: "
        "Typically spring and fall for comfortable temperatures and fewer bugs."
    )
    if season_hint:
        return base + f" You mentioned {season_hint}; verify local conditions for that time."
    return base
