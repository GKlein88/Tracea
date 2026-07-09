from pydantic import BaseModel


class PosterStatistics(BaseModel):
    original_points: int
    cleaned_points: int
    simplified_points: int
    svg_points: int
    distance_km: float
    elevation_gain_m: int


class PosterFile(BaseModel):
    filename: str


class PosterResponse(BaseModel):
    success: bool
    activity_name: str
    sport: str
    svg_url: str
    statistics: PosterStatistics