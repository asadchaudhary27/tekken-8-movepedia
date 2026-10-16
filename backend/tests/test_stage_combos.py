"""
Integration and Unit Tests for Phase 5: Stage Selector and Stage-Aware Combo Engine.
Verifies stage properties, hazard checks, alternative route links, P1/P2 independence,
and state synchronization guarantees.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.models.stage import Stage
from backend.app.models.character import Character
from backend.app.models.combo_route import ComboRoute


def test_stage_combo_recommendations_yakushima_infinite(client: TestClient, test_db):
    """
    On Yakushima (Infinite battleground, has_walls=False):
    - stage_has_walls must be False
    - stage_warnings must explain that walls and breaks are unavailable
    - Wall-dependent combos must have is_stage_compatible=False
    - Incompatible combos offer viable alternative midscreen routes
    """
    stage = test_db.query(Stage).filter(Stage.slug == "yakushima").first()
    assert stage is not None
    assert stage.has_walls is False

    response = client.get(
        f"/api/v1/combos/recommendations?player_slug=jin&opponent_slug=kazuya&stage_slug={stage.slug}"
    )
    assert response.status_code == 200
    report = response.json()

    assert report["stage_name"] == stage.name
    assert report["stage_has_walls"] is False
    assert len(report["stage_warnings"]) >= 1
    assert any("infinite" in w.lower() for w in report["stage_warnings"])

    # Verify that combos requiring walls are flagged unavailable or alternative available
    unmet_count = report["stage_unmet_combos_count"]
    assert unmet_count >= 1

    # Check wall combos in wall_combo category
    for c in report["wall_combo"]:
        if c["uses_wall"] or c["combo_type"] == "WALL_COMBO":
            assert c["is_stage_compatible"] is False
            assert c["stage_compatibility_status"] in ["UNAVAILABLE_ON_STAGE", "ALTERNATIVE_AVAILABLE"]
            assert "infinite" in c["stage_incompatibility_reason"].lower() or "wall" in c["stage_incompatibility_reason"].lower()
            if c["stage_compatibility_status"] == "ALTERNATIVE_AVAILABLE":
                assert c["alternative_route_id"] is not None
                assert c["alternative_route_title"] is not None


def test_stage_combo_recommendations_urban_square_multi_hazard(client: TestClient, test_db):
    """
    On Urban Square:
    - stage_has_walls is True
    - wall_break and balcony_break supported
    - Balcony break combo is compatible
    """
    stage = test_db.query(Stage).filter(Stage.slug == "urban-square").first()
    assert stage is not None
    assert stage.balcony_break is True
    assert stage.wall_break is True

    response = client.get(
        f"/api/v1/combos/recommendations?player_slug=jin&opponent_slug=kazuya&stage_slug={stage.slug}"
    )
    assert response.status_code == 200
    report = response.json()

    assert report["stage_has_walls"] is True
    assert report["stage_wall_break_supported"] is True
    assert report["stage_balcony_break_supported"] is True

    # Check that balcony break routes for Jin are stage-compatible on Urban Square
    balcony_combos = [c for c in report["stage_break"] if c["combo_type"] == "BALCONY_BREAK"]
    if balcony_combos:
        for bc in balcony_combos:
            assert bc["is_stage_compatible"] is True
            assert bc["stage_compatibility_status"] == "SUPPORTED"


def test_stage_combo_recommendations_sanctum_floor_break(client: TestClient, test_db):
    """
    On Sanctum:
    - Floor break is active
    - Balcony break is NOT active
    - Balcony break combo must be flagged incompatible on Sanctum
    """
    stage = test_db.query(Stage).filter(Stage.slug == "sanctum").first()
    assert stage is not None
    assert stage.floor_break is True
    assert stage.balcony_break is False

    response = client.get(
        f"/api/v1/combos/recommendations?player_slug=jin&opponent_slug=kazuya&stage_slug={stage.slug}"
    )
    assert response.status_code == 200
    report = response.json()

    assert report["stage_floor_break_supported"] is True
    assert report["stage_balcony_break_supported"] is False

    # Balcony break combo should be flagged incompatible on Sanctum
    balcony_combos = [c for c in report["stage_break"] if c["combo_type"] == "BALCONY_BREAK"]
    if balcony_combos:
        for bc in balcony_combos:
            assert bc["is_stage_compatible"] is False
            assert bc["stage_compatibility_status"] in ["UNAVAILABLE_ON_STAGE", "ALTERNATIVE_AVAILABLE"]
            assert "balcony" in bc["stage_incompatibility_reason"].lower()


def test_stage_combos_independent_p1_p2(client: TestClient, test_db):
    """
    Verifies that P1 and P2 maintain completely independent character identity
    and recommendations when evaluated under the same stage.
    """
    stage = test_db.query(Stage).filter(Stage.slug == "the-arena").first()
    assert stage is not None

    # Fetch P1 (Jin vs Kazuya)
    r1 = client.get(
        f"/api/v1/combos/recommendations?player_slug=jin&opponent_slug=kazuya&stage_id={stage.id}"
    )
    assert r1.status_code == 200
    p1_data = r1.json()

    # Fetch P2 (Kazuya vs Jin)
    r2 = client.get(
        f"/api/v1/combos/recommendations?player_slug=kazuya&opponent_slug=jin&stage_id={stage.id}"
    )
    assert r2.status_code == 200
    p2_data = r2.json()

    # Verify P1 identity
    assert p1_data["player_character"]["slug"] == "jin"
    assert p1_data["opponent_character"]["slug"] == "kazuya"
    assert p1_data["stage_name"] == stage.name

    # Verify P2 identity
    assert p2_data["player_character"]["slug"] == "kazuya"
    assert p2_data["opponent_character"]["slug"] == "jin"
    assert p2_data["stage_name"] == stage.name

    # Check distinct combo routes (P1 combos belong to Jin, P2 combos belong to Kazuya)
    if p1_data["standard_launch"]:
        for c in p1_data["standard_launch"]:
            assert c["character_id"] == p1_data["player_character"]["id"]

    if p2_data["standard_launch"]:
        for c in p2_data["standard_launch"]:
            assert c["character_id"] == p2_data["player_character"]["id"]


def test_stage_switching_preserves_character_state(client: TestClient, test_db):
    """
    Verifies that changing stage parameters does not reset player/opponent IDs
    or corrupt combo payloads.
    """
    stages = test_db.query(Stage).all()
    assert len(stages) >= 3

    for stg in stages[:3]:
        r = client.get(
            f"/api/v1/combos/recommendations?player_slug=jin&opponent_slug=kazuya&stage_id={stg.id}"
        )
        assert r.status_code == 200
        data = r.json()
        assert data["player_character"]["slug"] == "jin"
        assert data["opponent_character"]["slug"] == "kazuya"
        assert data["stage_name"] == stg.name
        assert data["total_combos_analyzed"] >= 1
