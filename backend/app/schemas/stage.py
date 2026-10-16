from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class StageBase(BaseModel):
    slug: str
    name: str
    location: Optional[str] = None
    image_url: str
    has_walls: bool = True
    boundary_shape: Optional[str] = "Octagonal"
    wall_distance: Optional[str] = None
    layout_description: Optional[str] = None
    wall_break: bool = False
    hard_wall_break: bool = False
    wall_blast: bool = False
    wall_bound: bool = False
    wall_break_interaction: Optional[str] = None
    floor_break: bool = False
    floor_blast: bool = False
    floor_break_interaction: Optional[str] = None
    balcony_break: bool = False
    balcony_break_interaction: Optional[str] = None
    has_transitions: bool = False
    transition_description: Optional[str] = None
    transition_conditions: Optional[str] = None
    total_sections: int = 1
    geometry_data_json: Optional[str] = None
    special_mechanics: Optional[str] = None
    notes: Optional[str] = None


class StageRead(StageBase):
    id: int
    data_source_id: Optional[int] = None
    hazards: List[str] = []

    model_config = ConfigDict(from_attributes=True)
