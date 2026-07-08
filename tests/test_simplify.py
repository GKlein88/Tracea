from unittest import TestCase

from app.geo.simplify import simplify_points
from app.models.activity import GPSPoint


def point(lat: float, lon: float) -> GPSPoint:
    return GPSPoint(
        lat=lat,
        lon=lon
    )


class TrackSimplificationTest(TestCase):
    def test_simplification_removes_visually_close_points(self):
        points = [
            point(0, 0),
            point(0.00001, 0),
            point(0.0001, 0),
        ]

        self.assertEqual(
            simplify_points(points),
            [
                points[0],
                points[2],
            ]
        )
