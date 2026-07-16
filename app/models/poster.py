from pydantic import BaseModel


class RouteArea(BaseModel):
    width: int
    height: int
    offset_x: int = 0
    offset_y: int = 0
    padding: int = 0


class PosterStyle(BaseModel):
    background: str
    route_color: str
    stroke_width: int


class TitleStyle(BaseModel):
    x: int
    y: int
    font_family: str
    font_size: int
    font_weight: str
    color: str
    text_anchor: str = "middle"


class StatsStyle(BaseModel):
    x: int
    y: int
    font_family: str
    font_size: int
    font_weight: str
    color: str
    gap: int = 20
    text_anchor: str = "middle"
    layout: str = "horizontal"


class PosterTemplate(BaseModel):
    name: str

    width: int
    height: int

    route_area: RouteArea

    style: PosterStyle

    title: TitleStyle
    stats: StatsStyle



class PosterConfig(BaseModel):
    """
    Editable poster content.
    This is what the frontend editor will modify.
    """

    title: str

    distance: str
    elevation: str
    duration: str

    duration_format: str = "prime"

    show_distance: bool = True
    show_elevation: bool = True
    show_duration: bool = True