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



def draw_background(
    dwg,
    template
):
    """
    Draw poster background.
    """

    dwg.add(
        dwg.rect(
            insert=(0, 0),
            size=(
                template.width,
                template.height
            ),
            fill=template.style.background
        )
    )



def draw_route(
    dwg,
    points,
    template
):
    """
    Draw GPS track.
    """

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



def draw_title(
    dwg,
    config,
    template
):
    """
    Draw poster title.
    """

    dwg.add(
        dwg.text(
            config.title,
            insert=(
                template.title.x,
                template.title.y
            ),
            font_family=template.title.font_family,
            font_size=template.title.font_size,
            font_weight=template.title.font_weight,
            fill=template.title.color,
            text_anchor=template.title.text_anchor
        )
    )



def draw_statistics(
    dwg,
    config,
    template
):
    """
    Draw poster statistics.
    """

    stats = []


    if config.show_distance:
        stats.append(
            config.distance
        )


    if config.show_elevation:
        stats.append(
            config.elevation
        )


    if config.show_duration:
        stats.append(
            config.duration
        )


    if not stats:
        return


    if template.stats.layout == "horizontal":

        total_width = (
            len(stats)
            *
            template.stats.gap
        )

        start_x = (
            template.stats.x
            -
            total_width / 2
        )


        for index, value in enumerate(stats):

            dwg.add(
                dwg.text(
                    value,
                    insert=(
                        start_x
                        +
                        index * template.stats.gap,
                        template.stats.y
                    ),
                    font_family=template.stats.font_family,
                    font_size=template.stats.font_size,
                    font_weight=template.stats.font_weight,
                    fill=template.stats.color,
                    text_anchor=template.stats.text_anchor
                )
            )


    else:

        current_y = template.stats.y

        for value in stats:

            dwg.add(
                dwg.text(
                    value,
                    insert=(
                        template.stats.x,
                        current_y
                    ),
                    font_family=template.stats.font_family,
                    font_size=template.stats.font_size,
                    font_weight=template.stats.font_weight,
                    fill=template.stats.color,
                    text_anchor=template.stats.text_anchor
                )
            )

            current_y += template.stats.gap



def generate_svg(
    points,
    template,
    config,
    output_file
):
    """
    Generate SVG poster.
    """

    dwg = svgwrite.Drawing(
        output_file,
        size=(
            template.width,
            template.height
        )
    )


    draw_background(
        dwg,
        template
    )


    draw_route(
        dwg,
        points,
        template
    )


    draw_title(
        dwg,
        config,
        template
    )


    draw_statistics(
        dwg,
        config,
        template
    )


    dwg.save()