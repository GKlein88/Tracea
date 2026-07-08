from unittest import TestCase

from app.geo.statistics import (
    calculate_distance,
    calculate_elevation_gain,
    geodesic_distance,
)
from app.models.activity import GPSPoint


def point(
    lat: float,
    lon: float,
    ele: float | None = None
) -> GPSPoint:
    return GPSPoint(
        lat=lat,
        lon=lon,
        ele=ele
    )


class TrackStatisticsTest(TestCase):
    def test_geodesic_distance_uses_wgs84_ellipsoid(self):
        distance_km = geodesic_distance(
            point(0, 0),
            point(0, 1)
        )

        self.assertAlmostEqual(
            distance_km,
            111.32,
            places=2
        )

    def test_calculate_distance_sums_geodesic_segments(self):
        distance_km = calculate_distance(
            [
                point(0, 0),
                point(0, 1),
                point(0, 2),
            ]
        )

        self.assertAlmostEqual(
            distance_km,
            222.64,
            places=2
        )

    def test_calculate_distance_ignores_small_gps_jitter(self):
        distance_km = calculate_distance(
            [
                point(0, 0),
                point(0.00001, 0),
                point(0, 0),
                point(0.00001, 0),
                point(0, 0),
            ]
        )

        self.assertEqual(
            distance_km,
            0.0
        )

    def test_elevation_gain_ignores_small_noise(self):
        points = [
            point(0, 0, 100),
            point(0, 0, 101),
            point(0, 0, 100),
            point(0, 0, 101),
            point(0, 0, 100),
        ]

        self.assertEqual(
            calculate_elevation_gain(points),
            0
        )

    def test_elevation_gain_does_not_double_count_shallow_dips(self):
        points = [
            point(0, 0, 100),
            point(0, 0, 105),
            point(0, 0, 101),
            point(0, 0, 106),
        ]

        self.assertEqual(
            calculate_elevation_gain(
                points,
                smoothing_window=1
            ),
            6
        )

    def test_elevation_gain_counts_separate_climbs_after_real_descent(self):
        points = [
            point(0, 0, 100),
            point(0, 0, 110),
            point(0, 0, 98),
            point(0, 0, 108),
        ]

        self.assertEqual(
            calculate_elevation_gain(
                points,
                smoothing_window=1
            ),
            20
        )
