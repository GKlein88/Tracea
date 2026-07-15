from pydantic import BaseModel


class RouteArea(BaseModel):
    width: int
    height: int
    offset_x: int = 0
    offset_y: int = 0
    padding: int = 50


class PosterStyle(BaseModel):
    background: str
    route_color: str
    stroke_width: int


class StatsConfig(BaseModel):
    show_distance: bool = True
    show_elevation: bool = True
    show_duration: bool = True

    duration_format: str = "hms"


class PosterTemplate(BaseModel):
    name: str
    width: int
    height: int

    route_area: RouteArea
    style: PosterStyle
    stats: StatsConfig