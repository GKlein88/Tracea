import re


def create_output_filename(name: str):
    """
    Create a filesystem-safe filename while preserving the original name.
    """

    safe_name = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        name
    )

    return f"outputs/{safe_name}.svg"