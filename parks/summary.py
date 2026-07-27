def park_summary(park_name: str) -> str:
    """Fetch a summary for a park or campground using Wikipedia API."""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{park_name.replace(' ', '_')}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("extract", "No summary available.")
    except Exception as e:
        return f"Error fetching park summary: {e}"