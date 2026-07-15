import svgwrite


def create_path(points):
    """
    Convert SVG coordinates into an SVG path command.
    """

    if not points:
        return ""

    path = (
        f"M {points[0]['x']} {points[0]['y']} "
    )

    for point in points[1:]:
        path += (
            f"L {point['x']} {point['y']} "
        )

    return path.strip()


def generate_svg(
    points,
    output_file,
    width,
    height,
    background,
    route_color,
    stroke_width
):
    """
    Generate an SVG poster containing the GPS track.est-ce q
    """

    dwg = svgwrite.Drawing(
        output_file,
        size=(width, height)
    )

    # Background
    dwg.add(
        dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill=background
        )
    )


    # GPS track
    path_data = create_path(points)

    if path_data:
        dwg.add(
            dwg.path(
                d=path_data,
                fill="none",
                stroke=route_color,
                stroke_width=stroke_width,
                stroke_linecap="round",
                stroke_linejoin="round"
            )
        )


    dwg.save()