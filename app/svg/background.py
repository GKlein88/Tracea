def draw_background(dwg, template):

    dwg.add(
        dwg.rect(
            insert=(0,0),
            size=(
                template.width,
                template.height
            ),
            fill=template.style.background
        )
    )