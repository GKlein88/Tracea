from pydantic import BaseModel


class GPSPoint(BaseModel):
    lat: float
    lon: float
    ele: float | None = None


class Activity(BaseModel):
    name: str
    points: list[GPSPoint]