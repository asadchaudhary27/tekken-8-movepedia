import pytest
from fastapi.testclient import TestClient
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.move_property import MoveProperty
from backend.app.models.practice import PracticeRecord


def test_punish_options_safe_move(client: TestClient, test_db):
    """Safe moves (disadvantage > -10) must be categorized as SAFE and not punishable."""
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    feng = test_db.query(Character).filter(Character.slug == "feng").first()

    # Feng's Demon Palm df+1 is ±0 (safe)
    response = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&query=df%2B1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["options"]) >= 1
    opt = data["options"][0]
    assert opt["is_safe"] is True
    assert opt["is_punishable"] is False
    assert opt["is_launch_punishable"] is False
    assert opt["punish_status"] == "SAFE"
    assert "safe on block" in opt["why_it_works"].lower()


def test_punish_options_boundary_frame_values(client: TestClient, test_db):
    """
    Test exact boundary frame values:
    - -9 is Safe
    - -10 is Punishable (i10 Jab tier)
    - -14 is Intermediate Punishable
    - -15 or worse is Launch Punishable
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    feng = test_db.query(Character).filter(Character.slug == "feng").first()

    # Create synthetic boundary test moves on Feng
    m_minus9 = Move(
        character_id=feng.id,
        name="Boundary Safe Poke",
        original_notation="f+1",
        normalized_notation="f,1",
        startup_frames=12,
        block_advantage=-9,
        hit_advantage=2,
        damage=14,
        hit_level="m",
        verification_status="VERIFIED"
    )
    m_minus10 = Move(
        character_id=feng.id,
        name="Boundary Minus 10 Poke",
        original_notation="df+4",
        normalized_notation="df,4",
        startup_frames=12,
        block_advantage=-10,
        hit_advantage=1,
        damage=15,
        hit_level="m",
        verification_status="VERIFIED"
    )
    m_minus14 = Move(
        character_id=feng.id,
        name="Boundary Minus 14 Strike",
        original_notation="b+2",
        normalized_notation="b,2",
        startup_frames=15,
        block_advantage=-14,
        hit_advantage=3,
        damage=22,
        hit_level="m",
        verification_status="VERIFIED"
    )
    m_minus15 = Move(
        character_id=feng.id,
        name="Boundary Minus 15 Hopkick",
        original_notation="uf+4",
        normalized_notation="uf,4",
        startup_frames=15,
        block_advantage=-15,
        hit_advantage=35,
        damage=25,
        hit_level="m",
        verification_status="VERIFIED"
    )
    test_db.add_all([m_minus9, m_minus10, m_minus14, m_minus15])
    test_db.commit()

    # Test -9 is safe
    r9 = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&query=Boundary Safe Poke")
    opt9 = r9.json()["options"][0]
    assert opt9["is_safe"] is True
    assert opt9["is_punishable"] is False

    # Test -10 is punishable with jab tier
    r10 = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&query=Boundary Minus 10 Poke")
    opt10 = r10.json()["options"][0]
    assert opt10["is_punishable"] is True
    assert opt10["is_launch_punishable"] is False
    assert "i10" in opt10["punish_tier"] or "Jab" in opt10["punish_tier"]
    assert opt10["punish_startup"] <= 10

    # Test -14 is intermediate
    r14 = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&query=Boundary Minus 14 Strike")
    opt14 = r14.json()["options"][0]
    assert opt14["is_punishable"] is True
    assert opt14["is_launch_punishable"] is False
    assert opt14["punish_startup"] <= 14

    # Test -15 is launch punishable
    r15 = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&query=Boundary Minus 15 Hopkick")
    opt15 = r15.json()["options"][0]
    assert opt15["is_punishable"] is True
    assert opt15["is_launch_punishable"] is True
    assert opt15["punish_startup"] <= 15


def test_crouching_recovery_on_low_attacks(client: TestClient, test_db):
    """
    Low attacks force crouching guard; punishes MUST come from While Standing (ws)
    or Full Crouch (fc). Standing jab checks (1,2) must NOT be offered for crouching recovery.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    feng = test_db.query(Character).filter(Character.slug == "feng").first()

    # Feng's Piercing Arrow db+3 is a low attack (-15 on block)
    response = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&query=db%2B3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["options"]) >= 1
    opt = data["options"][0]
    assert opt["opponent_recovery_state"] == "CROUCHING"
    assert opt["is_punishable"] is True
    assert opt["punish_state_required"] == "WHILE_STANDING"
    assert "ws" in opt["recommended_punish_input"].lower()
    assert "while standing" in opt["why_it_works"].lower()


def test_standing_recovery_on_mid_and_high_attacks(client: TestClient, test_db):
    """Mid and high attacks allow defender to recover standing and use standing punishers."""
    kazuya = test_db.query(Character).filter(Character.slug == "kazuya").first()
    feng = test_db.query(Character).filter(Character.slug == "feng").first()

    # Feng's Iron Fortress b+1+2 is a mid attack (-19 on block)
    response = client.get(f"/api/v1/punishment/options?player_character_id={kazuya.id}&opponent_character_id={feng.id}&query=b%2B1%2B2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["options"]) >= 1
    opt = data["options"][0]
    assert opt["opponent_recovery_state"] == "STANDING"
    assert opt["is_punishable"] is True
    assert opt["is_launch_punishable"] is True
    assert opt["punish_state_required"] == "STANDING"


def test_pushback_severe_conditional(client: TestClient, test_db):
    """
    Paul's Deathfist (qcf+2) is -17 on block but has extreme pushback.
    The engine must flag this as CONDITIONAL with pushback warnings rather than guaranteed.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    paul = test_db.query(Character).filter(Character.slug == "paul").first()

    response = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={paul.id}&query=qcf%2B2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["options"]) >= 1
    opt = data["options"][0]
    assert opt["opponent_pushback"] == "HIGH"
    assert opt["punish_status"] == "CONDITIONAL"
    assert "pushback" in opt["range_condition"].lower()
    assert "pushback" in opt["why_it_works"].lower()


def test_missing_frame_data_zero_guesses(client: TestClient, test_db):
    """
    If block disadvantage is None (e.g. stances or unverified moves),
    the assistant must report UNVERIFIED with zero guessed values.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    feng = test_db.query(Character).filter(Character.slug == "feng").first()

    # Feng's Shifting Cloud Stance f+3+4 has null block frames
    response = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&query=f%2B3%2B4")
    assert response.status_code == 200
    data = response.json()
    assert len(data["options"]) >= 1
    opt = data["options"][0]
    assert opt["opponent_block_advantage"] is None
    assert opt["punish_status"] == "UNVERIFIED"
    assert opt["is_punishable"] is False
    assert opt["is_safe"] is False
    assert "never guessed" in opt["why_it_works"].lower()


def test_punishment_multi_filtering(client: TestClient, test_db):
    """Multi-faceted filtering by query, block classification, and hit level."""
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    feng = test_db.query(Character).filter(Character.slug == "feng").first()

    # 1. Filter by block_filter=PUNISHABLE
    r_pun = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&block_filter=PUNISHABLE")
    assert r_pun.status_code == 200
    for opt in r_pun.json()["options"]:
        assert opt["is_punishable"] is True

    # 2. Filter by hit_level=l
    r_low = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&hit_level=l")
    assert r_low.status_code == 200
    for opt in r_low.json()["options"]:
        assert "l" in opt["opponent_hit_level"].lower()

    # 3. Filter by classification=SAFE
    r_safe = client.get(f"/api/v1/punishment/options?player_character_id={jin.id}&opponent_character_id={feng.id}&classification=SAFE")
    assert r_safe.status_code == 200
    for opt in r_safe.json()["options"]:
        assert opt["is_safe"] is True


def test_practice_mode_attempt_and_mastery(client: TestClient, test_db):
    """
    Interactive practice trials: records success/failure,
    computes rolling mastery %, and tracks checklist stats.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    feng = test_db.query(Character).filter(Character.slug == "feng").first()
    session_token = "test_practice_session_123"

    # Step 1: Record 1 success
    p1 = {
        "session_token": session_token,
        "player_character_id": jin.id,
        "opponent_character_id": feng.id,
        "opponent_move_name": "Piercing Arrow",
        "opponent_move_input": "db+3",
        "punish_move_input": "ws4",
        "result": "SUCCESS"
    }
    r1 = client.post("/api/v1/punishment/practice/record", json=p1)
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["attempts"] == 1
    assert d1["success_count"] == 1
    assert d1["fail_count"] == 0
    assert d1["mastery_score"] == 100

    # Step 2: Record 1 failure
    p2 = {
        "session_token": session_token,
        "player_character_id": jin.id,
        "opponent_character_id": feng.id,
        "opponent_move_name": "Piercing Arrow",
        "opponent_move_input": "db+3",
        "punish_move_input": "ws4",
        "result": "FAIL"
    }
    r2 = client.post("/api/v1/punishment/practice/record", json=p2)
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["attempts"] == 2
    assert d2["success_count"] == 1
    assert d2["fail_count"] == 1
    assert d2["mastery_score"] == 50

    # Step 3: Fetch cumulative training progress
    prog = client.get(f"/api/v1/punishment/practice/progress?session_token={session_token}")
    assert prog.status_code == 200
    pdata = prog.json()
    assert pdata["total_attempts"] == 2
    assert pdata["total_successes"] == 1
    assert pdata["total_failures"] == 1
    assert pdata["overall_accuracy_pct"] == 50.0
    assert len(pdata["records"]) == 1

    # Step 4: Reset progress
    reset_res = client.post(f"/api/v1/punishment/practice/reset?session_token={session_token}")
    assert reset_res.status_code == 200

    prog_after = client.get(f"/api/v1/punishment/practice/progress?session_token={session_token}")
    assert prog_after.json()["total_attempts"] == 0
    assert len(prog_after.json()["records"]) == 0


def test_character_not_found_errors(client: TestClient):
    """Non-existent character IDs should return HTTP 404."""
    r = client.get("/api/v1/punishment/options?player_character_id=99999&opponent_character_id=1")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"]

    r2 = client.get("/api/v1/punishment/options?player_character_id=1&opponent_character_id=99999")
    assert r2.status_code == 404
    assert "not found" in r2.json()["detail"]
