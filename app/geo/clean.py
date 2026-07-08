from app.geo.statistics import haversine_distance
from app.models.activity import GPSPoint


DEFAULT_MAX_SPEED_KMH = 150
DEFAULT_MAX_JUMP_WITHOUT_TIME_KM = 2


def _segment_is_aberrant(
    point1: GPSPoint,
    point2: GPSPoint,
    max_speed_kmh: float,
    max_jump_without_time_km: float
) -> bool:
    distance_km = haversine_distance(point1, point2)

    if point1.time is None or point2.time is None:
        return distance_km > max_jump_without_time_km

    elapsed_hours = abs(
        (point2.time - point1.time).total_seconds()
    ) / 3600

    if elapsed_hours == 0:
        return distance_km > 0

    return distance_km / elapsed_hours > max_speed_kmh


def clean_track(
    points: list[GPSPoint],
    max_speed_kmh: float = DEFAULT_MAX_SPEED_KMH,
    max_jump_without_time_km: float = DEFAULT_MAX_JUMP_WITHOUT_TIME_KM
) -> list[GPSPoint]:
    """
    Remove isolated aberrant GPS points while preserving real track detail.
    """

    if not points:
        return []

    if len(points) < 3:
        return points

    cleaned: list[GPSPoint] = []

    for index, point in enumerate(points):
        if index == 0:
            cleaned.append(point)
            continue

        if index == len(points) - 1:
            cleaned.append(point)
            continue

        previous_point = points[index - 1]
        next_point = points[index + 1]

        previous_segment_aberrant = _segment_is_aberrant(
            previous_point,
            point,
            max_speed_kmh,
            max_jump_without_time_km
        )
        next_segment_aberrant = _segment_is_aberrant(
            point,
            next_point,
            max_speed_kmh,
            max_jump_without_time_km
        )
        bypass_segment_aberrant = _segment_is_aberrant(
            previous_point,
            next_point,
            max_speed_kmh,
            max_jump_without_time_km
        )

        if (
            previous_segment_aberrant
            and next_segment_aberrant
            and not bypass_segment_aberrant
        ):
            continue

        cleaned.append(point)

    return cleaned


def clean_points(
    points: list[GPSPoint],
    max_speed_kmh: float = DEFAULT_MAX_SPEED_KMH,
    max_jump_without_time_km: float = DEFAULT_MAX_JUMP_WITHOUT_TIME_KM
) -> list[GPSPoint]:
    """
    Backward-compatible name for GPS point cleaning.
    """

    return clean_track(
        points=points,
        max_speed_kmh=max_speed_kmh,
        max_jump_without_time_km=max_jump_without_time_km
    )
