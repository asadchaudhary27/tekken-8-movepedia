import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.app.models.character import Character
from backend.app.models.stage import Stage


def test_list_stages_and_hazards(client: TestClient):
    """Verify official stages endpoint returns 10 arenas with hazard tags."""
    response = client.get("/api/v1/stages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10

    stage_names = [s["name"] for s in data]
    assert "The Arena" in stage_names
    assert "Yakushima" in stage_names
    assert "Sanctum" in stage_names

    # Check Yakushima is infinite with no walls
    yakushima = next(s for s in data if s["slug"] == "yakushima")
    assert yakushima["has_walls"] is False
    assert yakushima["boundary_shape"] == "Infinite"
    assert "Infinite Arena" in yakushima["hazards"]

    # Check Sanctum has floor break and hard wall break
    sanctum = next(s for s in data if s["slug"] == "sanctum")
    assert sanctum["floor_break"] is True
    assert sanctum["hard_wall_break"] is True
    assert "Floor Break" in sanctum["hazards"]


def test_stage_filter_by_walls(client: TestClient):
    """Verify filtering stages by presence of walls."""
    response = client.get("/api/v1/stages?has_walls=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(s["has_walls"] is False for s in data)


def test_stage_lookup_by_slug_and_id(client: TestClient):
    """Verify lookup by slug or id, and 404 handling."""
    res_slug = client.get("/api/v1/stages/the-arena")
    assert res_slug.status_code == 200
    assert res_slug.json()["slug"] == "the-arena"

    stage_id = res_slug.json()["id"]
    res_id = client.get(f"/api/v1/stages/{stage_id}")
    assert res_id.status_code == 200
    assert res_id.json()["name"] == "The Arena"

    res_404 = client.get("/api/v1/stages/nonexistent-stage-xyz")
    assert res_404.status_code == 404


def test_matchup_analysis_jin_vs_kazuya(client: TestClient, test_db: Session):
    """
    Verify complete matchup calculation:
    - Jin as Player
    - Kazuya as Opponent
    - The Arena as Stage
    - Mathematical punish windows correctly calculated against -10 or worse moves.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    kazuya = test_db.query(Character).filter(Character.slug == "kazuya").first()
    arena = test_db.query(Stage).filter(Stage.slug == "the-arena").first()

    assert jin is not None
    assert kazuya is not None
    assert arena is not None

    payload = {
        "player_character_id": jin.id,
        "opponent_character_id": kazuya.id,
        "stage_id": arena.id,
        "conditions": {
            "wall_position": "OPEN",
            "heat_state": "AVAILABLE",
            "starting_distance": "MID",
            "player_side": "P1"
        },
        "session_token": "test-session-token-123"
    }

    response = client.post("/api/v1/matchup/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Characters and stage verified
    assert data["player_character"]["name"] == "Jin Kazama"
    assert data["opponent_character"]["name"] == "Kazuya Mishima"
    assert data["stage"]["name"] == "The Arena"

    # Punish matrix calculation
    punish_matrix = data["punish_matrix"]
    assert len(punish_matrix) > 0

    # Kazuya Hell Sweep is -23 on block -> Should find a launch punish
    hellsweep_punishes = [
        p for p in punish_matrix 
        if "Hell Sweep" in p["opponent_move_name"] or "Spinning Demon" in p["opponent_move_name"]
    ]
    assert len(hellsweep_punishes) > 0
    p = hellsweep_punishes[0]
    assert p["opponent_block_advantage"] == -23
    assert p["punish_startup"] <= 23

    # Key moves extracted
    assert len(data["player_key_moves"]) > 0

    # Lab notes found
    assert data["has_specific_lab_notes"] is True
    assert "Mishima mirror dynamics" in data["matchup_notes"]

    # Data completeness report
    assert data["data_completeness"]["patch_version"] == "3.00.02"
    assert data["data_completeness"]["is_lab_verified"] is True


def test_matchup_fallback_unlabbed_pair(client: TestClient, test_db: Session):
    """
    Verify transparent fallback when specific lab notes are not cataloged yet:
    No fake data, clear notice to user, but frame-data punishes still calculate.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    reina = test_db.query(Character).filter(Character.slug == "reina").first()
    arena = test_db.query(Stage).filter(Stage.slug == "the-arena").first()

    payload = {
        "player_character_id": jin.id,
        "opponent_character_id": reina.id,
        "stage_id": arena.id
    }

    response = client.post("/api/v1/matchup/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["has_specific_lab_notes"] is False
    assert "Pair-specific lab notes not cataloged yet" in data["matchup_notes"]


def test_preference_persistence_and_swap(client: TestClient, test_db: Session):
    """Verify session token preferences save and retrieval."""
    token = "session-pref-unit-test"
    payload = {
        "session_token": token,
        "player_character_id": 1,
        "opponent_character_id": 2,
        "stage_id": 1,
        "conditions": {
            "wall_position": "NEAR_WALL",
            "heat_state": "IN_HEAT",
            "starting_distance": "CLOSE",
            "player_side": "P2"
        }
    }

    # Save preferences
    save_res = client.post("/api/v1/matchup/preferences", json=payload)
    assert save_res.status_code == 200
    saved = save_res.json()
    assert saved["player_character_id"] == 1
    assert saved["opponent_character_id"] == 2
    assert saved["conditions"]["wall_position"] == "NEAR_WALL"

    # Get preferences
    get_res = client.get(f"/api/v1/matchup/preferences?session_token={token}")
    assert get_res.status_code == 200
    retrieved = get_res.json()
    assert retrieved["player_character_id"] == 1
    assert retrieved["opponent_character_id"] == 2
    assert retrieved["conditions"]["heat_state"] == "IN_HEAT"
