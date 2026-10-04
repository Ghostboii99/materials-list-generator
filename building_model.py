"""Building objects used by the residential takeoff engine."""

from dataclasses import dataclass, field
from geometry import RoofPitch, rectangle_area, trapezoid_area, roof_plane_area


@dataclass(frozen=True)
class Opening:
    opening_id: str
    kind: str
    width_ft: float
    height_ft: float
    quantity: int = 1

    def __post_init__(self):
        if not self.opening_id.strip():
            raise ValueError("Opening ID is required.")
        if self.kind not in ("window", "exterior_door", "interior_door"):
            raise ValueError("Unsupported opening type.")
        if self.width_ft <= 0 or self.height_ft <= 0 or self.quantity <= 0:
            raise ValueError("Opening dimensions and quantity must be positive.")

    @property
    def area_sqft(self):
        return self.width_ft * self.height_ft * self.quantity

    @property
    def perimeter_lf(self):
        return 2 * (self.width_ft + self.height_ft) * self.quantity


@dataclass
class Wall:
    wall_id: str
    length_ft: float
    height_ft: float
    end_height_ft: float | None = None
    openings: list[Opening] = field(default_factory=list)

    @property
    def gross_area_sqft(self):
        if self.end_height_ft is not None:
            return trapezoid_area(self.length_ft, self.height_ft, self.end_height_ft)
        return rectangle_area(self.length_ft, self.height_ft)

    @property
    def openings_area_sqft(self):
        return sum(item.area_sqft for item in self.openings)

    @property
    def net_area_sqft(self):
        value = self.gross_area_sqft - self.openings_area_sqft
        if value < 0:
            raise ValueError(f"Openings exceed gross area for wall {self.wall_id}.")
        return value


@dataclass(frozen=True)
class RoofPlane:
    roof_id: str
    horizontal_run_ft: float
    length_ft: float
    pitch: RoofPitch

    @property
    def horizontal_area_sqft(self):
        return self.horizontal_run_ft * self.length_ft

    @property
    def sloped_length_ft(self):
        return self.pitch.sloped_length(self.horizontal_run_ft)

    @property
    def surface_area_sqft(self):
        return roof_plane_area(self.horizontal_area_sqft, self.pitch)


@dataclass
class Level:
    name: str
    walls: list[Wall] = field(default_factory=list)
    roof_planes: list[RoofPlane] = field(default_factory=list)

    @property
    def gross_wall_area_sqft(self):
        return sum(w.gross_area_sqft for w in self.walls)

    @property
    def net_wall_area_sqft(self):
        return sum(w.net_area_sqft for w in self.walls)

    @property
    def roof_area_sqft(self):
        return sum(r.surface_area_sqft for r in self.roof_planes)


@dataclass
class House:
    project_name: str
    levels: list[Level] = field(default_factory=list)

    @property
    def gross_wall_area_sqft(self):
        return sum(level.gross_wall_area_sqft for level in self.levels)

    @property
    def net_wall_area_sqft(self):
        return sum(level.net_wall_area_sqft for level in self.levels)

    @property
    def roof_area_sqft(self):
        return sum(level.roof_area_sqft for level in self.levels)
