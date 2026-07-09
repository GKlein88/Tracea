from dataclasses import dataclass


@dataclass(frozen=True)
class GeoConfig:
    max_speed_kmh: float
    max_jump_without_time_km: float
    min_segment_distance_km: float
    max_elevation_jump: float
    elevation_gain_threshold: float
    elevation_smoothing_window: int


DEFAULT_CONFIG = GeoConfig(
    max_speed_kmh=50,
    max_jump_without_time_km=0.5,
    min_segment_distance_km=0.005,
    max_elevation_jump=5,
    elevation_gain_threshold=3,
    elevation_smoothing_window=3,
)


SPORT_CONFIGS = {
    "running": GeoConfig(
        max_speed_kmh=35,
        max_jump_without_time_km=0.5,
        min_segment_distance_km=0.001,
        max_elevation_jump=5,
        elevation_gain_threshold=4,
        elevation_smoothing_window=5,
    ),

    "hiking": GeoConfig(
        max_speed_kmh=15,
        max_jump_without_time_km=0.5,
        min_segment_distance_km=0.001,
        max_elevation_jump=8,
        elevation_gain_threshold=3,
        elevation_smoothing_window=5,
    ),

    "cycling": GeoConfig(
        max_speed_kmh=100,
        max_jump_without_time_km=0.5,
        min_segment_distance_km=0.003,
        max_elevation_jump=5,
        elevation_gain_threshold=2,
        elevation_smoothing_window=3,
    ),

    "trail": GeoConfig(
        max_speed_kmh=30,
        max_jump_without_time_km=0.5,
        min_segment_distance_km=0.001,
        max_elevation_jump=5,
        elevation_gain_threshold=3,
        elevation_smoothing_window=5,
    ),
}


def get_geo_config(sport: str | None) -> GeoConfig:
    """
    Return the appropriate geo configuration for a sport.
    Falls back to default configuration.
    """

    if not sport:
        return DEFAULT_CONFIG

    return SPORT_CONFIGS.get(
        sport.lower(),
        DEFAULT_CONFIG,
    )