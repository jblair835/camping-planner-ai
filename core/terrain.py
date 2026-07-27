def terrain_info(location_hint: str) -> str:
    """Describe typical terrain for camping in the area."""
    return (
        f"Terrain around {location_hint}: "
        "Could include forests, hills, rivers, or desert. Check specific park maps for details."
    )