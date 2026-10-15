"""
Unit and Integration Tests for Phase 4: Stage-Aware Strategy Engine.
Verifies stage geometry handling, hazard validation, combo category filtering,
tactical report generation, infinite-stage safety, and frame-data immutability.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.models.stage import Stage
from backend.app.models.character import Character
from backend.app.models.move import Move
from backend.app.models.combo_route import ComboRoute


def test_stage_strategy_yakushima_infinite(client: TestClient, test_db):
    """
    On infinite stages (Yakushima, has_walls=False):
    - Wall carries, wall-splats, and wall-combo enders must be UNAVAILABLE.
    - Zero fabricated geometry (geometry_available must be False).
    - Environmental breaks (wall/floor/balcony) must be reported as UNAVAILABLE.
    - Midscreen combos must still be available.
    """
    stage = test_db.query(Stage).filter(Stage.slug == "yakushima").first()
    assert stage is not None
    assert stage.has_walls is False

    response = client.get(f"/api/v1/stages/{stage.id}/strategy?player_slug=jin&opponent_slug=kazuya")
    assert response.status_code == 200
    report = response.json()

    # Geometry checks: No fabricated map for unmapped/infinite stage
    assert report["geometry_available"] is False
    assert report["geometry_data"] is None

    # Wall availability status
    assert "UNAVAILABLE" in report["wall_availability_status"]

    # Combo filtering: No wall combos on infinite stage
    assert len(report["wall_carry_routes"]) == 0
    assert len(report["wall_combo_enders"]) == 0
    assert len(report["wall_break_routes"]) == 0
    assert len(report["floor_break_routes"]) == 0
    assert len(report["balcony_break_routes"]) == 0

    # Midscreen combos must still be available
    assert len(report["midscreen_combos"]) >= 1
    for combo in report["midscreen_combos"]:
        assert combo["combo_type"] == "MIDSCREEN" or not combo["uses_wall"]

    # Warnings must explicitly explain that walls and breaks are unavailable
    warnings_text = " ".join(report["unavailable_mechanics_warning"]).lower()
    assert "infinite" in warnings_text
    assert "unavailable" in warnings_text


def test_stage_strategy_the_arena_enclosed(client: TestClient, test_db):
    """
    On standard enclosed stages without destructible hazards (The Arena):
    - Verified geometry is available (Octagonal).
    - Wall carries and wall combo enders are available.
    - Wall breaks, floor breaks, and balcony breaks are reported as UNAVAILABLE.
    """
    stage = test_db.query(Stage).filter(Stage.slug == "the-arena").first()
    assert stage is not None
    assert stage.has_walls is True
    assert stage.wall_break is False

    response = client.get(f"/api/v1/stages/{stage.id}/strategy?player_slug=jin&opponent_slug=kazuya")
    assert response.status_code == 200
    report = response.json()

    # Geometry is verified
    assert report["geometry_available"] is True
    assert report["geometry_data"] is not None
    assert report["geometry_data"]["shape"] == "Octagonal"
    assert len(report["geometry_data"]["elements"]) >= 1

    # Wall availability
    assert "AVAILABLE" in report["wall_availability_status"]

    # Wall carries and wall enders exist
    assert len(report["wall_carry_routes"]) >= 1
    assert len(report["wall_combo_enders"]) >= 1

    # Environmental breaks do not exist on The Arena
    assert len(report["wall_break_routes"]) == 0
    assert len(report["floor_break_routes"]) == 0
    assert len(report["balcony_break_routes"]) == 0

    # Warnings reflect unavailable breaks
    warnings_text = " ".join(report["unavailable_mechanics_warning"]).lower()
    assert "wall break is unavailable" in warnings_text
    assert "balcony break is unavailable" in warnings_text


def test_stage_strategy_urban_square_multi_hazard(client: TestClient, test_db):
    """
    On multi-hazard stages (Urban Square):
    - Has wall break and balcony break.
    - Verified geometry is available (Rectangular).
    - Balcony break combo routes are populated for Jin.
    - Interaction descriptions are populated.
    """
    stage = test_db.query(Stage).filter(Stage.slug == "urban-square").first()
    assert stage is not None
    assert stage.wall_break is True
    assert stage.balcony_break is True

    response = client.get(f"/api/v1/stages/{stage.id}/strategy?player_slug=jin")
    assert response.status_code == 200
    report = response.json()

    assert report["geometry_available"] is True
    assert report["stage"]["balcony_break"] is True
    assert report["balcony_break_interaction"] is not None
    assert len(report["balcony_break_routes"]) >= 1
    balcony_combo = report["balcony_break_routes"][0]
    assert balcony_combo["combo_type"] == "BALCONY_BREAK"
    assert balcony_combo["is_stage_dependent"] is True


def test_stage_strategy_sanctum_floor_break(client: TestClient, test_db):
    """
    On Sanctum (Ancient ruins):
    - Floor break is active over the altar.
    - Floor break interaction description is populated.
    - Floor break combo route for Jin is present.
    """
    stage = test_db.query(Stage).filter(Stage.slug == "sanctum").first()
    assert stage is not None
    assert stage.floor_break is True

    response = client.get(f"/api/v1/stages/{stage.id}/strategy?player_slug=jin")
    assert response.status_code == 200
    report = response.json()

    assert report["stage"]["floor_break"] is True
    assert report["floor_break_interaction"] is not None
    assert len(report["floor_break_routes"]) >= 1
    floor_combo = report["floor_break_routes"][0]
    assert floor_combo["combo_type"] == "FLOOR_BREAK"
    assert floor_combo["is_stage_dependent"] is True


def test_combos_api_endpoint_filters(client: TestClient, test_db):
    """
    Test GET /api/v1/combos with various tactical filters:
    - No filter (returns all combos)
    - By combo_type (MIDSCREEN, WALL_CARRY, WALL_COMBO, BALCONY_BREAK, etc.)
    - By counter-hit requirement
    - By heat requirement
    - By stage_slug
    - By character_slug
    """
    # 1. All combos
    r_all = client.get("/api/v1/combos")
    assert r_all.status_code == 200
    all_combos = r_all.json()
    assert len(all_combos) >= 20

    # 2. Filter by combo_type = WALL_CARRY
    r_carry = client.get("/api/v1/combos?combo_type=WALL_CARRY")
    assert r_carry.status_code == 200
    carry_combos = r_carry.json()
    assert len(carry_combos) >= 1
    for c in carry_combos:
        assert c["combo_type"] == "WALL_CARRY"

    # 3. Filter by combo_type = BALCONY_BREAK
    r_balcony = client.get("/api/v1/combos?combo_type=BALCONY_BREAK")
    assert r_balcony.status_code == 200
    balcony_combos = r_balcony.json()
    assert len(balcony_combos) >= 1
    for c in balcony_combos:
        assert c["combo_type"] == "BALCONY_BREAK"

    # 4. Filter by requires_ch = true
    r_ch = client.get("/api/v1/combos?requires_ch=true")
    assert r_ch.status_code == 200
    ch_combos = r_ch.json()
    assert len(ch_combos) >= 1
    for c in ch_combos:
        assert c["requires_counter_hit"] is True

    # 5. Filter by requires_heat = true
    r_heat = client.get("/api/v1/combos?requires_heat=true")
    assert r_heat.status_code == 200
    heat_combos = r_heat.json()
    assert len(heat_combos) >= 1
    for c in heat_combos:
        assert c["uses_heat"] is True

    # 6. Filter by character_slug = jin
    r_jin = client.get("/api/v1/combos?character_slug=jin")
    assert r_jin.status_code == 200
    jin_combos = r_jin.json()
    assert len(jin_combos) >= 5
    for c in jin_combos:
        assert c["character"]["slug"] == "jin"


def test_stage_strategy_api_endpoint_corner_condition(client: TestClient, test_db):
    """
    Test wall_position conditions:
    When wall_position is 'CORNER', corner_pressure_strategy reflects high pressure.
    """
    stage = test_db.query(Stage).filter(Stage.slug == "the-arena").first()
    response = client.get(
        f"/api/v1/stages/{stage.id}/strategy?player_slug=jin&opponent_slug=kazuya&wall_position=CORNER"
    )
    assert response.status_code == 200
    report = response.json()
    assert "corner" in report["corner_pressure_strategy"].lower()
    assert "50-50" in report["corner_pressure_strategy"].lower()


def test_stage_strategy_api_invalid_inputs(client: TestClient, test_db):
    """Invalid stage ID or character slug must return 404 with meaningful error."""
    # Invalid stage
    r_stage = client.get("/api/v1/stages/999999/strategy?player_slug=jin")
    assert r_stage.status_code == 404
    assert "not found" in r_stage.json()["detail"].lower()

    # Invalid player
    stage = test_db.query(Stage).first()
    r_char = client.get(f"/api/v1/stages/{stage.id}/strategy?player_slug=nonexistent_character")
    assert r_char.status_code == 404
    assert "not found" in r_char.json()["detail"].lower()


def test_stage_switching_does_not_mutate_frame_data(client: TestClient, test_db):
    """
    DATA INTEGRITY & ISOLATION RULE:
    Changing stages or retrieving stage-specific combo strategies
    must NEVER alter unrelated character move frame data.
    """
    jin = test_db.query(Character).filter(Character.slug == "jin").first()
    arena = test_db.query(Stage).filter(Stage.slug == "the-arena").first()
    yakushima = test_db.query(Stage).filter(Stage.slug == "yakushima").first()

    # 1. Query baseline frame data for Jin's EWGF
    ewgf_before = test_db.query(Move).filter(
        Move.character_id == jin.id,
        Move.original_notation == "f,n,d,df+2"
    ).first()
    assert ewgf_before is not None
    orig_startup = ewgf_before.startup_frames
    orig_block = ewgf_before.block_advantage
    orig_damage = ewgf_before.damage

    # 2. Run strategy analysis on The Arena
    r_arena = client.get(f"/api/v1/stages/{arena.id}/strategy?player_slug=jin")
    assert r_arena.status_code == 200

    # 3. Run strategy analysis on Yakushima
    r_yakushima = client.get(f"/api/v1/stages/{yakushima.id}/strategy?player_slug=jin")
    assert r_yakushima.status_code == 200

    # 4. Re-query baseline frame data for Jin's EWGF
    test_db.expire_all()
    ewgf_after = test_db.query(Move).filter(
        Move.character_id == jin.id,
        Move.original_notation == "f,n,d,df+2"
    ).first()

    assert ewgf_after.startup_frames == orig_startup
    assert ewgf_after.block_advantage == orig_block
    assert ewgf_after.damage == orig_damage
