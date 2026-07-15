from pyproj import Transformer

from app.models.activity import GPSPoint


def project_points(
    points: list[GPSPoint],
    route_area: dict
):
    """
    Convert GPS coordinates into SVG coordinates.

    The route is:
    - projected from WGS84 to Web Mercator
    - scaled proportionally
    - centered inside the provided route area

    The function is independent from the poster design.
    It only positions the route inside the given area.
    """

    if not points:
        return []


    # Extract route area configuration
    area_width = route_area.width
    area_height = route_area.height
    offset_x = route_area.offset_x
    offset_y = route_area.offset_y
    padding = route_area.padding

    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:3857",
        always_xy=True
    )


    # Project GPS coordinates
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


    # Single GPS point
    if range_x == 0 and range_y == 0:
        return [
            {
                "x": offset_x + area_width / 2,
                "y": offset_y + area_height / 2
            }
        ]


    # Available drawing space
    available_width = area_width - (2 * padding)
    available_height = area_height - (2 * padding)


    scale_x = (
        available_width / range_x
        if range_x
        else float("inf")
    )

    scale_y = (
        available_height / range_y
        if range_y
        else float("inf")
    )


    scale = min(
        scale_x,
        scale_y
    )


    # Final route dimensions
    scaled_width = range_x * scale
    scaled_height = range_y * scale


    # Center route inside the drawing area
    margin_x = (
        area_width - scaled_width
    ) / 2

    margin_y = (
        area_height - scaled_height
    ) / 2


    svg_points = []


    for point in projected:

        svg_x = (
            (point["x"] - min_x)
            * scale
            + offset_x
            + margin_x
        )


        # SVG Y axis goes downward
        svg_y = (
            offset_y
            + margin_y
            + scaled_height
            - (
                (point["y"] - min_y)
                * scale
            )
        )


        svg_points.append(
            {
                "x": round(svg_x, 2),
                "y": round(svg_y, 2)
            }
        )


    return svg_points