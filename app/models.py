from pydantic import BaseModel


class TripRequest(BaseModel):
    location: str
    origin: str
    num_people: int
    num_days: int
    camp_style: str
    season: str
    experience_level: str
