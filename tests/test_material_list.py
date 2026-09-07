import unittest

from material_list import calculate_materials


class MaterialListTests(unittest.TestCase):
    def test_known_wall(self):
        result = calculate_materials(16, 8, 16, 0)
        self.assertEqual([13, 6, 4], [item.quantity for item in result])

    def test_rejects_invalid_spacing(self):
        with self.assertRaises(ValueError):
            calculate_materials(16, stud_spacing_in=15)


if __name__ == "__main__":
    unittest.main()

