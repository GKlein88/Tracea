import json
from pathlib import Path

from app.models.poster import PosterTemplate


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / "poster-templates"


def load_template(name: str) -> PosterTemplate:

    template_file = TEMPLATE_DIR / f"{name}.json"

    with open(template_file, "r") as file:
        data = json.load(file)

    return PosterTemplate(**data)