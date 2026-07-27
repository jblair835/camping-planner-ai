import argparse
from Camping_Guide import run_guide


def main():
    parser = argparse.ArgumentParser(description="Camping Planner AI CLI")
    parser.add_argument("--json", action="store_true", help="Output plan as JSON")
    parser.add_argument("--calendar", action="store_true", help="Export calendar events to .ics")
    parser.add_argument("--pdf", action="store_true", help="Export trip report as PDF")
    args = parser.parse_args()

    print("=== Camping Planner AI ===")

    location = input("Where do you want to camp? ")
    origin = input("Where are you driving from? ")
    num_people = int(input("How many people? "))
    num_days = int(input("How many days? "))
    camp_style = input("Camping style (tent, RV, cabin, backpacking)? ")
    season = input("Season or month? ")
    experience_level = input("Experience level? ")

    result = run_guide(
        location=location,
        origin=origin,
        num_people=num_people,
        num_days=num_days,
        camp_style=camp_style,
        season=season,
        experience_level=experience_level,
        json_output=args.json,
        export_calendar=args.calendar,
        export_pdf=args.pdf,
    )

    print("\n\n===== CAMPING PLAN OUTPUT =====\n")
    print(result)


if __name__ == "__main__":
    main()
