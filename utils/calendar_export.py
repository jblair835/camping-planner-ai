def export_to_ics(events: list[dict], filename: str = "camping_plan.ics"):
    """Export a list of events to a simple .ics file (stub)."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\nVERSION:2.0\n")
        for event in events:
            f.write("BEGIN:VEVENT\n")
            f.write(f"SUMMARY:{event.get('title', 'Camping Event')}\n")
            f.write(f"DESCRIPTION:{event.get('description', '')}\n")
            f.write("END:VEVENT\n")
        f.write("END:VCALENDAR\n")
