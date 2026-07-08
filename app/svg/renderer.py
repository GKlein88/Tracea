import svgwrite


def create_path(points):
    """
    Convert SVG coordinates into an SVG path command.
    """

    if not points:
        return ""

    path = f"M {points[0]['x']} {points[0]['y']} "

    for point in points[1:]:
        path += f"L {point['x']} {point['y']} "

    return path.strip()


def generate_svg(
    points,
    output_file,
    width=800,
    height=800
):
    """
    Generate an SVG file containing the GPS track.
    """

    dwg = svgwrite.Drawing(
        output_file,
        size=(width, height)
    )

    # Add background
    dwg.add(
        dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill="white"
        )
    )

    # Create GPS track path
    path_data = create_path(points)

    if path_data:
        dwg.add(
            dwg.path(
                d=path_data,
                fill="none",
                stroke="black",
                stroke_width=4
            )
        )

    dwg.save()
