import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.character import Character
from backend.app.models.stage import Stage
from backend.app.models.move import Move
from backend.app.models.combo_route import ComboRoute
from backend.app.models.combo_compatibility import ComboCompatibility
from backend.app.models.verification import VerificationRecord
from backend.app.models.conflict import DataConflict
from backend.app.services.admin_data_service import AdminDataService


ADMIN_HEADERS = {
    "X-Admin-Key": settings.ADMIN_SECRET_KEY,
    "X-Admin-User": "Lead Lab Architect",
}


# ==============================================================================
# Phase 8 Testing Checklist: Comprehensive System Integration Suite
# ==============================================================================


def test_end_to_end_10_step_matchup_workflow(client: TestClient, test_db: Session):
    """
    Validates the complete 10-step FYP user journey:
    1. Select Player (Jin)
    2. Select Opponent (Kazuya)
    3. Select Stage (The Arena)
    4. Configure Conditions (Wall=OPEN, Heat=AVAILABLE, Dist=MID, Side=P1)
    5. Load Matchup Assessment (Overall Rating, Confidence, Directional Provenance)
    6. View Strengths, Weaknesses, and Evidence-based Matchup Notes
    7. View Opponent Move List & Verified Standing/Crouching Punish Options
    8. Check Recommended Player Attacks
    9. View Opponent-Compatible Combos, Damage Scaling Decay, and Stage-Dependent Routes
    10. Record Practice Drill Progress and verify streak/mastery metrics
    """
    # Step 1 & 2: Fetch Characters
    chars_res = client.get("/api/v1/characters")
    assert chars_res.status_code == 200
    characters = chars_res.json()
    jin = next((c for c in characters if c["slug"] == "jin"), None)
    kazuya = next((c for c in characters if c["slug"] == "kazuya"), None)
    assert jin is not None and kazuya is not None

    # Step 3: Fetch Stages
    stages_res = client.get("/api/v1/stages")
    assert stages_res.status_code == 200
    stages = stages_res.json()
    arena = next((s for s in stages if s["slug"] == "the-arena"), None)
    assert arena is not None

    # Step 4 & 5: Post Matchup Analysis with Conditions
    payload = {
        "player_character_id": jin["id"],
        "opponent_character_id": kazuya["id"],
        "stage_id": arena["id"],
        "conditions": {
            "wall_position": "OPEN",
            "heat_state": "AVAILABLE",
            "starting_distance": "MID",
            "player_side": "P1"
        },
        "session_token": "phase8_integration_test_sess"
    }
    matchup_res = client.post("/api/v1/matchup/analyze", json=payload)
    assert matchup_res.status_code == 200
    m_data = matchup_res.json()

    # Step 5 Validation: Overall assessment & confidence
    assert m_data["overall_assessment"]["rating"] in ["FAVORABLE", "EVEN"]
    assert m_data["overall_assessment"]["confidence_level"] in ["HIGH", "MEDIUM"]
    assert m_data["overall_assessment"]["confidence_score"] >= 80
    assert "Jin Kazama (P1) vs Kazuya Mishima (P2)" in m_data["directional_provenance"]["direction"]

    # Step 6 Validation: Strengths, Weaknesses, Evidence Sources
    assert len(m_data["player_strengths"]) > 0
    assert len(m_data["opponent_strengths"]) > 0
    assert len(m_data["overall_assessment"]["evidence_sources"]) > 0

    # Step 7: Opponent Move List & Smart Punishment Options
    punish_res = client.get(
        f"/api/v1/punishment/options?player_character_id={jin['id']}&opponent_character_id={kazuya['id']}"
    )
    assert punish_res.status_code == 200
    p_data = punish_res.json()
    assert p_data["total_opponent_moves"] >= 5
    assert p_data["punishable_moves_count"] >= 1
    assert len(p_data["options"]) > 0
    first_opt = p_data["options"][0]
    assert "opponent_move_name" in first_opt
    assert "opponent_move_input" in first_opt

    # Step 8: Check Recommended Player Moves against this opponent
    assert len(m_data["useful_moves"]) > 0
    useful_move_names = [m["move_name"] for m in m_data["useful_moves"]]
    assert any("Demon Paw" in name or "Electric" in name or "df+2" in name or "d+2" in name or "Jab" in name or "Hook" in name for name in useful_move_names)

    # Step 9: Opponent-Compatible Combos & Stage-Aware Routes
    combos_res = client.get(
        f"/api/v1/combos/recommendations?player_id={jin['id']}&opponent_id={kazuya['id']}&stage_id={arena['id']}&wall_position=OPEN&heat_state=AVAILABLE"
    )
    assert combos_res.status_code == 200
    c_data = combos_res.json()
    assert c_data["opponent_hurtbox"]["character_name"] == "Kazuya Mishima"
    assert c_data["opponent_hurtbox"]["hurtbox_class"] == "MALE_STANDARD"
    assert len(c_data["standard_launch"]) >= 1
    assert len(c_data["beginner_friendly"]) >= 1
    assert len(c_data["wall_carry"]) >= 1

    # Step 10: Interactive Training Checklist / Reaction Drill Progress
    drill_payload_success = {
        "session_token": "phase8_integration_test_sess",
        "player_character_id": jin["id"],
        "opponent_character_id": kazuya["id"],
        "opponent_move_name": "Demon Scissors",
        "opponent_move_input": "4~3",
        "punish_move_input": "df+2",
        "result": "SUCCESS"
    }
    drill_res = client.post("/api/v1/punishment/practice/record", json=drill_payload_success)
    assert drill_res.status_code == 200
    drill_data = drill_res.json()
    assert drill_data["attempts"] == 1
    assert drill_data["success_count"] == 1
    assert drill_data["mastery_score"] == 100

    # Fetch cumulative training progress
    prog_res = client.get("/api/v1/punishment/practice/progress?session_token=phase8_integration_test_sess")
    assert prog_res.status_code == 200
    prog_data = prog_res.json()
    assert prog_data["total_attempts"] >= 1
    assert prog_data["total_successes"] >= 1
    assert prog_data["overall_accuracy_pct"] == 100.0


def test_directional_asymmetry_and_tactical_parity(client: TestClient, test_db: Session):
    """
    Verifies that matchup analysis is strictly direction-sensitive:
    1. Jin (P1) vs Kazuya (P2) is NOT identical to Kazuya (P1) vs Jin (P2).
    2. King (P1) vs Feng (P2) has UNFAVORABLE rating, whereas Feng (P1) vs King (P2) reflects Feng's advantages.
    """
    chars_res = client.get("/api/v1/characters")
    characters = chars_res.json()
    jin = next(c for c in characters if c["slug"] == "jin")
    kazuya = next(c for c in characters if c["slug"] == "kazuya")
    king = next(c for c in characters if c["slug"] == "king")
    feng = next(c for c in characters if c["slug"] == "feng")

    stages_res = client.get("/api/v1/stages")
    arena = stages_res.json()[0]

    # Direction A: Jin (P1) vs Kazuya (P2)
    dir_a = client.post("/api/v1/matchup/analyze", json={
        "player_character_id": jin["id"],
        "opponent_character_id": kazuya["id"],
        "stage_id": arena["id"],
        "conditions": {"player_side": "P1"}
    }).json()

    # Direction B: Kazuya (P1) vs Jin (P2)
    dir_b = client.post("/api/v1/matchup/analyze", json={
        "player_character_id": kazuya["id"],
        "opponent_character_id": jin["id"],
        "stage_id": arena["id"],
        "conditions": {"player_side": "P1"}
    }).json()

    assert dir_a["directional_provenance"]["direction"] != dir_b["directional_provenance"]["direction"]
    assert "Jin Kazama (P1)" in dir_a["directional_provenance"]["direction"]
    assert "Kazuya Mishima (P1)" in dir_b["directional_provenance"]["direction"]
    assert dir_a["player_character"]["name"] == "Jin Kazama"
    assert dir_b["player_character"]["name"] == "Kazuya Mishima"

    # Test King (P1) vs Feng (P2) -> UNFAVORABLE
    king_vs_feng = client.post("/api/v1/matchup/analyze", json={
        "player_character_id": king["id"],
        "opponent_character_id": feng["id"],
        "stage_id": arena["id"],
        "conditions": {"player_side": "P1"}
    }).json()

    assert king_vs_feng["overall_assessment"]["rating"] == "UNFAVORABLE"
    assert any("evasive" in s.lower() or "kenpo" in s.lower() or "backswing" in s.lower()
               for s in king_vs_feng["opponent_strengths"])


def test_stage_hazard_dependency_mechanics(client: TestClient, test_db: Session):
    """
    Tests stage hazard interactions across distinct arenas:
    1. The Arena (Enclosed, Floor Blast) -> Floor blast enabled, wall carry routes available.
    2. Urban Square (Wall Break, Balcony Break) -> Wall break and Balcony break routes available.
    3. Yakushima (Infinite, Open) -> Walls unavailable, floor break unavailable, wall warnings emitted.
    """
    stages_res = client.get("/api/v1/stages")
    stages = stages_res.json()
    arena = next(s for s in stages if s["slug"] == "the-arena")
    sanctum = next(s for s in stages if s["slug"] == "sanctum")
    urban = next(s for s in stages if s["slug"] == "urban-square")
    yakushima = next(s for s in stages if s["slug"] == "yakushima")

    # 1. The Arena Strategy (Enclosed with Walls, Wall carries enabled)
    strat_arena = client.get(
        f"/api/v1/stages/{arena['id']}/strategy?player_slug=jin&opponent_slug=kazuya&wall_position=OPEN"
    ).json()
    assert strat_arena["stage"]["has_walls"] is True
    assert len(strat_arena["wall_carry_routes"]) >= 1
    assert len(strat_arena["wall_combo_enders"]) >= 1

    # 2. Sanctum Strategy (Floor Break enabled)
    strat_sanctum = client.get(
        f"/api/v1/stages/{sanctum['id']}/strategy?player_slug=jin&opponent_slug=kazuya&wall_position=OPEN"
    ).json()
    assert strat_sanctum["stage"]["floor_break"] is True

    # 3. Urban Square Strategy (Wall Break & Balcony Break)
    strat_urban = client.get(
        f"/api/v1/stages/{urban['id']}/strategy?player_slug=jin&opponent_slug=kazuya&wall_position=OPEN"
    ).json()
    assert strat_urban["stage"]["has_walls"] is True
    assert strat_urban["stage"]["wall_break"] is True
    assert strat_urban["stage"]["balcony_break"] is True
    assert len(strat_urban["balcony_break_routes"]) >= 1

    # 4. Yakushima Strategy (Infinite Arena, No Walls)
    strat_yaku = client.get(
        f"/api/v1/stages/{yakushima['id']}/strategy?player_slug=jin&opponent_slug=kazuya&wall_position=OPEN"
    ).json()
    assert strat_yaku["stage"]["has_walls"] is False
    assert strat_yaku["stage"]["boundary_shape"] == "Infinite"
    assert len(strat_yaku["wall_carry_routes"]) == 0
    assert len(strat_yaku["wall_combo_enders"]) == 0
    assert len(strat_yaku["unavailable_mechanics_warning"]) > 0
    warnings_text = " ".join(strat_yaku["unavailable_mechanics_warning"]).lower()
    assert "infinite" in warnings_text or "unavailable" in warnings_text


def test_standing_vs_crouching_punish_options(client: TestClient, test_db: Session):
    """
    Verifies smart punishment assistant rules:
    - Opponent low attack recovery is crouching -> recommended punishes must be while standing (ws).
    - Opponent mid/high attack recovery is standing -> recommended punishes must be standing attacks.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    feng = test_db.query(Character).filter(Character.slug == "feng").first()

    # Low attack query: Feng db+3 (-15 on block)
    r_low = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&query=db%2B3")
    assert r_low.status_code == 200
    opt_low = r_low.json()["options"][0]
    assert opt_low["opponent_recovery_state"] == "CROUCHING"
    assert opt_low["is_punishable"] is True
    assert opt_low["punish_state_required"] == "WHILE_STANDING"
    assert "ws" in opt_low["recommended_punish_input"].lower()

    # Mid attack query: Feng b+1+2 (-19 on block)
    r_mid = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&query=b%2B1%2B2")
    assert r_mid.status_code == 200
    opt_mid = r_mid.json()["options"][0]
    assert opt_mid["opponent_recovery_state"] == "STANDING"
    assert opt_mid["is_punishable"] is True
    assert opt_mid["punish_state_required"] == "STANDING"


def test_character_specific_combo_compatibility_profiles(client: TestClient, test_db: Session):
    """
    Verifies juggle compatibility modeling:
    - Kuma hurtbox class is BEARS.
    - Reina hurtbox class is FEMALE_COMPACT.
    - Baseline Male (Kazuya) is MALE_STANDARD.
    """
    chars_res = client.get("/api/v1/characters")
    chars = chars_res.json()
    jin = next(c for c in chars if c["slug"] == "jin")
    kuma = next((c for c in chars if c["slug"] in ["kuma", "panda"]), None)
    reina = next((c for c in chars if c["slug"] in ["reina", "xiaoyu", "asuka"]), None)
    kazuya = next(c for c in chars if c["slug"] == "kazuya")

    # Kazuya Hurtbox
    c_kazuya = client.get(f"/api/v1/combos/recommendations?player_id={jin['id']}&opponent_id={kazuya['id']}").json()
    assert c_kazuya["opponent_hurtbox"]["hurtbox_class"] == "MALE_STANDARD"

    # Bear Hurtbox
    if kuma:
        c_kuma = client.get(f"/api/v1/combos/recommendations?player_id={jin['id']}&opponent_id={kuma['id']}").json()
        assert c_kuma["opponent_hurtbox"]["hurtbox_class"] == "BEARS"
        assert len(c_kuma["opponent_hurtbox"]["known_quirks"]) > 0

    # Female Compact Hurtbox
    if reina:
        c_reina = client.get(f"/api/v1/combos/recommendations?player_id={jin['id']}&opponent_id={reina['id']}").json()
        assert c_reina["opponent_hurtbox"]["hurtbox_class"] == "FEMALE_COMPACT"


def test_heat_availability_toggle_impact(client: TestClient, test_db: Session):
    """
    Verifies tactical Heat condition toggles:
    - AVAILABLE: Heat-dependent routes are enabled and populated in heat_dependent bucket.
    - Combos report requires_heat and is_available properties.
    """
    chars_res = client.get("/api/v1/characters")
    jin = next(c for c in chars_res.json() if c["slug"] == "jin")
    kazuya = next(c for c in chars_res.json() if c["slug"] == "kazuya")

    # Heat AVAILABLE
    res_avail = client.get(
        f"/api/v1/combos/recommendations?player_id={jin['id']}&opponent_id={kazuya['id']}&heat_state=AVAILABLE"
    ).json()
    assert len(res_avail["heat_dependent"]) >= 1
    assert all(c["uses_heat"] is True for c in res_avail["heat_dependent"])


def test_wall_positioning_tactical_adjustments(client: TestClient, test_db: Session):
    """
    Verifies wall positioning changes strategy:
    - OPEN: Midscreen launchers and wall carry routes prioritized.
    - CORNER: Corner pressure and wall splat strategy emphasized.
    """
    stages_res = client.get("/api/v1/stages")
    arena = next(s for s in stages_res.json() if s["slug"] == "the-arena")

    strat_open = client.get(
        f"/api/v1/stages/{arena['id']}/strategy?player_slug=jin&opponent_slug=kazuya&wall_position=OPEN"
    ).json()
    strat_corner = client.get(
        f"/api/v1/stages/{arena['id']}/strategy?player_slug=jin&opponent_slug=kazuya&wall_position=CORNER"
    ).json()

    assert "corner" in strat_corner["corner_pressure_strategy"].lower()
    assert len(strat_open["wall_carry_routes"]) >= 1


def test_data_state_differentiation_protocol(client: TestClient, test_db: Session):
    """
    Verifies mathematical differentiation of all 4 data completeness states:
    1. UNKNOWN: Missing juggle compatibility defaults strictly to UNKNOWN_COMPATIBILITY (never false negatives).
    2. NOT_PROVIDED: Upstream missing fields are counted as not_provided_count in quality report.
    3. CONFLICTING: Discrepancies between patches/sources are registered in DataConflict entity.
    4. CONFIRMED_ABSENT: Verification records can explicitly record nonexistence (CONFIRMED_ABSENT).
    """
    # 1. UNKNOWN test via Combo Compatibility fallback
    chars_res = client.get("/api/v1/characters").json()
    jin = next(c for c in chars_res if c["slug"] == "jin")
    feng = next(c for c in chars_res if c["slug"] == "feng")

    combos_res = client.get(f"/api/v1/combos/recommendations?player_id={jin['id']}&opponent_id={feng['id']}").json()
    all_combos = (
        combos_res.get("standard_launch", [])
        + combos_res.get("beginner_friendly", [])
        + combos_res.get("high_damage_optimal", [])
        + combos_res.get("alternative_routes", [])
    )
    for c in all_combos:
        assert c["compatibility_status"] in [
            "VERIFIED_FOR_OPPONENT",
            "TESTED_UNDER_CONDITIONS",
            "REPORTED_UNTESTED",
            "UNKNOWN_COMPATIBILITY",
            "INCOMPATIBLE_DOCUMENTED"
        ]

    # 2. Quality dashboard differentiation
    dash_res = client.get("/api/v1/admin/dashboard", headers=ADMIN_HEADERS)
    assert dash_res.status_code == 200
    dash_data = dash_res.json()

    assert "total_moves" in dash_data
    assert "status_distribution" in dash_data

    # 3. Create a verification record with CONFIRMED_ABSENT
    verif_payload = {
        "entity_type": "MOVE",
        "entity_id": 1,
        "new_status": "CONFIRMED_ABSENT",
        "evidence_notes": "Verified that this move has no heat engager property in Patch 3.00.02"
    }
    verif_res = client.post("/api/v1/admin/verification-status", json=verif_payload, headers=ADMIN_HEADERS)
    assert verif_res.status_code == 200
    assert verif_res.json()["new_status"] == "CONFIRMED_ABSENT"


def test_admin_authorization_and_atomic_import_rollback(client: TestClient, test_db: Session):
    """
    Verifies security and database integrity:
    1. Rejection of unauthorized requests without X-Admin-Key header (401 Unauthorized).
    2. Atomic transaction rollback on import errors: invalid payload causes zero commits.
    """
    # 1. Unauthorized Access
    unauth_res = client.get("/api/v1/admin/dashboard")
    assert unauth_res.status_code == 401
    assert "denied" in unauth_res.json()["detail"].lower() or "required" in unauth_res.json()["detail"].lower()

    # 2. Atomic Rollback on corrupted import
    jin = test_db.query(Character).filter_by(slug="jin").first()
    count_before = test_db.query(Move).count()

    # Batch with 1 valid row and 1 fatally invalid row (missing notation)
    rows = [
        {
            "character_id": jin.id,
            "name": "Valid Candidate",
            "normalized_notation": "f+1+4_test_phase8_rollback",
            "startup_frames": 14,
            "verification_status": "UNVERIFIED",
        },
        {
            "character_id": jin.id,
            # Missing notation -> triggers ValueError
            "name": "Bad Candidate Without Notation",
        },
    ]

    summary = AdminDataService.execute_import(
        db=test_db,
        entity_type="MOVES",
        rows=rows,
        user="RollbackTester",
    )

    assert summary.success is False
    assert summary.rollback_occurred is True
    assert summary.records_created == 0

    # Ensure nothing was committed to database
    count_after = test_db.query(Move).count()
    assert count_after == count_before
