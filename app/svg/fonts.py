import base64
from pathlib import Path
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


def get_font_path(family, weight):
    for font_family, font_weight, filename in FONTS:

        if (
            font_family == family
            and int(font_weight) == int(weight)
        ):
            return FONT_DIR / filename

    raise ValueError(
        f"Font not found: {family} {weight}"
    )


def measure_text_width(text, font_path, font_size):

    font = TTFont(font_path)

    cmap = font.getBestCmap()
    hmtx = font["hmtx"]

    units_per_em = font["head"].unitsPerEm

    width = 0

    for char in text:

        glyph_name = cmap.get(ord(char))

        if glyph_name:
            advance, _ = hmtx[glyph_name]
            width += advance

    return width / units_per_em * font_size


def embed_fonts(dwg):

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