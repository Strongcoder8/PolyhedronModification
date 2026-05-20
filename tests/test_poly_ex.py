import unittest
from math import isclose
from shadow.polyedr import Polyedr

class TestCharacteristic(unittest.TestCase):

    def test_partial_visible_outside_square(self):
        poly = Polyedr("data/test1.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 8.0))

    def test_partial_visible_center_inside(self):
        poly = Polyedr("data/test2.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 0.0))

    def test_fully_visible_ignored(self):
        poly = Polyedr("data/test3.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 0.0))

    def test_fully_invisible_ignored(self):
        poly = Polyedr("data/test4.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 0.0))

    def test_mixed(self):
        poly = Polyedr("data/test5.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 4.0))

if __name__ == '__main__': # pragma: no cover
    unittest.main()