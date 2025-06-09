import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from np_re_model import get_zipcode_coordinates, load_us_mainland_zipcodes

class TestZipcodeUtils(unittest.TestCase):
    def test_get_zipcode_coordinates(self):
        lat, lon = get_zipcode_coordinates('10001')
        self.assertIsNotNone(lat)
        self.assertIsNotNone(lon)

    def test_load_us_mainland_zipcodes(self):
        df = load_us_mainland_zipcodes()
        self.assertGreater(len(df), 30000)
        self.assertIn('zip_code', df.columns)
        self.assertIn('latitude', df.columns)
        self.assertIn('longitude', df.columns)

if __name__ == '__main__':
    unittest.main()
