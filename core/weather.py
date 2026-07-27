def get_weather_forecast(location: str, season: str) -> str:
    """Return a simple weather forecast summary."""
    return (
        f"Weather forecast for {location} in {season}:\n"
        "- Mild daytime temperatures\n"
        "- Cool nights\n"
        "- Low chance of rain\n"
        "- Light winds\n"
        "- Check updated forecasts before departure"
    )
