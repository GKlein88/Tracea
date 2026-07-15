from pydantic import BaseModel
from datetime import datetime


class GPSPoint(BaseModel):
    lat: float
    lon: float
    elevation: float | None = None
    timestamp: datetime | None = None


class Activity(BaseModel):
    name: str
    sport: str | None = None
    points: list[GPSPoint]

    distance_km: float | None = None
    elevation_gain_m: int | None = None
    duration_seconds: int | None = None