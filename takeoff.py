"""Purchase-ready takeoff result types."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TakeoffItem:
    category: str
    material: str
    required_quantity: float
    purchase_quantity: int
    unit: str
    stock_size: str
    overage: float
    expected_waste: float

    @classmethod
    def from_coverage(
        cls,
        category: str,
        material: str,
        required_quantity: float,
        coverage_per_unit: float,
        unit: str,
        stock_size: str,
    ):
        if required_quantity < 0:
            raise ValueError("Required quantity cannot be negative.")
        if coverage_per_unit <= 0:
            raise ValueError("Coverage per unit must be positive.")

        import math
        purchase_quantity = math.ceil(required_quantity / coverage_per_unit)
        purchased_capacity = purchase_quantity * coverage_per_unit
        overage = purchased_capacity - required_quantity

        return cls(
            category=category,
            material=material,
            required_quantity=required_quantity,
            purchase_quantity=purchase_quantity,
            unit=unit,
            stock_size=stock_size,
            overage=overage,
            expected_waste=overage,
        )
