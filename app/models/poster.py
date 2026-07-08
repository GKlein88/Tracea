from pydantic import BaseModel

from app.models.activity import GPSPoint


class PosterStats(BaseModel):
    distance_km: float
    elevation_gain_m: float


class Poster(BaseModel):
    title: str
    stats: PosterStats
    track: list[GPSPoint]