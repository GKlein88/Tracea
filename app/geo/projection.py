from pyproj import Transformer
from app.models.activity import GPSPoint


def project_points(points: list[GPSPoint], width=800, height=800, padding=80):
    """
    Convert GPS coordinates into SVG coordinates
    while preserving geographic proportions.
    """

    if not points:
        return []

    # WGS84 GPS coordinates -> Web Mercator meters
    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:3857",
        always_xy=True
    )

    projected = []

    for point in points:
        x, y = transformer.transform(
            point.lon,
            point.lat
        )

        projected.append(
            {
                "x": x,
                "y": y
            }
        )

    xs = [p["x"] for p in projected]
    ys = [p["y"] for p in projected]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    range_x = max_x - min_x
    range_y = max_y - min_y

    scale = min(
        (width - 2 * padding) / range_x,
        (height - 2 * padding) / range_y
    )

    svg_points = []

    for point in projected:

        svg_x = (
            (point["x"] - min_x) * scale
            + padding
        )

        # SVG Y axis goes downward
        svg_y = (
            height
            - (
                (point["y"] - min_y) * scale
                + padding
            )
        )

        svg_points.append(
            {
                "x": round(svg_x, 2),
                "y": round(svg_y, 2)
            }
        )

    return svg_points   