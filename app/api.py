from fastapi import FastAPI
from app.models import TripRequest
from Camping_Guide import run_guide

app = FastAPI(
    title="Camping Planner AI",
    description="AI-powered camping trip planner using CrewAI agents",
    version="1.0.0",
)


@app.post("/plan")
def generate_plan(req: TripRequest):
    """Generate a camping plan using the Camping_Guide orchestrator."""

    result = run_guide(
        location=req.location,
        origin=req.origin,
        num_people=req.num_people,
        num_days=req.num_days,
        camp_style=req.camp_style,
        season=req.season,
        experience_level=req.experience_level,
        json_output=True,  # API always returns JSON
        export_calendar=False,
        export_pdf=False,
    )

    return {"plan": result}
