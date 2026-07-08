import shutil
import tempfile
from pathlib import Path

from fastapi import UploadFile

from app.gpx.parser import parse_gpx
from app.geo.clean import clean_track
from app.geo.simplify import simplify_points
from app.geo.projection import project_points
from app.svg.renderer import generate_svg
from app.utils.files import create_output_filename
from app.geo.statistics import (
    calculate_distance,
    calculate_elevation_gain,
)


async def generate_poster(file: UploadFile):
    """
    Generate an SVG poster from a GPX file.
    """

    temp_path = None

    try:
        # Save uploaded GPX temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".gpx"
        ) as temp_file:
            temp_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # Parse GPX data
        activity = parse_gpx(temp_path)

        track_name = activity.name
        raw_points = activity.points

        # Remove only aberrant points
        cleaned_points = clean_track(
            activity.points
        )

        # Compute statistics
        distance_km = calculate_distance(
            cleaned_points
        )

        elevation_gain_m = calculate_elevation_gain(
            cleaned_points
        )

        # Simplify GPS track
        simplified_points = simplify_points(cleaned_points)

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
                "cleaned_points": len(cleaned_points),
                "simplified_points": len(simplified_points),
                "svg_points": len(svg_points),
                "distance_km": distance_km,
                "elevation_gain_m": elevation_gain_m,
            },
            "poster": {
                "filename": output_file,
            },
        }
    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)
