from shapely.geometry import LineString
from app.models.activity import GPSPoint


def simplify_points(points, tolerance=0.00001):
    """
    Simplify a GPS track while preserving its overall shape.
    """

    if len(points) < 3:
        return points

    line = LineString(
        [
            (point.lon, point.lat)
            for point in points
        ]
    )

    simplified = line.simplify(
        tolerance=tolerance,
        preserve_topology=False
    )

    return [
        GPSPoint(
            lat=lat,
            lon=lon,
            ele=None
        )
        for lon, lat in simplified.coords
    ]