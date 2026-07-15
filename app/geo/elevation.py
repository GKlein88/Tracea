from statistics import median
from app.models.activity import GPSPoint
from app.geo.config import GeoConfig

def smooth_elevation(
    points: list[GPSPoint],
    config: GeoConfig
) -> list[GPSPoint]:

    if len(points) < 5:
        return points

    smoothed = []
    window = config.elevation_smoothing_window

    for i, point in enumerate(points):
        start = max(0, i - window)
        end = min(len(points), i + window + 1)

        values = [
            p.elevation
            for p in points[start:end]
            if p.elevation is not None
        ]

        if values:
            elevation = median(values)
            smoothed.append(
                point.model_copy(
                    update={"ele": elevation}
                )
            )
        else:
            smoothed.append(point)

    return smoothed