from pydantic import BaseModel


class PosterStatistics(BaseModel):
    original_points: int
    cleaned_points: int
    simplified_points: int
    svg_points: int

    distance_km: float
    elevation_gain_m: int
    duration_seconds: int


class PosterResponse(BaseModel):
    success: bool
    activity_name: str
    sport: str | None
    svg_url: str
    statistics: PosterStatistics