from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class SearchResultItem(BaseModel):
    id: int
    category: str  # CHARACTER, MOVE, COMBO, STAGE
    title: str
    subtitle: str
    character_name: Optional[str] = None
    character_slug: Optional[str] = None
    notation: Optional[str] = None
    badge: Optional[str] = None
    target_section: str  # fighters, move-explorer, combo-lab, stages, analyzer
    deep_link_params: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class GlobalSearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResultItem] = Field(default_factory=list)
    character_results: List[SearchResultItem] = Field(default_factory=list)
    move_results: List[SearchResultItem] = Field(default_factory=list)
    combo_results: List[SearchResultItem] = Field(default_factory=list)
    stage_results: List[SearchResultItem] = Field(default_factory=list)
