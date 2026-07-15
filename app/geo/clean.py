from app.geo.statistics import haversine_distance
from app.models.activity import GPSPoint
from app.geo.config import GeoConfig



def _segment_is_aberrant(
    point1: GPSPoint,
    point2: GPSPoint,
    config: GeoConfig,
) -> bool:
    distance_km = haversine_distance(point1, point2)
    
    MIN_SEGMENT_DISTANCE_KM = config.min_segment_distance_km
    MAX_JUMP_WITHOUT_TIME_KM = config.max_jump_without_time_km
    MAX_SPEED_KMH = config.max_speed_kmh

    if distance_km < MIN_SEGMENT_DISTANCE_KM:
            return False

    if point1.timestamp is None or point2.timestamp is None:
        return distance_km > MAX_JUMP_WITHOUT_TIME_KM

    elapsed_hours = abs(
        (point2.timestamp - point1.timestamp).total_seconds()
    ) / 3600

    if elapsed_hours == 0:
        return distance_km > 0

    return distance_km / elapsed_hours > MAX_SPEED_KMH


def clean_track(
    points: list[GPSPoint],
    config: GeoConfig,
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
            config
        )
        next_segment_aberrant = _segment_is_aberrant(
            point,
            next_point,
            config
        )
        bypass_segment_aberrant = _segment_is_aberrant(
            previous_point,
            next_point,
            config
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
    config: GeoConfig,
) -> list[GPSPoint]:
    """
    Backward-compatible name for GPS point cleaning.
    """

    return clean_track(
        points=points,
        config=config,
    )
