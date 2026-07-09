import gpxpy
from app.models.activity import Activity, GPSPoint


def parse_gpx(file_path: str):
    """
    Parse a GPX file and return track metadata and GPS points.
    """

    with open(file_path, "r", encoding="utf-8") as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    points = []

    track_name = None
    track_type = None

    # Try to get the track name
    if gpx.tracks:
        track = gpx.tracks[0]
        track_name = track.name
        if hasattr(track, "type") and track.type:
            track_type = track.type.lower()

    # Fallback to metadata name
    if not track_name and gpx.name:
        track_name = gpx.name

    # Extract all GPS points
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(
                    {
                        "lat": point.latitude,
                        "lon": point.longitude,
                        "ele": point.elevation,
                        "time": point.time
                    }
                )

    return Activity(
        name=track_name or "Untitled",
        sport=track_type,
        points=[
            GPSPoint(**point)
            for point in points
        ]
    )