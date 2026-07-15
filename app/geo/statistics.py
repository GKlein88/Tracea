from math import atan2, cos, radians, sin, sqrt
from datetime import timedelta

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

    total = 0.0

    for i in range(1, len(points)):
        segment = haversine_distance(
            points[i - 1],
            points[i],
        )

        total += segment

    return round(total, 1)


def calculate_elevation_gain(
    points: list[GPSPoint],
) -> int:
    """
    Calculate total positive elevation gain.
    Points are expected to have already been smoothed.
    """

    if len(points) < 2:
        return 0

    gain = 0.0

    previous = points[0].ele

    if previous is None:
        return 0

    for point in points[1:]:
        if point.ele is None:
            continue

        delta = point.ele - previous

        if delta > 0:
            gain += delta

        previous = point.ele

    return round(gain)


def calculate_duration(
    points: list[GPSPoint]
) -> int:
    """
    Calculate activity duration in seconds.
    """

    timestamps = [
        point.timestamp
        for point in points
        if point.timestamp
    ]

    if len(timestamps) < 2:
        return 0

    duration = (
        max(timestamps)
        - min(timestamps)
    )

    return int(duration.total_seconds())