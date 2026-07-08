import re
from pathlib import Path


OUTPUT_DIR = Path("outputs")


def create_output_filename(name: str):
    """
    Create a filesystem-safe filename while preserving the original name.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        name
    ).strip()

    if not safe_name:
        safe_name = "poster"

    return str(OUTPUT_DIR / f"{safe_name}.svg")
