"""Generate a basic wall-framing material list."""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Material:
    material: str
    quantity: int
    unit: str


def calculate_materials(
    wall_length_ft: float,
    wall_height_ft: float = 8,
    stud_spacing_in: int = 16,
    waste_percent: float = 10.5,
) -> list[Material]:
    """Return purchase quantities for a simple continuous wall."""
    if wall_length_ft <= 0 or wall_height_ft <= 0:
        raise ValueError("Wall dimensions must be greater than zero.")
    if stud_spacing_in not in (12, 16, 24):
        raise ValueError("Stud spacing must be 12, 16, or 24 inches.")
    if not 0 <= waste_percent <= 50:
        raise ValueError("Waste must be between 0 and 50 percent.")

    factor = 1 + waste_percent / 100
    studs = math.ceil((wall_length_ft * 12 / stud_spacing_in + 1) * factor)
    plate_linear_ft = wall_length_ft * 3
    plates = math.ceil(plate_linear_ft / 8 * factor)
    sheathing_area = wall_length_ft * wall_height_ft
    sheets = math.ceil(sheathing_area / 32 * factor)

    return [
        Material("2x4 studs", studs, "each"),
        Material("2x4x8 plates", plates, "each"),
        Material("4x8 sheathing", sheets, "sheets"),
    ]


def export_csv(materials: list[Material], output_path: str) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["material", "quantity", "unit"])
        writer.writeheader()
        writer.writerows(asdict(item) for item in materials)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wall-length", type=float, required=True)
    parser.add_argument("--wall-height", type=float, default=8)
    parser.add_argument("--stud-spacing", type=int, default=16)
    parser.add_argument("--waste", type=float, default=10.5)
    parser.add_argument("--output", default="materials.csv")
    args = parser.parse_args()
    materials = calculate_materials(args.wall_length, args.wall_height, args.stud_spacing, args.waste)
    export_csv(materials, args.output)
    for item in materials:
        print(f"{item.material}: {item.quantity} {item.unit}")
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()

