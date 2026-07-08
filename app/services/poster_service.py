import shutil
import tempfile

from fastapi import UploadFile

from app.gpx.parser import parse_gpx
from app.geo.simplify import simplify_points
from app.geo.projection import project_points
from app.svg.renderer import generate_svg
from app.utils.files import create_output_filename


async def generate_poster(file: UploadFile):
    """
    Generate an SVG poster from a GPX file.
    """

    # Save uploaded GPX temporarily
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".gpx"
    )

    with open(temp_file.name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse GPX data
    activity = parse_gpx(temp_file.name)

    track_name = activity.name
    raw_points = activity.points

    # Simplify GPS track
    simplified_points = simplify_points(raw_points)

    # Convert GPS coordinates to SVG coordinates
    svg_points = project_points(simplified_points)

    # Create output filename
    output_file = create_output_filename(track_name)

    # Generate SVG
    generate_svg(
        points=svg_points,
        output_file=output_file
    )

    return {
        "success": True,
        "track_name": track_name,
        "statistics": {
            "original_points": len(raw_points),
            "simplified_points": len(simplified_points),
            "svg_points": len(svg_points),
        },
        "poster": {
            "filename": output_file,
        },
    }