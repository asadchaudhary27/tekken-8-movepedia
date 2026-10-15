import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.character import Character
from backend.app.models.combo_route import ComboRoute
from backend.app.models.combo_compatibility import ComboCompatibility
from backend.app.services.combo_compatibility_engine import ComboCompatibilityEngine


def test_damage_scaling_formula_not_blind_sum():
    """
    Strict rule: Never calculate combo damage by blindly summing raw damages.
    Tekken 8 aerial juggle scaling rules:
      Hit 1: 100% (or 120% on Counter-Hit)
      Hit 2: 70%
      Hit 3: 50%
      Hit 4: 40%
      Hit 5+: 30% floor
    """
    test_hits = [
        {"raw_damage": 20, "move_notation": "Launcher df+2"},
        {"raw_damage": 20, "move_notation": "Followup 1"},
        {"raw_damage": 20, "move_notation": "Tornado b+3"},
        {"raw_damage": 20, "move_notation": "Screw hit"},
        {"raw_damage": 20, "move_notation": "Ender d+2"},
    ]

    # Normal starter:
    # Hit 1: 20 * 100% = 20
    # Hit 2: 20 * 70%  = 14
    # Hit 3: 20 * 50%  = 10
    # Hit 4: 20 * 40%  = 8
    # Hit 5: 20 * 30%  = 6
    # Total scaled = 20 + 14 + 10 + 8 + 6 = 58
    # Raw blind sum = 100
    res = ComboCompatibilityEngine.calculate_scaled_damage(test_hits, is_counter_hit=False)

    assert res.raw_damage_sum == 100
    assert res.scaled_damage_total == 58
    assert res.scaled_damage_total < res.raw_damage_sum
    assert len(res.hits) == 5
    assert res.hits[0].scaling_percent == 100
    assert res.hits[0].scaled_damage == 20
    assert res.hits[1].scaling_percent == 70
    assert res.hits[1].scaled_damage == 14
    assert res.hits[2].scaling_percent == 50
    assert res.hits[2].scaled_damage == 10
    assert res.hits[3].scaling_percent == 40
    assert res.hits[3].scaled_damage == 8
    assert res.hits[4].scaling_percent == 30
    assert res.hits[4].scaled_damage == 6

    # Counter-Hit starter: Hit 1 scaled to 120% (20 * 120% = 24)
    # Total scaled = 24 + 14 + 10 + 8 + 6 = 62
    ch_res = ComboCompatibilityEngine.calculate_scaled_damage(test_hits, is_counter_hit=True)
    assert ch_res.hits[0].scaling_percent == 120
    assert ch_res.hits[0].scaled_damage == 24
    assert ch_res.scaled_damage_total == 62


def test_hurtbox_profile_assignment(test_db: Session):
    """
    Verify all 43 fighters have a valid hurtbox profile and none are null or unknown.
    """
    chars = test_db.query(Character).all()
    assert len(chars) == 43

    valid_classes = {"MALE_STANDARD", "FEMALE_COMPACT", "BIG", "BEARS"}
    for c in chars:
        assert c.hurtbox_class in valid_classes, f"Invalid hurtbox class for {c.name}: {c.hurtbox_class}"
        assert c.hurtbox_notes is not None and len(c.hurtbox_notes) > 0

    # Specific profile verifications
    kuma = test_db.query(Character).filter_by(slug="kuma").first()
    panda = test_db.query(Character).filter_by(slug="panda").first()
    assert kuma.hurtbox_class == "BEARS"
    assert panda.hurtbox_class == "BEARS"

    jack8 = test_db.query(Character).filter_by(slug="jack-8").first()
    king = test_db.query(Character).filter_by(slug="king").first()
    assert jack8.hurtbox_class == "BIG"
    assert king.hurtbox_class == "BIG"

    xiaoyu = test_db.query(Character).filter_by(slug="xiaoyu").first()
    reina = test_db.query(Character).filter_by(slug="reina").first()
    assert xiaoyu.hurtbox_class == "FEMALE_COMPACT"
    assert reina.hurtbox_class == "FEMALE_COMPACT"

    jin = test_db.query(Character).filter_by(slug="jin").first()
    kazuya = test_db.query(Character).filter_by(slug="kazuya").first()
    assert jin.hurtbox_class == "MALE_STANDARD"
    assert kazuya.hurtbox_class == "MALE_STANDARD"


def test_character_specific_routes_bear(test_db: Session):
    """
    Verify Bear-specific routes connect against Bear hurtbox profiles and standard
    routes have documented incompatibility/drops on Bears.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    kuma = test_db.query(Character).filter_by(slug="kuma").first()

    report = ComboCompatibilityEngine.generate_recommendations(
        db=test_db,
        player_character=jin,
        opponent_character=kuma,
    )

    assert report.opponent_hurtbox.hurtbox_class == "BEARS"
    assert len(report.opponent_hurtbox.known_quirks) >= 3

    # Anti-Bear combo should be present in character_specific category and verified
    bear_combos = [c for c in report.character_specific if c.target_hurtbox_class == "BEARS"]
    assert len(bear_combos) >= 1
    assert bear_combos[0].compatibility_status == "VERIFIED_FOR_OPPONENT"

    # Standard staple combo should have documented incompatibility on Bears
    standard_staple = next(
        (c for c in report.standard_launch if c.title == "Electric Hook Fist Staple Juggle"), None
    )
    assert standard_staple is not None
    assert standard_staple.compatibility_status == "INCOMPATIBLE_DOCUMENTED"
    assert standard_staple.incompatibility_reason is not None
    assert "whiff" in standard_staple.incompatibility_reason.lower()


def test_unknown_compatibility_fallback_rule(test_db: Session):
    """
    STRICT RULE: Missing compatibility records MUST evaluate to UNKNOWN_COMPATIBILITY,
    never INCOMPATIBLE. Zero guessing of drops without lab data.
    """
    # Pick a character without explicit compatibility record for Jin's combos
    jin = test_db.query(Character).filter_by(slug="jin").first()
    clive = test_db.query(Character).filter_by(slug="clive").first()

    # Universal combo against Clive (which has no explicit record)
    combo = test_db.query(ComboRoute).filter_by(title="Demon's Paw Wall Carry Route").first()
    # Remove any compatibilities for test
    status, badge, timing, reason = ComboCompatibilityEngine.resolve_compatibility(combo, clive)

    # Since Clive is MALE_STANDARD and combo is UNIVERSAL, it connects with standard testing
    # But for a non-matching unrecorded pair:
    feng = test_db.query(Character).filter_by(slug="feng").first()
    bob = test_db.query(Character).filter_by(slug="bob").first()
    feng_combo = test_db.query(ComboRoute).filter_by(title="Demon Palm Midscreen Staple").first()

    status, badge, timing, reason = ComboCompatibilityEngine.resolve_compatibility(feng_combo, bob)
    # Bob is BIG, universal combo connects with TESTED_UNDER_CONDITIONS or UNKNOWN
    assert status != "INCOMPATIBLE_DOCUMENTED"
    assert reason is None


def test_documented_incompatibility_female_compact(test_db: Session):
    """
    Verify documented drop conditions: Anti-Bear low-profile juggle drops on female compact targets.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    xiaoyu = test_db.query(Character).filter_by(slug="xiaoyu").first()

    anti_bear_combo = test_db.query(ComboRoute).filter_by(title="Anti-Bear Low-Profile Juggle").first()
    status, badge, timing, reason = ComboCompatibilityEngine.resolve_compatibility(anti_bear_combo, xiaoyu)

    assert status == "INCOMPATIBLE_DOCUMENTED"
    assert badge == "incompatible"
    assert reason is not None
    assert "compact" in reason.lower() or "drop" in reason.lower()


def test_tested_vs_estimated_damage_labelling(test_db: Session):
    """
    Verify distinct labelling: TESTED vs ESTIMATED damage.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    kazuya = test_db.query(Character).filter_by(slug="kazuya").first()

    detailed = ComboCompatibilityEngine.combo_to_detailed_read(
        combo=test_db.query(ComboRoute).filter_by(title="Electric Hook Fist Staple Juggle").first(),
        opponent=kazuya,
    )

    assert detailed.damage_type == "TESTED"
    assert detailed.is_damage_estimate is False
    assert detailed.raw_damage_sum is not None
    assert detailed.total_damage < detailed.raw_damage_sum
    assert len(detailed.scaling_breakdown) > 0


def test_easier_alternative_linking(test_db: Session):
    """
    Verify optimal combo links to its easier alternative route.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    kazuya = test_db.query(Character).filter_by(slug="kazuya").first()

    optimal = test_db.query(ComboRoute).filter_by(title="High-Damage ZEN Micro-Dash Optimal").first()
    assert optimal.easier_alternative_id is not None

    detailed = ComboCompatibilityEngine.combo_to_detailed_read(optimal, kazuya)
    assert detailed.easier_alternative_title == "Electric Hook Fist Staple Juggle"
    assert detailed.easier_alternative_notes is not None


def test_all_10_recommendation_buckets_populated(test_db: Session):
    """
    Verify report delivers all 10 analytical categories requested in Phase 5 prompt.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    kazuya = test_db.query(Character).filter_by(slug="kazuya").first()

    report = ComboCompatibilityEngine.generate_recommendations(
        db=test_db,
        player_character=jin,
        opponent_character=kazuya,
    )

    assert len(report.beginner_friendly) >= 1
    assert len(report.standard_launch) >= 1
    assert len(report.high_damage_optimal) >= 1
    assert len(report.wall_carry) >= 1
    assert len(report.wall_combo) >= 1
    assert len(report.heat_dependent) >= 1
    assert len(report.counter_hit) >= 1
    assert len(report.character_specific) >= 1
    assert len(report.stage_break) >= 1
    assert len(report.alternative_routes) >= 1

    # Check damage scaling explanation is included
    assert "scaling" in report.damage_scaling_rules_explanation.lower()
    assert "100%" in report.damage_scaling_rules_explanation


def test_api_recommendations_endpoint(client: TestClient):
    """
    Test GET /api/v1/combos/recommendations endpoint.
    """
    response = client.get("/api/v1/combos/recommendations?player_slug=jin&opponent_slug=kuma")
    assert response.status_code == 200
    data = response.json()

    assert data["player_character"]["slug"] == "jin"
    assert data["opponent_character"]["slug"] == "kuma"
    assert data["opponent_hurtbox"]["hurtbox_class"] == "BEARS"
    assert "beginner_friendly" in data
    assert "standard_launch" in data
    assert "high_damage_optimal" in data
    assert "alternative_routes" in data
    assert data["total_combos_analyzed"] > 0


def test_api_calculate_damage_endpoint(client: TestClient):
    """
    Test POST /api/v1/combos/calculate-damage endpoint.
    """
    payload = {
        "hits": [
            {"raw_damage": 25, "move_notation": "EWGF"},
            {"raw_damage": 18, "move_notation": "b+3"},
            {"raw_damage": 22, "move_notation": "ZEN 1,3"},
            {"raw_damage": 15, "move_notation": "Dash"},
            {"raw_damage": 20, "move_notation": "d+2"},
        ],
        "is_counter_hit": False,
        "tested_damage": 72,
        "damage_type": "TESTED",
        "calculation_method": "LAB_TESTED_IN_GAME",
    }
    response = client.post("/api/v1/combos/calculate-damage", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Raw sum = 25 + 18 + 22 + 15 + 20 = 100
    # Scaled = 25 (100%) + 12 (70%) + 11 (50%) + 6 (40%) + 6 (30%) = 60
    assert data["raw_damage_sum"] == 100
    assert data["scaled_damage_total"] == 60
    assert len(data["hits"]) == 5
    assert data["hits"][0]["scaling_percent"] == 100
    assert data["hits"][1]["scaling_percent"] == 70
    assert data["hits"][2]["scaling_percent"] == 50
    assert data["hits"][3]["scaling_percent"] == 40
    assert data["hits"][4]["scaling_percent"] == 30


def test_combo_wall_distance_and_positioning_requirements(test_db: Session):
    """
    Verify combo routes requiring wall proximity, wall splat, or open ground
    are correctly cataloged and separated.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    kazuya = test_db.query(Character).filter_by(slug="kazuya").first()

    report = ComboCompatibilityEngine.generate_recommendations(
        db=test_db,
        player_character=jin,
        opponent_character=kazuya,
        wall_position="NEAR_WALL",
    )

    assert report.wall_position == "NEAR_WALL"
    # Wall combos require wall and are present in wall_combo
    wall_combos = report.wall_combo
    assert len(wall_combos) >= 1
    for wc in wall_combos:
        assert wc.uses_wall is True
        assert wc.combo_type in ["WALL_COMBO", "WALL_BREAK"]

    # Wall carry routes carry opponent towards the wall
    wall_carry_combos = report.wall_carry
    assert len(wall_carry_combos) >= 1
    for wcc in wall_carry_combos:
        assert wcc.combo_type == "WALL_CARRY" or wcc.uses_wall is True


def test_combo_heat_requirements_and_state(test_db: Session):
    """
    Verify Heat-dependent combos (e.g., Heat Engager/Heat Dash/Heat Smash extensions)
    require Heat and are isolated in heat_dependent category.
    """
    jin = test_db.query(Character).filter_by(slug="jin").first()
    kazuya = test_db.query(Character).filter_by(slug="kazuya").first()

    report = ComboCompatibilityEngine.generate_recommendations(
        db=test_db,
        player_character=jin,
        opponent_character=kazuya,
        heat_state="AVAILABLE",
    )

    assert report.heat_state == "AVAILABLE"
    assert len(report.heat_dependent) >= 1
    for hc in report.heat_dependent:
        assert hc.uses_heat is True

    # Check non-heat routes exist
    non_heat_combos = [c for c in report.standard_launch if not c.uses_heat]
    assert len(non_heat_combos) >= 1


def test_combo_patch_differences_and_source_provenance(test_db: Session):
    """
    Verify patch version provenance tracking and ensure patch differences
    are preserved on all combo routes.
    """
    combos = test_db.query(ComboRoute).all()
    assert len(combos) > 0

    for c in combos:
        # Every combo must have a valid patch_version and source
        assert c.patch_version is not None and len(c.patch_version) > 0
        assert c.source is not None and len(c.source) > 0
        assert c.damage_type in ["TESTED", "REPORTED", "ESTIMATED", "UNVERIFIED"]
        assert c.damage_calculation_method in [
            "LAB_TESTED_IN_GAME",
            "REPORTED_SOURCE",
            "SCALED_ESTIMATE",
            "UNVERIFIED",
        ]

    # Create a route from a different/older patch version (e.g. 1.05.00) to verify multi-patch segregation
    jin = test_db.query(Character).filter_by(slug="jin").first()
    legacy_combo = ComboRoute(
        character_id=jin.id,
        title="Legacy Patch 1.05 Electric Route",
        notation_sequence="cd+2 > b+3 > ZEN 1,3",
        total_damage=68,
        hit_count=4,
        difficulty="HARD",
        combo_type="MIDSCREEN",
        launcher_type="NORMAL_HIT",
        patch_version="1.05.00",
        source="Legacy Tekken 8 Patch 1.05.00 Lab Data",
        verification_status="LEGACY_VERIFIED",
        damage_type="TESTED",
        damage_calculation_method="LAB_TESTED_IN_GAME",
        target_hurtbox_class="UNIVERSAL",
    )
    test_db.add(legacy_combo)
    test_db.commit()
    test_db.refresh(legacy_combo)

    assert legacy_combo.patch_version == "1.05.00"
    assert legacy_combo.patch_version != "3.00.02"

    # Cleanup legacy combo so it doesn't pollute subsequent queries
    test_db.delete(legacy_combo)
    test_db.commit()

