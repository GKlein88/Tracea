import base64
from pathlib import Path
import svgwrite
from fontTools.ttLib import TTFont


FONT_DIR = (
    Path(__file__).parent.parent
    / "static"
    / "fonts"
    / "Futura"
)


FONTS = [
    ("FuturaPT", "200", "FuturaLT-Light.woff2"),
    ("FuturaPT", "400", "FuturaLT.woff2"),
    ("FuturaPT", "600", "FuturaLT-Heavy.woff2"),
    ("FuturaPT", "700", "FuturaLT-Bold.woff2"),
    ("FuturaPT", "800", "FuturaLT-ExtraBold.woff2"),

    ("FuturaPT Condensed", "200", "FuturaLT-CondensedLight.woff2"),
    ("FuturaPT Condensed", "400", "FuturaLT-Condensed.woff2"),
    ("FuturaPT Condensed", "700", "FuturaLT-CondensedBold.woff2"),
    ("FuturaPT Condensed", "800", "FuturaLT-CondensedExtraBold.woff2"),
]


def get_font_path(
    family,
    weight
):
    """
    Find font file matching family and weight.
    """

    for font_family, font_weight, filename in FONTS:

        if (
            font_family == family
            and int(font_weight) == int(weight)
        ):
            return FONT_DIR / filename

    raise ValueError(
        f"Font not found: {family} {weight}"
    )
    


def measure_text_width(
    text,
    font_path,
    font_size
):
    """
    Measure text width using real font metrics.
    """

    font = TTFont(font_path)

    cmap = font.getBestCmap()
    hmtx = font["hmtx"]

    units_per_em = font["head"].unitsPerEm

    width = 0

    for char in text:

        glyph_name = cmap.get(
            ord(char)
        )

        if glyph_name:
            advance, _ = hmtx[glyph_name]
            width += advance

    return (width / units_per_em * font_size)


def embed_fonts(dwg):
    """
    Embed Futura fonts inside SVG.
    """

    css = ""

    for family, weight, filename in FONTS:

        font_path = FONT_DIR / filename

        font_data = base64.b64encode(
            font_path.read_bytes()
        ).decode("utf-8")

        css += f"""
        @font-face {{
            font-family: "{family}";
            src: url(data:font/woff2;base64,{font_data})
            format("woff2");
            font-weight: {weight};
            font-style: normal;
        }}
        """

    dwg.defs.add(
        dwg.style(css)
    )
    
      

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


def fit_text_size(
    text,
    max_width,
    font_path,
    font_size
):
    """
    Reduce font size until text fits.
    """

    while (
        measure_text_width(
            text,
            font_path,
            font_size
        )
        > max_width
        and font_size > 20
    ):
        font_size -= 2

    return font_size


def split_title(
    text,
    max_width,
    font_path,
    font_size
):
    """
    Split title according to real text width.
    """

    words = text.split(" ")

    lines = []
    current = ""

    for word in words:

        test = (
            f"{current} {word}"
            if current
            else word
        )

        width = measure_text_width(
            test,
            font_path,
            font_size
        )

        if width <= max_width:
            current = test

        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


def draw_title(
    dwg,
    config,
    template
):
    """
    Draw poster title.
    """

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

    if len(lines) > 1:

        max_line_width = max(
            measure_text_width(
                line,
                font_path,
                font_size
            )
            for line in lines
        )

        while (
            max_line_width > template.title.max_width
            and font_size > 20
        ):
            font_size -= 2

            max_line_width = max(
                measure_text_width(
                    line,
                    font_path,
                    font_size
                )
                for line in lines
            )

    title = dwg.text(
    "",
        insert=(
            template.title.x,
            template.title.y
        ),
        dominant_baseline="hanging",
        font_family=template.title.font_family,
        font_size=font_size,
        font_weight=template.title.font_weight,
        fill=template.title.color,
        text_anchor=template.title.text_anchor
    )

    for index, line in enumerate(lines):

        title.add(
            dwg.tspan(
                line,
                x=[
                    template.title.x
                ],
                dy=[
                    0
                    if index == 0
                    else template.title.line_height
                ]
            )
        )

    dwg.add(title)
    


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
    
    embed_fonts(dwg)


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