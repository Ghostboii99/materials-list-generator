import unittest

from building_model import House, Level, Opening, RoofPlane, Wall
from geometry import RoofPitch


class BuildingModelTests(unittest.TestCase):
    def test_window_area_and_perimeter(self):
        window = Opening("W01", "window", 3, 5, 2)
        self.assertEqual(30, window.area_sqft)
        self.assertEqual(32, window.perimeter_lf)

    def test_wall_deducts_openings(self):
        wall = Wall(
            "Front",
            20,
            8,
            openings=[Opening("W01", "window", 3, 5, 2)],
        )
        self.assertEqual(160, wall.gross_area_sqft)
        self.assertEqual(130, wall.net_area_sqft)

    def test_trapezoid_wall(self):
        wall = Wall("Slope Wall", 10, 8, end_height_ft=12)
        self.assertEqual(100, wall.gross_area_sqft)

    def test_roof_plane_uses_pitch(self):
        roof = RoofPlane("R01", 10, 40, RoofPitch(6))
        self.assertAlmostEqual(447.2136, roof.surface_area_sqft, places=4)
        self.assertAlmostEqual(11.18034, roof.sloped_length_ft, places=5)

    def test_house_aggregates_levels(self):
        level = Level(
            "First Floor",
            walls=[Wall("Front", 20, 8)],
            roof_planes=[RoofPlane("R01", 10, 40, RoofPitch(6))],
        )
        house = House("Example House", [level])
        self.assertEqual(160, house.gross_wall_area_sqft)
        self.assertAlmostEqual(447.2136, house.roof_area_sqft, places=4)

    def test_rejects_bad_opening_type(self):
        with self.assertRaises(ValueError):
            Opening("X01", "garage_widget", 3, 5)


if __name__ == "__main__":
    unittest.main()
