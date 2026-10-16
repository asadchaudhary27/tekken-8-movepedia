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


def test_directional_asymmetry_jin_vs_kazuya(client: TestClient, test_db: Session):
    """
    Verify directional asymmetry:
    Jin (P1) vs Kazuya (P2) != Kazuya (P1) vs Jin (P2).
    Both directions must yield distinct, asymmetric tactical advice and ratings.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    kazuya = test_db.query(Character).filter(Character.slug == "kazuya").first()
    arena = test_db.query(Stage).filter(Stage.slug == "the-arena").first()

    assert jin is not None and kazuya is not None and arena is not None

    # Direction 1: Jin vs Kazuya
    payload_jin_p1 = {
        "player_character_id": jin.id,
        "opponent_character_id": kazuya.id,
        "stage_id": arena.id
    }
    res_jin = client.post("/api/v1/matchup/analyze", json=payload_jin_p1)
    assert res_jin.status_code == 200
    data_jin = res_jin.json()

    # Direction 2: Kazuya vs Jin
    payload_kaz_p1 = {
        "player_character_id": kazuya.id,
        "opponent_character_id": jin.id,
        "stage_id": arena.id
    }
    res_kaz = client.post("/api/v1/matchup/analyze", json=payload_kaz_p1)
    assert res_kaz.status_code == 200
    data_kaz = res_kaz.json()

    # 1. Asymmetric Rating Verification
    assert data_jin["overall_assessment"]["rating"] == "FAVORABLE"
    assert data_jin["overall_assessment"]["rating_label"] == "Favorable"
    assert data_jin["overall_assessment"]["rating_color"] == "success"

    assert data_kaz["overall_assessment"]["rating"] == "EVEN"
    assert data_kaz["overall_assessment"]["rating_label"] == "Even"
    assert data_kaz["overall_assessment"]["rating_color"] == "info"

    # 2. Asymmetric Sidestep Advice
    assert data_jin["sidestep_and_tracking"]["recommended_side"] == "SSL"
    assert data_kaz["sidestep_and_tracking"]["recommended_side"] == "SSR"

    # 3. Asymmetric Directional Metadata
    assert data_jin["directional_provenance"]["direction"] == "Jin Kazama (P1) vs Kazuya Mishima (P2)"
    assert data_kaz["directional_provenance"]["direction"] == "Kazuya Mishima (P1) vs Jin Kazama (P2)"

    # 4. Asymmetric Useful & Dangerous Moves
    jin_useful_inputs = [m["input"] for m in data_jin["useful_moves"]]
    assert "f+4" in jin_useful_inputs or "f,f+2" in jin_useful_inputs

    kaz_useful_inputs = [m["input"] for m in data_kaz["useful_moves"]]
    assert "f,n,df+2" in kaz_useful_inputs or "ws1,2" in kaz_useful_inputs


def test_unfavorable_directional_rating_king_vs_feng(client: TestClient, test_db: Session):
    """
    Verify UNFAVORABLE rating rule:
    King playing against Feng Wei is classified as UNFAVORABLE due to Kenpo evasion.
    """
    king = test_db.query(Character).filter(Character.slug == "king").first()
    feng = test_db.query(Character).filter(Character.slug == "feng").first()
    arena = test_db.query(Stage).filter(Stage.slug == "the-arena").first()

    assert king is not None and feng is not None and arena is not None

    payload = {
        "player_character_id": king.id,
        "opponent_character_id": feng.id,
        "stage_id": arena.id
    }
    response = client.post("/api/v1/matchup/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["overall_assessment"]["rating"] == "UNFAVORABLE"
    assert data["overall_assessment"]["rating_label"] == "Unfavorable"
    assert data["overall_assessment"]["rating_color"] == "danger"
    assert "Kenpo" in data["overall_assessment"]["reasoning"] or "evasive" in data["overall_assessment"]["reasoning"]
    assert data["overall_assessment"]["confidence_level"] == "HIGH"
    assert data["overall_assessment"]["confidence_score"] >= 80


def test_all_10_matchup_sections_present(client: TestClient, test_db: Session):
    """
    Verify all 10 required Phase 2 matchup intelligence sections are strictly returned:
    1. Overall matchup assessment
    2. Player character strengths
    3. Opponent character strengths
    4. Player's useful moves against this opponent
    5. Opponent moves requiring special attention
    6. Range, approach, spacing, and movement considerations
    7. Defensive options and punish opportunities
    8. Side-step, tracking, and evasive considerations
    9. Heat mechanics and character-specific mechanics
    10. Stage-specific matchup considerations
    Plus: Directional provenance metadata
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    kazuya = test_db.query(Character).filter(Character.slug == "kazuya").first()
    arena = test_db.query(Stage).filter(Stage.slug == "the-arena").first()

    payload = {
        "player_character_id": jin.id,
        "opponent_character_id": kazuya.id,
        "stage_id": arena.id
    }
    response = client.post("/api/v1/matchup/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Section 1: Overall Matchup Assessment
    oa = data["overall_assessment"]
    assert "rating" in oa and oa["rating"] in ["FAVORABLE", "EVEN", "UNFAVORABLE", "INSUFFICIENT_DATA"]
    assert "rating_label" in oa
    assert "rating_color" in oa
    assert "reasoning" in oa and len(oa["reasoning"]) > 0
    assert "confidence_level" in oa and oa["confidence_level"] in ["HIGH", "MEDIUM", "LOW", "NONE"]
    assert "confidence_score" in oa and 0 <= oa["confidence_score"] <= 100
    assert isinstance(oa["evidence_sources"], list)
    assert isinstance(oa["unknowns"], list)

    # Section 2: Player Strengths
    assert "player_strengths" in data and isinstance(data["player_strengths"], list)
    assert len(data["player_strengths"]) > 0

    # Section 3: Opponent Strengths
    assert "opponent_strengths" in data and isinstance(data["opponent_strengths"], list)
    assert len(data["opponent_strengths"]) > 0

    # Section 4: Player's Useful Moves
    assert "useful_moves" in data and isinstance(data["useful_moves"], list)
    assert len(data["useful_moves"]) > 0
    u_move = data["useful_moves"][0]
    assert "move_name" in u_move and "input" in u_move and "role" in u_move and "tactical_purpose" in u_move

    # Section 5: Opponent Dangerous Moves
    assert "dangerous_moves" in data and isinstance(data["dangerous_moves"], list)
    assert len(data["dangerous_moves"]) > 0
    d_move = data["dangerous_moves"][0]
    assert "move_name" in d_move and "input" in d_move and "risk_level" in d_move
    assert "threat_description" in d_move and "recommended_counter" in d_move

    # Section 6: Spacing & Movement
    sm = data["spacing_and_movement"]
    assert "optimal_range" in sm
    assert "neutral_strategy" in sm
    assert "approach_advice" in sm
    assert "retreat_spacing" in sm

    # Section 7: Defensive Tactics
    dt = data["defensive_tactics"]
    assert "punish_matrix" in dt and len(dt["punish_matrix"]) > 0
    assert "fuzzy_guard_notes" in dt
    assert "interrupt_opportunities" in dt
    assert "low_defense_priority" in dt

    # Section 8: Sidestep & Tracking
    st = data["sidestep_and_tracking"]
    assert "recommended_side" in st
    assert "side_label" in st
    assert "reasoning" in st
    assert "linear_moves_to_step" in st
    assert "opponent_homing_moves" in st

    # Section 9: Heat Mechanics
    hm = data["heat_and_mechanics"]
    assert "player_heat_focus" in hm
    assert "opponent_heat_threats" in hm
    assert "heat_smash_interaction" in hm
    assert "stance_and_install_dynamics" in hm

    # Section 10: Stage Matchup Synergy
    sms = data["stage_matchup_synergy"]
    assert "has_walls" in sms
    assert "wall_danger_level" in sms
    assert "tactical_advice" in sms
    assert "character_stage_advantage" in sms

    # Directional Provenance Metadata
    dp = data["directional_provenance"]
    assert "direction" in dp
    assert "patch_version" in dp and dp["patch_version"] == "3.00.02"
    assert "contributor" in dp
    assert "verification_status" in dp
    assert "last_reviewed" in dp


def test_insufficient_data_rating_for_unlabbed_pair(client: TestClient, test_db: Session):
    """
    Verify INSUFFICIENT_DATA rating rule for uncataloged pairings:
    No fake win rates or speculative statistics are ever fabricated.
    Unknown items are clearly cataloged. Punish matrix calculates from real moves.
    """
    asuka = test_db.query(Character).filter(Character.slug == "asuka").first()
    bryan = test_db.query(Character).filter(Character.slug == "bryan").first()
    arena = test_db.query(Stage).filter(Stage.slug == "the-arena").first()

    assert asuka is not None and bryan is not None and arena is not None

    payload = {
        "player_character_id": asuka.id,
        "opponent_character_id": bryan.id,
        "stage_id": arena.id
    }
    response = client.post("/api/v1/matchup/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    oa = data["overall_assessment"]
    assert oa["rating"] == "INSUFFICIENT_DATA"
    assert oa["rating_label"] == "Insufficient Data"
    assert oa["rating_color"] == "neutral"
    assert oa["confidence_level"] in ["LOW", "NONE"]
    assert oa["confidence_score"] <= 30
    assert len(oa["unknowns"]) >= 2

    # Verify no fake percentages or win rates in text
    assert "% win" not in oa["reasoning"].lower()
    assert "win rate" not in oa["reasoning"].lower()


def test_phase2_bidirectional_matchup_and_punish_logic(client: TestClient, test_db: Session):
    """
    Phase 2 Verification:
    - Bidirectional punish matrices: P1 punishing P2, P2 punishing P1.
    - Low attack punishes enforce While-Standing (WHILE_STANDING) stance requirement.
    - High-pushback attacks are tagged with HIGH pushback risk and CONDITIONAL verification status.
    - Opponent key moves and combo recommendations are properly provided.
    - Characters include hurtbox_class metadata for juggle and hitbox considerations.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    kazuya = test_db.query(Character).filter(Character.slug == "kazuya").first()
    arena = test_db.query(Stage).filter(Stage.slug == "the-arena").first()

    assert jin is not None and kazuya is not None and arena is not None

    payload = {
        "player_character_id": jin.id,
        "opponent_character_id": kazuya.id,
        "stage_id": arena.id,
        "conditions": {
            "wall_position": "OPEN",
            "heat_state": "AVAILABLE",
            "starting_distance": "MID",
            "player_side": "P1"
        }
    }
    response = client.post("/api/v1/matchup/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    # 1. Bidirectional matrices present
    assert "p1_punish_matrix" in data
    assert "p2_punish_matrix" in data
    assert len(data["p1_punish_matrix"]) > 0
    assert len(data["p2_punish_matrix"]) > 0

    # P1 punishes Kazuya's attacks
    p1_p = data["p1_punish_matrix"][0]
    assert "stance_requirement" in p1_p
    assert "verification_status" in p1_p
    assert "pushback_risk" in p1_p
    assert p1_p["stance_requirement"] in ["STANDING", "WHILE_STANDING"]

    # 2. Low moves require While-Standing (ws) punishes
    low_punishes = [p for p in data["p1_punish_matrix"] if p.get("hit_level") and "l" in p["hit_level"].lower()]
    if low_punishes:
        for lp in low_punishes:
            assert lp["stance_requirement"] == "WHILE_STANDING"
            assert "ws" in lp["recommended_punish_input"].lower() or "crouch" in lp["conditions_note"].lower()

    # 3. High pushback move evaluation
    pushback_moves = [p for p in data["p2_punish_matrix"] if p["pushback_risk"] == "HIGH"]
    for pb in pushback_moves:
        assert pb["verification_status"] == "CONDITIONAL"
        assert "pushback" in pb["conditions_note"].lower()

    # 4. Opponent key moves and combos populated
    assert "opponent_key_moves" in data and len(data["opponent_key_moves"]) > 0
    assert "opponent_suitable_combos" in data and len(data["opponent_suitable_combos"]) > 0

    # 5. Hurtbox class serialized
    assert "hurtbox_class" in data["player_character"]
    assert "hurtbox_class" in data["opponent_character"]
    assert data["player_character"]["hurtbox_class"] in ["MALE_STANDARD", "FEMALE_COMPACT", "BIG", "BEARS"]


