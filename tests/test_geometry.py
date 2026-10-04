import math
import unittest

from geometry import (
    RoofPitch,
    gable_area,
    linear_ft_to_pieces,
    rectangle_area,
    roof_plane_area,
    sqft_to_linear_ft,
    sqft_to_sheets,
    trapezoid_area,
    triangle_area,
)


class GeometryTests(unittest.TestCase):
    def test_basic_shapes(self):
        self.assertEqual(80, rectangle_area(10, 8))
        self.assertEqual(24, triangle_area(6, 8))
        self.assertEqual(60, trapezoid_area(10, 4, 8))

    def test_six_twelve_pitch(self):
        pitch = RoofPitch(6, 12)
        self.assertAlmostEqual(0.5, pitch.slope)
        self.assertAlmostEqual(26.565, pitch.angle_degrees, places=3)
        self.assertAlmostEqual(math.sqrt(1.25), pitch.multiplier)

    def test_sloped_length(self):
        self.assertAlmostEqual(11.18034, RoofPitch(6).sloped_length(10), places=5)

    def test_roof_plane_area_uses_pitch(self):
        self.assertAlmostEqual(1118.034, roof_plane_area(1000, RoofPitch(6)), places=3)

    def test_gable_area(self):
        # 20x8 rectangle + triangle with 10 ft run and 5 ft rise.
        self.assertEqual(210, gable_area(20, 8, RoofPitch(6)))

    def test_sheet_conversion_rounds_up(self):
        self.assertEqual(4, sqft_to_sheets(100))

    def test_sqft_to_linear_ft_uses_exposure(self):
        # 100 sq ft at 6-inch exposure requires 200 LF.
        self.assertEqual(200, sqft_to_linear_ft(100, 6))

    def test_linear_ft_to_stock_pieces(self):
        self.assertEqual(6, linear_ft_to_pieces(87, 16))

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            RoofPitch(-1)
        with self.assertRaises(ValueError):
            rectangle_area(0, 8)
        with self.assertRaises(ValueError):
            sqft_to_linear_ft(100, 0)


if __name__ == "__main__":
    unittest.main()
