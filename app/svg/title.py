from .fonts import (
    get_font_path,
    measure_text_width
)


def split_title(text, max_width, font_path, font_size):

    words = text.split(" ")

    lines = []
    current = ""

    for word in words:

        test = (
            f"{current} {word}"
            if current
            else word
        )

        if (measure_text_width(test, font_path, font_size) <= max_width):
            current = test
        else:
            if current:
                lines.append(current)
            current = word
            
    if current:
        lines.append(current)

    return lines



def draw_title(dwg, config, template):

    font_path = get_font_path(
        template.title.font_family,
        template.title.font_weight
    )

    font_size = template.title.font_size

    lines = split_title(
        config.title,
        template.title.max_width,
        font_path,
        font_size
    )

    title = dwg.text(
        "",
        id="poster-title",
        insert=(
            template.title.x,
            template.title.y
        ),
        dominant_baseline="hanging",
        font_family=template.title.font_family,
        font_size=font_size,
        font_weight=template.title.font_weight,
        fill=template.title.color,
        text_anchor=template.title.text_anchor,
        class_=f"line-height-{template.title.line_height} max-width-{template.title.max_width}"
    )

    for index, line in enumerate(lines):

        title.add(
            dwg.tspan(
                line,
                x=[template.title.x],
                dy=[
                    0
                    if index == 0
                    else template.title.line_height
                ]
            )
        )

    dwg.add(title)