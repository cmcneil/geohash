from typing import Tuple
import re

DEFAULT_PRECISION = 10
MAX_PRECISION = 22
BITS_PER_BASE32_CHAR = 5
BASE32_CHARS = "0123456789bcdefghjkmnpqrstuvwxyz"
MAX_PRECISION_BITS = MAX_PRECISION * BITS_PER_BASE32_CHAR


def _is_valid_base32_string(s: str) -> bool:
    return re.match('^[' + BASE32_CHARS + ']*$', s) is not None


def _intify(i):
    # Python's int data type by default stores an unbounded amount of data,
    # so we trim it to a signed 32-bit integer, which is used in Java's hashCode function
    return (i % 4294967296) - 2147483648


def _java_hash_code(s):
    # https://replit.com/@Hdjensofjfnen/hashCode
    counter = 0
    for i in range(len(s)):
        counter += _intify(ord(s[-i - 1]) * (pow(31, i)))
        # The iterative algorithm that computes the hash in Java
    return _intify(counter)


class GeoHash:
    """An object for GeoHashing a latitude/longitude.

    Similar hash prefixes will be nearby.
    A replica of
    https://firebase.google.com/docs/firestore/solutions/geoqueries#kotlin+ktx
    """
    def __init__(self, latitude=37.765173, longitude=-122.439584,
                 precision=DEFAULT_PRECISION, geo_hash=None):
        if geo_hash is not None:
            if geo_hash == '' or not _is_valid_base32_string(geo_hash):
                raise ValueError("Not a valid geoHash: " + geo_hash)
            self.geo_hash = geo_hash
            return

        if precision < 1:
            raise ValueError("Precision of GeoHash must be larger than zero!")
        if precision > MAX_PRECISION:
            raise ValueError("Precision of a GeoHash must be less "
                             f"than {(MAX_PRECISION + 1)}!")
        self.latitude = latitude
        self.longitude = longitude
        self.precision = precision

        longitude_range = [-180., 180.]
        latitude_range = [-90., 90.]

        buffer = []
        for i in range(precision):
            hash_value = 0
            for j in range(BITS_PER_BASE32_CHAR):
                even = (i * BITS_PER_BASE32_CHAR + j) % 2 == 0
                val = longitude if even else latitude
                current_range = longitude_range if even else latitude_range
                mid = (current_range[0] + current_range[1]) / 2
                if val > mid:
                    hash_value = (hash_value << 1) + 1
                    current_range[0] = mid
                else:
                    hash_value = hash_value << 1
                    current_range[1] = mid
            buffer.append(BASE32_CHARS[hash_value])
        self.geo_hash = ''.join(buffer)

    def __str__(self) -> str:
        return f"GeoHash(geo_hash={self.geo_hash})"

    def __eq__(self, other):
        return self.geo_hash == other.geo_hash

    def hash_code(self) -> int:
        return _java_hash_code(self.geo_hash)

    @staticmethod
    def location_from_hash(h: str) -> Tuple[float, float]:
        decoded = 0
        num_bits = len(h) * BITS_PER_BASE32_CHAR

        for i in range(len(h)):
            c = BASE32_CHARS.index(h[i])
            decoded = decoded << BITS_PER_BASE32_CHAR
            decoded += c

        min_lng, max_lng = -180., 180.
        min_lat, max_lat = -90., 90.

        for i in range(num_bits):
            bit = (decoded >> (num_bits - i - 1)) & 1

            if i % 2 == 0:
                if bit == 1:
                    min_lng = (min_lng + max_lng) / 2
                else:
                    max_lng = (min_lng + max_lng) / 2
            else:
                if bit == 1:
                    min_lat = (min_lat + max_lat) / 2
                else:
                    max_lat = (min_lat + max_lat) / 2
        lat = (min_lat + max_lat) / 2
        lng = (min_lng + max_lng) / 2
        return (lat, lng)
