from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from backend.app.schemas.stage import StageRead
from backend.app.schemas.character import CharacterRead
from backend.app.schemas.combo import ComboRouteRead


class StageGeometryElement(BaseModel):
    element_type: str = Field(description="wall, break_zone, hazard, spawn, or balcony")
    label: str
    x: float
    y: float
    width: Optional[float] = None
    height: Optional[float] = None
    radius: Optional[float] = None
    points: Optional[str] = None
    color: Optional[str] = None
    notes: Optional[str] = None


class StageGeometryData(BaseModel):
    is_verified: bool = True
    shape: str = "Octagonal"
    width_meters: float = 24.0
    length_meters: float = 24.0
    canvas_viewbox: str = "0 0 400 400"
    elements: List[StageGeometryElement] = Field(default_factory=list)


class StageStrategyReport(BaseModel):
    stage: StageRead
    player_character: CharacterRead
    opponent_character: Optional[CharacterRead] = None

    # Geometry & Layout Intelligence
    geometry_available: bool = False
    geometry_data: Optional[Dict[str, Any]] = None
    layout_description: str
    wall_distance: str
    wall_availability_status: str

    # 1. Midscreen combo options
    midscreen_combos: List[ComboRouteRead] = Field(default_factory=list)

    # 2. Wall-carry routes
    wall_carry_routes: List[ComboRouteRead] = Field(default_factory=list)

    # 3. Wall-combo enders
    wall_combo_enders: List[ComboRouteRead] = Field(default_factory=list)

    # 4. Wall-break opportunities
    wall_break_routes: List[ComboRouteRead] = Field(default_factory=list)
    wall_break_interaction: Optional[str] = None

    # 5. Floor-break opportunities
    floor_break_routes: List[ComboRouteRead] = Field(default_factory=list)
    floor_break_interaction: Optional[str] = None

    # 6. Balcony-break opportunities
    balcony_break_routes: List[ComboRouteRead] = Field(default_factory=list)
    balcony_break_interaction: Optional[str] = None

    # 7. Corner pressure and wall positioning
    corner_pressure_strategy: str
    wall_positioning_notes: str

    # 8. Situations where wall combo or transition is unavailable
    unavailable_mechanics_warning: List[str] = Field(default_factory=list)

    # 9. Stage-dependency analysis
    universal_combos_count: int = 0
    stage_dependent_combos_count: int = 0
    tactical_summary: str

    # Metadata & Source
    source: str = "TekkenDocs / Stage Strategy Lab"
    patch_version: str = "3.00.02"
