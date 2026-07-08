from datetime import datetime, timedelta, timezone
from unittest import TestCase

from app.geo.clean import clean_track
from app.models.activity import GPSPoint


def point(
    lat: float,
    lon: float,
    seconds: int | None = None
) -> GPSPoint:
    timestamp = None

    if seconds is not None:
        timestamp = datetime(
            2026,
            1,
            1,
            tzinfo=timezone.utc
        ) + timedelta(seconds=seconds)

    return GPSPoint(
        lat=lat,
        lon=lon,
        time=timestamp
    )


class TrackCleaningTest(TestCase):
    def test_cleaning_keeps_close_points(self):
        points = [
            point(0, 0),
            point(0.00001, 0),
            point(0.0001, 0),
        ]

        self.assertEqual(
            clean_track(points),
            points
        )

    def test_cleaning_removes_isolated_spike(self):
        points = [
            point(0, 0, 0),
            point(1, 1, 60),
            point(0, 0.001, 120),
        ]

        self.assertEqual(
            clean_track(points),
            [
                points[0],
                points[2],
            ]
        )

    def test_cleaning_keeps_real_track_after_sampling_gap(self):
        points = [
            point(0, 0),
            point(0, 0.03),
            point(0, 0.031),
        ]

        self.assertEqual(
            clean_track(points),
            points
        )
