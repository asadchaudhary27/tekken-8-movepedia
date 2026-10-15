import pytest
from sqlalchemy.exc import IntegrityError
from backend.app.models.character import Character
from backend.app.models.move import Move, MoveInput
from backend.app.models.move_property import MoveProperty


def test_character_and_move_relationships(test_db):
    """Verifies foreign key relationships between Character, Move, and MoveInput."""
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    assert jin is not None
    assert len(jin.moves) > 0

    first_move = jin.moves[0]
    assert first_move.character.slug == "jin"
    assert len(first_move.inputs) > 0


def test_uniqueness_constraint_prevents_duplicates(test_db):
    """Ensures duplicate moves for the same character violate uniqueness constraint."""
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    existing_move = jin.moves[0]

    duplicate = Move(
        character_id=jin.id,
        name="Duplicate Move",
        original_notation=existing_move.original_notation,
        normalized_notation=existing_move.normalized_notation,
        startup_frames=10,
        damage=10
    )
    test_db.add(duplicate)
    with pytest.raises(IntegrityError):
        test_db.commit()
    test_db.rollback()


def test_nullable_frame_handling_preserves_none(test_db):
    """Critical requirement: Unknown frame values MUST remain NULL/None, never 0."""
    feng = test_db.query(Character).filter(Character.slug == "feng").first()
    # Find stance move with unknown frame values
    stance_move = test_db.query(Move).filter(
        Move.character_id == feng.id,
        Move.normalized_notation == "f+3+4"
    ).first()

    assert stance_move is not None
    assert stance_move.startup_frames is None
    assert stance_move.block_advantage is None
    assert stance_move.damage is None
    # Verify explicitly that it is NOT zero
    assert stance_move.startup_frames != 0
    assert stance_move.block_advantage != 0
