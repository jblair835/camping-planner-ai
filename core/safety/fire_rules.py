def get_fire_rules(location_hint: str) -> str:
    """Provide general campfire rules for a given area hint."""

    return (
        f"Fire rules near {location_hint}:\n"
        "- Check current fire restrictions and local regulations.\n"
        "- Use designated fire rings where available.\n"
        "- Keep fires small and manageable.\n"
        "- Never leave a fire unattended.\n"
        "- Fully extinguish the fire before leaving (drown, stir, feel)."
    )
