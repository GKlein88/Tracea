from .fonts import (
    get_font_path,
    measure_text_width
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

    if template.stats.layout == "positions":

        count = len(stats)

        if count == 3:
            positions = [
                template.stats.positions.left,
                template.stats.positions.center,
                template.stats.positions.right
            ]

        elif count == 2:
            positions = [
                template.stats.side_margin_two,
                template.width - template.stats.side_margin_two
            ]

        else:
            positions = [
                template.stats.x
            ]

        for index, value in enumerate(stats):

            dwg.add(
                dwg.text(
                    value,
                    insert=(
                        positions[index],
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