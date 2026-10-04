import unittest

from assemblies.exterior_wall import exterior_wall_takeoff
from building_model import Opening, Wall


class ExteriorWallTakeoffTests(unittest.TestCase):
    def test_wall_generates_purchase_ready_materials(self):
        wall = Wall(
            "Front",
            20,
            8,
            openings=[
                Opening("W01", "window", 3, 5, 2),
                Opening("D01", "exterior_door", 3, 7),
            ],
        )

        items = exterior_wall_takeoff(
            wall,
            siding_exposure_in=6,
            siding_stock_length_ft=12,
            housewrap_roll_sqft=100,
            flashing_roll_ft=50,
        )
        by_name = {item.material: item for item in items}

        # 160 gross SF - 30 SF windows - 21 SF door = 109 net SF.
        self.assertEqual(109, by_name["Wall sheathing"].required_quantity)
        self.assertEqual(4, by_name["Wall sheathing"].purchase_quantity)
        self.assertEqual(19, by_name["Wall sheathing"].expected_waste)

        # Housewrap intentionally covers gross wall area before openings are cut.
        self.assertEqual(160, by_name["Housewrap / WRB"].required_quantity)
        self.assertEqual(2, by_name["Housewrap / WRB"].purchase_quantity)

        # 109 SF at 6-inch exposure = 218 LF; 12-ft boards => 19 pieces.
        self.assertEqual(218, by_name["Lap siding"].required_quantity)
        self.assertEqual(19, by_name["Lap siding"].purchase_quantity)

        # Two 3x5 windows = 32 LF perimeter; one 3x7 door = 20 LF.
        self.assertEqual(52, by_name["Opening flashing tape"].required_quantity)
        self.assertEqual(2, by_name["Opening flashing tape"].purchase_quantity)


if __name__ == "__main__":
    unittest.main()
