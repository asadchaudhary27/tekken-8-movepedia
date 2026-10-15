from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.character import Character
from backend.app.models.practice import PracticeRecord
from backend.app.schemas.punishment import (
    PunishmentAssistantResponse,
    PracticeAttemptPayload,
    PracticeProgressResponse,
    PracticeRecordItem
)
from backend.app.services.punishment_engine import SmartPunishmentEngine

router = APIRouter()


@router.get("/options", response_model=PunishmentAssistantResponse, summary="Get smart punishment options")
def get_punishment_options(
    player_character_id: int = Query(..., description="Selected player character ID"),
    opponent_character_id: int = Query(..., description="Opponent character ID"),
    query: Optional[str] = Query(None, description="Search opponent move name or notation"),
    block_filter: Optional[str] = Query(None, description="ALL, PUNISHABLE, LAUNCH_PUNISHABLE, SAFE, or PLUS"),
    hit_level: Optional[str] = Query(None, description="ALL, h, m, or l"),
    stance: Optional[str] = Query(None, description="Character stance filter or ALL"),
    classification: Optional[str] = Query(None, description="PUNISHABLE, LAUNCH, SAFE, or ALL"),
    min_damage: Optional[int] = Query(None, description="Minimum punish damage filter"),
    patch_version: Optional[str] = Query(None, description="Patch version filter e.g. 3.00.02"),
    verification_status: Optional[str] = Query(None, description="VERIFIED, CONDITIONAL, or UNVERIFIED"),
    db: Session = Depends(get_db)
):
    """
    Evaluates verified frame data for an opponent's move list against the selected player character's
    punishment tools. Distinguishes standing vs crouching recovery, While-Standing (WS) vs standing options,
    severe pushback reach constraints, and provides beginner-friendly explanations. Zero guessed frame values.
    """
    player_char = db.query(Character).filter(Character.id == player_character_id).first()
    if not player_char:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player character ID {player_character_id} not found."
        )

    opponent_char = db.query(Character).filter(Character.id == opponent_character_id).first()
    if not opponent_char:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opponent character ID {opponent_character_id} not found."
        )

    return SmartPunishmentEngine.analyze_punishments(
        db=db,
        player_char=player_char,
        opponent_char=opponent_char,
        query=query,
        block_filter=block_filter,
        hit_level=hit_level,
        stance=stance,
        classification=classification,
        min_damage=min_damage,
        patch_version=patch_version,
        verification_status=verification_status
    )


@router.post("/practice/record", response_model=PracticeRecordItem, summary="Record a practice attempt")
def record_practice_attempt(
    payload: PracticeAttemptPayload,
    db: Session = Depends(get_db)
):
    """
    Records an interactive trial in practice mode (SUCCESS or FAIL) against a specific opponent move
    and updates the rolling mastery percentage.
    """
    if payload.result.upper() not in ["SUCCESS", "FAIL"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Result must be either 'SUCCESS' or 'FAIL'."
        )

    rec = SmartPunishmentEngine.record_practice_attempt(
        db=db,
        session_token=payload.session_token,
        player_char_id=payload.player_character_id,
        opponent_char_id=payload.opponent_character_id,
        opponent_move_id=payload.opponent_move_id,
        opponent_move_name=payload.opponent_move_name,
        opponent_move_input=payload.opponent_move_input,
        punish_move_input=payload.punish_move_input,
        result=payload.result
    )

    return PracticeRecordItem(
        id=rec.id,
        opponent_move_name=rec.opponent_move_name,
        opponent_move_input=rec.opponent_move_input,
        punish_move_input=rec.punish_move_input,
        success_count=rec.success_count,
        fail_count=rec.fail_count,
        attempts=rec.attempts,
        mastery_score=rec.mastery_score,
        last_practiced_at=rec.last_practiced_at.isoformat() if rec.last_practiced_at else None
    )


@router.get("/practice/progress", response_model=PracticeProgressResponse, summary="Get training progress")
def get_practice_progress(
    session_token: str = Query(..., description="Browser session token"),
    db: Session = Depends(get_db)
):
    """
    Returns cumulative training progress, checklist records, and overall accuracy for the practice mode.
    """
    return SmartPunishmentEngine.get_practice_progress(
        db=db,
        session_token=session_token
    )


@router.post("/practice/reset", summary="Reset training progress")
def reset_practice_progress(
    session_token: str = Query(..., description="Browser session token"),
    db: Session = Depends(get_db)
):
    """
    Clears all practice records for the specified session token.
    """
    deleted_count = db.query(PracticeRecord).filter(
        PracticeRecord.session_token == session_token
    ).delete()
    db.commit()

    return {
        "message": f"Reset {deleted_count} practice records successfully.",
        "session_token": session_token
    }
