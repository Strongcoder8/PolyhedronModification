import unittest
from math import isclose
from polyedr import Polyedr


class TestCharacteristic(unittest.TestCase):

    def test_partial_visible_outside_square(self):
        """Частично видимая грань, центр (1,1) вне единичного квадрата
         → периметр 8."""
        poly = Polyedr("data/test1.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 8.0))

    def test_partial_visible_center_inside(self):
        """Частично видимая грань, центр (0.3,0.3) внутри квадрата
        → не учитывается."""
        poly = Polyedr("data/test2.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 0.0))

    def test_fully_visible_ignored(self):
        """Полностью видимая грань не учитывается."""
        poly = Polyedr("data/test3.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 0.0))

    def test_fully_invisible_ignored(self):
        """Полностью невидимая грань не учитывается."""
        poly = Polyedr("data/test4.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 0.0))

    def test_mixed(self):
        """Две грани: одна с центром вне (периметр 4),
         вторая с центром внутри (периметр 4),
        но учитывается только первая."""
        poly = Polyedr("data/test5.geom")
        result = poly.get_partial_visible_perimeter_outside_square()
        self.assertTrue(isclose(result, 0.0))


if __name__ == '__main__':
    unittest.main()
