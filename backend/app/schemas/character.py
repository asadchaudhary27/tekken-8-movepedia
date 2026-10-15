from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CharacterBase(BaseModel):
    slug: str
    name: str
    japanese_name: Optional[str] = None
    archetype: Optional[str] = None
    default_stance: Optional[str] = None
    avatar_url: Optional[str] = None
    is_dlc: bool = False


class CharacterCreate(CharacterBase):
    pass


class CharacterResponse(CharacterBase):
    id: int
    created_at: datetime
    move_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)


CharacterRead = CharacterResponse
