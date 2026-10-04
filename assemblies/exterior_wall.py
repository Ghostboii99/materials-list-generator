"""Exterior wall material takeoff calculations."""

from building_model import Wall
from geometry import sqft_to_linear_ft
from takeoff import TakeoffItem


def exterior_wall_takeoff(
    wall: Wall,
    siding_exposure_in: float = 7.0,
    siding_stock_length_ft: float = 12.0,
    housewrap_roll_sqft: float = 1000.0,
    flashing_roll_ft: float = 75.0,
):
    """Generate core exterior materials from one wall and its openings."""
    if siding_exposure_in <= 0 or siding_stock_length_ft <= 0:
        raise ValueError("Siding exposure and stock length must be positive.")

    net_area = wall.net_area_sqft
    opening_perimeter = sum(o.perimeter_lf for o in wall.openings)

    sheathing = TakeoffItem.from_coverage(
        "Exterior", "Wall sheathing", net_area, 32, "sheets", "4x8 sheet"
    )

    housewrap = TakeoffItem.from_coverage(
        "Exterior", "Housewrap / WRB", wall.gross_area_sqft,
        housewrap_roll_sqft, "rolls", f"{housewrap_roll_sqft:g} SF roll"
    )

    siding_lf = sqft_to_linear_ft(net_area, siding_exposure_in)
    siding = TakeoffItem.from_coverage(
        "Exterior", "Lap siding", siding_lf, siding_stock_length_ft,
        "pieces", f"{siding_stock_length_ft:g} FT"
    )

    flashing = TakeoffItem.from_coverage(
        "Exterior", "Opening flashing tape", opening_perimeter,
        flashing_roll_ft, "rolls", f"{flashing_roll_ft:g} LF roll"
    )

    return [sheathing, housewrap, siding, flashing]
