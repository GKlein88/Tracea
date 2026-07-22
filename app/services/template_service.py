import json
from pathlib import Path

from app.models.poster import PosterTemplate


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / "static/poster-templates"


def load_template(name: str) -> PosterTemplate:
    """
    Load a poster template configuration.
    """

    template_file = TEMPLATE_DIR / f"{name}.json"

    if not template_file.exists():
        raise FileNotFoundError(
            f"Template '{name}' not found"
        )

    with open(
        template_file,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    return PosterTemplate(**data)