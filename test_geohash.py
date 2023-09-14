from typing import Tuple
import unittest

from geohash import GeoHash


class TestGeoHash(unittest.TestCase):
    def assert_hash_round_trip(self, lat: float, lng: float, dec=2):
        h = GeoHash(lat, lng).geo_hash
        r_lat, r_lng = GeoHash.location_from_hash(h)
        self.assertAlmostEqual(lat, r_lat, dec)
        self.assertAlmostEqual(lng, r_lng, dec)

    def test_hash_values(self):
        self.assertEqual(GeoHash(geo_hash="7zzzzzzzzz"), GeoHash(0, 0))
        self.assertEqual(GeoHash(geo_hash="2pbpbpbpbp"), GeoHash(0, -180))
        self.assertEqual(GeoHash(geo_hash="rzzzzzzzzz"), GeoHash(0, 180))
        self.assertEqual(GeoHash(geo_hash="5bpbpbpbpb"), GeoHash(-90, 0))
        self.assertEqual(GeoHash(geo_hash="0000000000"), GeoHash(-90, -180))
        self.assertEqual(GeoHash(geo_hash="pbpbpbpbpb"), GeoHash(-90, 180))
        self.assertEqual(GeoHash(geo_hash="gzzzzzzzzz"), GeoHash(90, 0))
        self.assertEqual(GeoHash(geo_hash="bpbpbpbpbp"), GeoHash(90, -180))
        self.assertEqual(GeoHash(geo_hash="zzzzzzzzzz"), GeoHash(90, 180))
        self.assertEqual(GeoHash(geo_hash="9q8yywe56g"), GeoHash(37.7853074, -122.4054274))
        self.assertEqual(GeoHash(geo_hash="dqcjf17sy6"), GeoHash(38.98719, -77.250783))
        self.assertEqual(GeoHash(geo_hash="tj4p5gerfz"), GeoHash(29.3760648, 47.9818853))
        self.assertEqual(GeoHash(geo_hash="umghcygjj7"), GeoHash(78.216667, 15.55))
        self.assertEqual(GeoHash(geo_hash="4qpzmren1k"), GeoHash(-54.933333, -67.616667))
        self.assertEqual(GeoHash(geo_hash="4w2kg3s54y"), GeoHash(-54, -67))

    def test_location_from_hash(self):
        self.assert_hash_round_trip(37.7853074, -122.4054274)
        self.assert_hash_round_trip(38.98719, -77.250783)
        self.assert_hash_round_trip(29.3760648, 47.9818853)
        self.assert_hash_round_trip(78.216667, 15.55)
        self.assert_hash_round_trip(-54.933333, -67.616667)
        self.assert_hash_round_trip(-54, -67)
        self.assert_hash_round_trip(0, 0)
        self.assert_hash_round_trip(0, -180)
        self.assert_hash_round_trip(0, 180)
        self.assert_hash_round_trip(-90, 0)
        self.assert_hash_round_trip(-90, -180)
        self.assert_hash_round_trip(-90, 180)
        self.assert_hash_round_trip(90, 0)
        self.assert_hash_round_trip(90, -180)
        self.assert_hash_round_trip(90, 180)

    def test_custom_precision(self):
        self.assertEqual(GeoHash(geo_hash="000000"), GeoHash(-90, -180, 6))
        self.assertEqual(GeoHash(geo_hash="zzzzzzzzzzzzzzzzzzzz"), GeoHash(90, 180, 20))
        self.assertEqual(GeoHash(geo_hash="p"), GeoHash(-90, 180, 1))
        self.assertEqual(GeoHash(geo_hash="bpbpb"), GeoHash(90, -180, 5))
        self.assertEqual(GeoHash(geo_hash="9q8yywe5"), GeoHash(37.7853074, -122.4054274, 8))
        self.assertEqual(GeoHash(geo_hash="dqcjf17sy6cppp8vfn"), GeoHash(38.98719, -77.250783, 18))
        self.assertEqual(GeoHash(geo_hash="tj4p5gerfzqu"), GeoHash(29.3760648, 47.9818853, 12))
        self.assertEqual(GeoHash(geo_hash="u"), GeoHash(78.216667, 15.55, 1))
        self.assertEqual(GeoHash(geo_hash="4qpzmre"), GeoHash(-54.933333, -67.616667, 7))
        self.assertEqual(GeoHash(geo_hash="4w2kg3s54"), GeoHash(-54, -67, 9))


if __name__ == '__main__':
    unittest.main()
