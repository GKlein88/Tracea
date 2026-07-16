from pydantic import BaseModel


class PosterStatistics(BaseModel):
    """
    Raw GPX calculated values.
    """

    original_points: int
    cleaned_points: int
    simplified_points: int
    svg_points: int

    distance_km: float
    elevation_gain_m: int
    duration_seconds: int



class PosterContent(BaseModel):
    """
    Editable content displayed on the poster.
    """

    title: str

    distance_text: str
    elevation_text: str
    duration_text: str

    duration_format: str

    show_distance: bool = True
    show_elevation: bool = True
    show_duration: bool = True



class PosterResponse(BaseModel):

    success: bool

    activity_name: str
    sport: str | None

    svg_url: str

    statistics: PosterStatistics

    content: PosterContent

    template: str