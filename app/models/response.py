from pydantic import BaseModel


class PosterStatistics(BaseModel):
    original_points: int
    simplified_points: int
    svg_points: int


class PosterFile(BaseModel):
    filename: str


class PosterResponse(BaseModel):
    success: bool
    track_name: str
    statistics: PosterStatistics
    poster: PosterFile