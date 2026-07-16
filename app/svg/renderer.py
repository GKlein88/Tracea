import svgwrite

from .fonts import embed_fonts
from .background import draw_background
from .route import draw_route
from .text import draw_title
from .stats import draw_statistics



def generate_svg(
    points,
    template,
    config,
    output_file
):

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