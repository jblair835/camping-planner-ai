def koa_info(location_hint: str) -> str:
    """Provide generic KOA campground info based on a region."""
    return (
        f"KOA campgrounds near {location_hint}: "
        "Expect RV sites, tent sites, cabins, restrooms, showers, and family-friendly amenities."
    )