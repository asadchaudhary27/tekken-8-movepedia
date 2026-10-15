import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.character import Character
from backend.app.models.stage import Stage
from backend.app.models.user_preference import UserPreference
from backend.app.schemas.matchup import (
    MatchupConditions,
    MatchupRequest,
    MatchupOverviewResponse,
    PreferencePayload
)
from backend.app.services.matchup_analyzer import MatchupAnalyzerEngine

router = APIRouter()


@router.post("/analyze", response_model=MatchupOverviewResponse, summary="Analyze character pair on stage")
def analyze_matchup(request: MatchupRequest, db: Session = Depends(get_db)):
    """
    Computes a verified Tekken 8 matchup dashboard between two selected fighters
    on a specific battleground under designated game conditions.
    """
    # 1. Fetch player character
    player_char = db.query(Character).filter(Character.id == request.player_character_id).first()
    if not player_char:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player character ID {request.player_character_id} not found."
        )

    # 2. Fetch opponent character
    opponent_char = db.query(Character).filter(Character.id == request.opponent_character_id).first()
    if not opponent_char:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opponent character ID {request.opponent_character_id} not found."
        )

    # 3. Fetch stage
    stage = db.query(Stage).filter(Stage.id == request.stage_id).first()
    if not stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stage ID {request.stage_id} not found."
        )

    # 4. Resolve conditions
    conditions = request.conditions or MatchupConditions()

    # 5. Persist user preferences if session token is provided
    if request.session_token:
        pref = db.query(UserPreference).filter(UserPreference.session_token == request.session_token).first()
        if not pref:
            pref = UserPreference(
                session_token=request.session_token,
                last_player_character_id=player_char.id,
                last_opponent_character_id=opponent_char.id,
                last_stage_id=stage.id,
                last_conditions_json=conditions.model_dump_json()
            )
            db.add(pref)
        else:
            pref.last_player_character_id = player_char.id
            pref.last_opponent_character_id = opponent_char.id
            pref.last_stage_id = stage.id
            pref.last_conditions_json = conditions.model_dump_json()
        db.commit()

    # 6. Execute mathematical matchup analysis
    overview = MatchupAnalyzerEngine.analyze_matchup(
        db=db,
        player_char=player_char,
        opponent_char=opponent_char,
        stage=stage,
        conditions=conditions
    )

    return overview


@router.get("/preferences", summary="Get user matchup selection preferences")
def get_preferences(session_token: str = Query(..., description="Unique browser session token"), db: Session = Depends(get_db)):
    """
    Retrieves stored matchup selections for a returning browser session.
    """
    pref = db.query(UserPreference).filter(UserPreference.session_token == session_token).first()
    if not pref:
        return {
            "session_token": session_token,
            "player_character_id": None,
            "opponent_character_id": None,
            "stage_id": None,
            "conditions": None
        }

    conditions = None
    if pref.last_conditions_json:
        try:
            conditions = json.loads(pref.last_conditions_json)
        except Exception:
            pass

    return {
        "session_token": session_token,
        "player_character_id": pref.last_player_character_id,
        "opponent_character_id": pref.last_opponent_character_id,
        "stage_id": pref.last_stage_id,
        "conditions": conditions
    }


@router.post("/preferences", summary="Save user matchup selection preferences")
def save_preferences(payload: PreferencePayload, db: Session = Depends(get_db)):
    """
    Saves or updates user selection preferences.
    """
    pref = db.query(UserPreference).filter(UserPreference.session_token == payload.session_token).first()
    conditions_json = payload.conditions.model_dump_json() if payload.conditions else None

    if not pref:
        pref = UserPreference(
            session_token=payload.session_token,
            last_player_character_id=payload.player_character_id,
            last_opponent_character_id=payload.opponent_character_id,
            last_stage_id=payload.stage_id,
            last_conditions_json=conditions_json
        )
        db.add(pref)
    else:
        if payload.player_character_id is not None:
            pref.last_player_character_id = payload.player_character_id
        if payload.opponent_character_id is not None:
            pref.last_opponent_character_id = payload.opponent_character_id
        if payload.stage_id is not None:
            pref.last_stage_id = payload.stage_id
        if conditions_json is not None:
            pref.last_conditions_json = conditions_json

    db.commit()
    db.refresh(pref)

    conditions = None
    if pref.last_conditions_json:
        try:
            conditions = json.loads(pref.last_conditions_json)
        except Exception:
            pass

    return {
        "session_token": pref.session_token,
        "player_character_id": pref.last_player_character_id,
        "opponent_character_id": pref.last_opponent_character_id,
        "stage_id": pref.last_stage_id,
        "conditions": conditions
    }
