import shutil
import tempfile
from pathlib import Path

from fastapi import UploadFile

from app.gpx.parser import parse_gpx

from app.geo.config import SPORT_CONFIGS
from app.geo.clean import clean_track
from app.geo.simplify import simplify_points
from app.geo.projection import project_points
from app.geo.elevation import smooth_elevation
from app.geo.statistics import (
    calculate_distance,
    calculate_elevation_gain,
    calculate_duration,
)

from app.svg.renderer import generate_svg

from app.utils.files import create_output_filename
from app.utils.formatting import format_duration

from app.services.template_service import load_template

from app.models.poster import PosterConfig



async def generate_poster(file: UploadFile):
    """
    Generate an SVG poster from a GPX file.
    """

    temp_path = None

    try:

        # Load template
        selected_template = "minimal"
        template = load_template(selected_template)

        # Save uploaded GPX temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gpx") as temp_file:
            temp_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # Parse GPX
        activity = parse_gpx(temp_path)
        activity_name = (activity.name or Path(file.filename).stem)
        raw_points = activity.points
        sport = activity.sport
        sport_config = SPORT_CONFIGS[sport]

        # Clean track
        cleaned_points = clean_track(raw_points, sport_config)

        # Smooth elevation
        smoothed_points = smooth_elevation(cleaned_points, sport_config)

        # Statistics
        distance_km = calculate_distance(cleaned_points)
        elevation_gain_m = calculate_elevation_gain(smoothed_points)
        duration_seconds = calculate_duration(cleaned_points)

        # Simplify route
        simplified_points = simplify_points(cleaned_points)

        # Project GPS -> SVG
        svg_points = project_points(simplified_points, template.route_area)

        # Extract hours, minutes, and seconds from total duration_seconds
        calc_hours = duration_seconds // 3600
        calc_minutes = (duration_seconds % 3600) // 60
        calc_seconds = duration_seconds % 60
        
        # Format duration
        formatted_duration = format_duration(
            hours=calc_hours,
            minutes=calc_minutes,
            secs=calc_seconds,
            style=template.stats.duration_format
        )

        # Editable poster content
        poster_config = PosterConfig(
            title=activity_name.upper(),
            distance_text=f"{distance_km:.1f} KM",
            elevation_text=f"{elevation_gain_m} M",
            duration_text=formatted_duration,
            duration_hours=calc_hours,
            duration_minutes=calc_minutes,
            duration_seconds=calc_seconds,
            duration_format=template.stats.duration_format
        )

        # Output filename
        output_file = create_output_filename(activity_name)

        # Generate SVG
        generate_svg(
            points=svg_points,
            template=template,
            config=poster_config,
            output_file=output_file
        )
        
        return {
            "success": True,
            "activity_name": activity_name,
            "sport": sport,
            "svg_url": (
                f"/outputs/{Path(output_file).name}"
            ),
            "template": template.name,            
            "statistics": {
                "original_points": len(raw_points),
                "cleaned_points": len(cleaned_points),
                "simplified_points": len(simplified_points),
                "svg_points": len(svg_points),
                "distance_km": distance_km,
                "elevation_gain_m": elevation_gain_m,
                "duration_seconds": duration_seconds,
            },
            "content": {
                "title": poster_config.title,
                "distance_text": poster_config.distance_text,
                "elevation_text": poster_config.elevation_text,
                "duration_text": poster_config.duration_text,
                "duration_format": poster_config.duration_format
            }
        }

    finally:
        if temp_path:
            Path(temp_path).unlink(
                missing_ok=True
            )