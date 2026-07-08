from math import atan2, cos, radians, sin, sqrt

from app.models.activity import GPSPoint


EARTH_RADIUS_KM = 6371.0088


def haversine_distance(
    point1: GPSPoint,
    point2: GPSPoint,
) -> float:
    """
    Calculate the geodesic distance between two GPS points in kilometers.
    """

    lat1 = radians(point1.lat)
    lon1 = radians(point1.lon)

    lat2 = radians(point2.lat)
    lon2 = radians(point2.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def calculate_distance(
    points: list[GPSPoint],
) -> float:
    """
    Calculate the total activity distance in kilometers.
    """

    if len(points) < 2:
        return 0.0

    total = sum(
        haversine_distance(points[i - 1], points[i])
        for i in range(1, len(points))
    )

    return round(total, 2)


def calculate_elevation_gain(
    points: list[GPSPoint],
    threshold: float = 3.0,
) -> int:
    """
    Calculate positive elevation gain.

    Small altitude variations below the threshold are ignored to reduce
    GPS noise.
    """

    if len(points) < 2:
        return 0

    gain = 0.0
    previous = points[0].ele or 0.0

    for point in points[1:]:
        current = point.ele or previous
        delta = current - previous

        if delta >= threshold:
            gain += delta

        previous = current

    return round(gain)