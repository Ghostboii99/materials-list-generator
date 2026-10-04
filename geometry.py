"""Reusable geometry calculations for residential takeoffs."""

from __future__ import annotations

import math
from dataclasses import dataclass


def _positive(value: float, name: str) -> float:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    return value


@dataclass(frozen=True)
class RoofPitch:
    """Roof pitch expressed as rise per horizontal run (12 by default)."""
    rise: float
    run: float = 12.0

    def __post_init__(self) -> None:
        _positive(self.run, "Pitch run")
        if self.rise < 0:
            raise ValueError("Pitch rise cannot be negative.")

    @property
    def slope(self) -> float:
        return self.rise / self.run

    @property
    def angle_degrees(self) -> float:
        return math.degrees(math.atan(self.slope))

    @property
    def multiplier(self) -> float:
        return math.sqrt(1 + self.slope ** 2)

    def sloped_length(self, horizontal_run_ft: float) -> float:
        return _positive(horizontal_run_ft, "Horizontal run") * self.multiplier


def rectangle_area(length_ft: float, height_ft: float) -> float:
    return _positive(length_ft, "Length") * _positive(height_ft, "Height")


def triangle_area(base_ft: float, height_ft: float) -> float:
    return _positive(base_ft, "Base") * _positive(height_ft, "Height") / 2


def trapezoid_area(base_ft: float, height_one_ft: float, height_two_ft: float) -> float:
    _positive(base_ft, "Base")
    _positive(height_one_ft, "First height")
    _positive(height_two_ft, "Second height")
    return base_ft * (height_one_ft + height_two_ft) / 2


def slope_from_rise_run(rise: float, run: float) -> float:
    _positive(run, "Run")
    if rise < 0:
        raise ValueError("Rise cannot be negative.")
    return rise / run


def roof_plane_area(horizontal_area_sqft: float, pitch: RoofPitch) -> float:
    return _positive(horizontal_area_sqft, "Horizontal roof area") * pitch.multiplier


def gable_area(width_ft: float, wall_height_ft: float, pitch: RoofPitch) -> float:
    _positive(width_ft, "Gable width")
    _positive(wall_height_ft, "Wall height")
    gable_rise = (width_ft / 2) * pitch.slope
    return rectangle_area(width_ft, wall_height_ft) + triangle_area(width_ft, gable_rise)


def sqft_to_sheets(area_sqft: float, sheet_width_ft: float = 4, sheet_length_ft: float = 8) -> int:
    coverage = _positive(sheet_width_ft, "Sheet width") * _positive(sheet_length_ft, "Sheet length")
    return math.ceil(_positive(area_sqft, "Area") / coverage)


def sqft_to_linear_ft(area_sqft: float, coverage_width_in: float) -> float:
    coverage_ft = _positive(coverage_width_in, "Coverage width") / 12
    return _positive(area_sqft, "Area") / coverage_ft


def linear_ft_to_pieces(linear_ft: float, stock_length_ft: float) -> int:
    return math.ceil(_positive(linear_ft, "Linear feet") / _positive(stock_length_ft, "Stock length"))
