def create_path(points):

    if not points:
        return ""

    path = f"M {points[0]['x']} {points[0]['y']} "

    for point in points[1:]:
        path += f"L {point['x']} {point['y']} "

    return path.strip()



def draw_route(dwg, points, template):

    path_data = create_path(points)

    if not path_data:
        return

    dwg.add(
        dwg.path(
            d=path_data,
            fill="none",
            stroke=template.style.route_color,
            stroke_width=template.style.stroke_width,
            stroke_linecap="round",
            stroke_linejoin="round"
        )
    )