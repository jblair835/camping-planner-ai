def get_weather_risks(location: str, season: str) -> str:
    """Return weather risk guidance."""
    return (
        f"Weather risks for {location} in {season}:\n"
        "- Sudden temperature drops at night\n"
        "- Afternoon thunderstorms possible\n"
        "- High UV exposure\n"
        "- Rapid weather changes in mountain areas\n"
        "- Check updated forecasts frequently"
    )
