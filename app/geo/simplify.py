from shapely.geometry import LineString

from app.geo.statistics import haversine_distance
from app.models.activity import GPSPoint


def _remove_visually_close_points(
    points: list[GPSPoint],
    min_distance_m: float
) -> list[GPSPoint]:
    if not points:
        return []

    simplified = [points[0]]

    for point in points[1:]:
        distance = haversine_distance(simplified[-1], point)

        if distance * 1000 < min_distance_m:
            continue

        simplified.append(point)

    return simplified


def simplify_points(
    points: list[GPSPoint],
    tolerance: float = 0.00001,
    min_distance_m: float = 5
) -> list[GPSPoint]:
    """
    Simplify a GPS track for visual rendering.
    """

    visually_reduced_points = _remove_visually_close_points(
        points=points,
        min_distance_m=min_distance_m
    )

    if len(visually_reduced_points) < 3:
        return visually_reduced_points

    line = LineString(
        [
            (point.lon, point.lat)
            for point in visually_reduced_points
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
