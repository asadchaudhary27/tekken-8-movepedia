from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class NotationToken(BaseModel):
    raw_token: str
    direction_code: Optional[str] = None
    direction_arrow: Optional[str] = None
    direction_english: Optional[str] = None
    direction_numpad: Optional[str] = None
    buttons: List[str] = []
    buttons_english: List[str] = []
    buttons_playstation: List[str] = []
    buttons_xbox: List[str] = []
    buttons_arcade: List[str] = []
    is_simultaneous: bool = False
    is_hold: bool = False
    is_just_frame: bool = False
    is_unsupported: bool = False
    unsupported_reason: Optional[str] = None


class NotationConversionRequest(BaseModel):
    notation: str = Field(..., description="Raw notation string to translate, e.g. df+2 or f,F+1+2")
    controller_layout: str = Field("PLAYSTATION", description="Target controller layout: PLAYSTATION, XBOX, ARCADE")


class NotationConversionResponse(BaseModel):
    original_notation: str
    normalized_notation: str
    arrow_display: str
    english_display: str
    numpad_display: str
    controller_display: str
    controller_layout: str
    tokens: List[NotationToken]
    unsupported_tokens: List[str] = []
    has_unsupported_syntax: bool = False
