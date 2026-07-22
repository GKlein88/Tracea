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
    font_weight: int
    color: str
    text_anchor: str = "middle"
    max_width: int
    max_lines: int
    line_height: int


class StatsPositions2(BaseModel):
    left: int
    right: int


class StatsPositions3(BaseModel):
    left: int
    center: int
    right: int


class StatsAnchor2(BaseModel):
    left: str = "start"
    right: str = "end"


class StatsAnchor3(BaseModel):
    left: str = "start"
    center: str = "middle"
    right: str = "end"


class StatsStyle(BaseModel):
    layout: str
    y: int
    font_family: str
    font_size: int
    font_weight: int
    duration_format: str = "prime"
    color: str

    positions2: StatsPositions2 | None = None
    text_anchors2: StatsAnchor2 | None = None
    positions3: StatsPositions3 | None = None
    text_anchors3: StatsAnchor3 | None = None
    
    

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
    """
    title: str
    distance_text: str
    elevation_text: str
    duration_text: str

    duration_hours: int = 0
    duration_minutes: int = 0
    duration_seconds: int = 0
    duration_format: str = "clock"

    show_distance: bool = True
    show_elevation: bool = True
    show_duration: bool = True