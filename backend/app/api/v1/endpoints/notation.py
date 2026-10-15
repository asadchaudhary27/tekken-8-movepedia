from fastapi import APIRouter, status
from backend.app.schemas.notation import (
    NotationConversionRequest,
    NotationConversionResponse
)
from backend.app.services.notation import NotationEngine

router = APIRouter()


@router.post("/convert", response_model=NotationConversionResponse, summary="Convert notation to 4 display modes")
def convert_notation(payload: NotationConversionRequest):
    """
    Translates input notation into:
    1. Arrow Display (e.g. ↘ + 2)
    2. English Display (e.g. Down Forward + Right Punch)
    3. Numpad Display (e.g. 3 + 2)
    4. Controller Display (e.g. ↘ + △)
    """
    response = NotationEngine.convert(
        raw_notation=payload.notation,
        controller_layout=payload.controller_layout
    )
    return response
