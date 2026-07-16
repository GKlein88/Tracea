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
                template.stats.positions3.left,
                template.stats.positions3.center,
                template.stats.positions3.right
            ]
            anchors = [
                template.stats.text_anchors3.left,
                template.stats.text_anchors3.center,
                template.stats.text_anchors3.right
            ]

        elif count == 2:
            positions = [
                template.stats.positions2.left,
                template.stats.positions2.right
            ]
            anchors = [
                template.stats.text_anchors2.left,
                template.stats.text_anchors2.right
            ]

        for index, value in enumerate(stats):

            dwg.add(
                dwg.text(
                    value,
                    insert=(
                        positions[index],
                        template.stats.y
                    ),
                    dominant_baseline="hanging",
                    font_family=template.stats.font_family,
                    font_size=template.stats.font_size,
                    font_weight=template.stats.font_weight,
                    fill=template.stats.color,
                    text_anchor=anchors[index]
                )
            )