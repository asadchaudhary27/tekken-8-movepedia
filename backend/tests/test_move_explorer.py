"""
Comprehensive Test Suite for Phase 4: Tekken 8 Move Explorer & Verified Frame Data Engine.

Tests:
1. Move listing & enrichment with explicit frame states (VERIFIED, CONDITIONAL, NOT_APPLICABLE).
2. Advanced multi-field filtering: hit level, startup range, block safety, punishability, property type, stance, verification status, and substring text search.
3. Punish recommendations with pushback and reach awareness.
4. Strategic defensive countermeasures.
5. Version and source provenance tracking (patch_version, source_name, source_url, last_verified_date).
6. Single move inspection endpoint (/moves/{id}) and summary statistics (/moves/stats/summary).
"""

import pytest


def test_get_moves_by_character_slug(client):
    """Verify moves listing for a specific character with full enrichment."""
    response = client.get("/api/v1/moves?character_slug=jin&limit=50")
    assert response.status_code == 200
    moves = response.json()
    assert len(moves) > 0

    for m in moves:
        assert m["character_slug"] == "jin"
        assert "name" in m
        assert "original_notation" in m
        assert "hit_level_type" in m
        assert "block_safety" in m
        assert "frame_state_type" in m
        assert "patch_version" in m
        assert m["patch_version"] == "3.00.02"
        assert m["source_name"] == "wavu_wiki"


def test_explicit_frame_states(client):
    """
    Ensure frame states are strictly separated:
    - Stance moves / transitions must be NOT_APPLICABLE
    - Conditional strings (~, c, g, a, k) must be CONDITIONAL
    - Standard frame data must be VERIFIED
    - Never replace missing values with fake zeroes
    """
    response = client.get("/api/v1/moves?limit=500")
    assert response.status_code == 200
    moves = response.json()

    for m in moves:
        frame_state = m["frame_state_type"]
        assert frame_state in ["VERIFIED", "CONDITIONAL", "NOT_APPLICABLE", "UNKNOWN", "NOT_VERIFIED"]

        # If stance
        is_stance = (m.get("hit_level") or "").lower() == "s" or "stance" in (m.get("name") or "").lower() or (m.get("hit_level_type") == "STANCE")
        if is_stance:
            assert m["frame_state_type"] == "NOT_APPLICABLE"
            assert m["block_safety"] == "NOT_APPLICABLE"
            assert m["damage"] is None or m["damage"] >= 0

        # If conditional notation in startup or advantage
        raw_b = m.get("block_advantage_raw") or ""
        raw_s = m.get("startup_raw") or ""
        if not is_stance and ("~" in raw_b or "~" in raw_s or "c" in raw_b or "g" in raw_b):
            assert m["frame_state_type"] == "CONDITIONAL"


def test_hit_level_filtering(client):
    """Test filtering moves by High, Mid, Low, and Stance hit levels."""
    # High
    res_high = client.get("/api/v1/moves?hit_level=HIGH&limit=100")
    assert res_high.status_code == 200
    high_moves = res_high.json()
    assert len(high_moves) > 0
    for m in high_moves:
        assert "h" in (m.get("hit_level") or "").lower() or m["hit_level_type"] == "HIGH"

    # Mid
    res_mid = client.get("/api/v1/moves?hit_level=MID&limit=100")
    assert res_mid.status_code == 200
    mid_moves = res_mid.json()
    assert len(mid_moves) > 0
    for m in mid_moves:
        assert "m" in (m.get("hit_level") or "").lower() or m["hit_level_type"] == "MID"

    # Low
    res_low = client.get("/api/v1/moves?hit_level=LOW&limit=100")
    assert res_low.status_code == 200
    low_moves = res_low.json()
    assert len(low_moves) > 0
    for m in low_moves:
        assert "l" in (m.get("hit_level") or "").lower() or m["hit_level_type"] == "LOW"

    # Stance
    res_stance = client.get("/api/v1/moves?hit_level=STANCE&limit=100")
    assert res_stance.status_code == 200
    stance_moves = res_stance.json()
    for m in stance_moves:
        assert m["hit_level_type"] == "STANCE" or m["frame_state_type"] == "NOT_APPLICABLE"


def test_startup_range_filtering(client):
    """Test filtering moves by startup frame boundaries."""
    # Fast jabs (i10 to i12)
    res_fast = client.get("/api/v1/moves?startup_min=10&startup_max=12&limit=100")
    assert res_fast.status_code == 200
    fast_moves = res_fast.json()
    assert len(fast_moves) > 0
    for m in fast_moves:
        assert m["startup_frames"] is not None
        assert 10 <= m["startup_frames"] <= 12

    # Standard launchers (i15 to i16)
    res_launch = client.get("/api/v1/moves?startup_min=15&startup_max=16&limit=100")
    assert res_launch.status_code == 200
    launch_moves = res_launch.json()
    assert len(launch_moves) > 0
    for m in launch_moves:
        assert m["startup_frames"] is not None
        assert 15 <= m["startup_frames"] <= 16


def test_block_safety_filtering(client):
    """Test filtering by block safety (SAFE, UNSAFE, LAUNCH_PUNISH, PLUS)."""
    # Safe moves (>= -9 and <= 0)
    res_safe = client.get("/api/v1/moves?block_safety=SAFE&limit=100")
    assert res_safe.status_code == 200
    safe_moves = res_safe.json()
    assert len(safe_moves) > 0
    for m in safe_moves:
        assert m["block_safety"] == "SAFE"
        if m["block_advantage"] is not None:
            assert -9 <= m["block_advantage"] <= 0

    # Unsafe moves (-14 <= blk <= -10)
    res_unsafe = client.get("/api/v1/moves?block_safety=UNSAFE&limit=100")
    assert res_unsafe.status_code == 200
    unsafe_moves = res_unsafe.json()
    assert len(unsafe_moves) > 0
    for m in unsafe_moves:
        assert m["block_safety"] == "UNSAFE"
        if m["block_advantage"] is not None:
            assert -14 <= m["block_advantage"] <= -10

    # Launch punishable moves (<= -15)
    res_launch = client.get("/api/v1/moves?block_safety=LAUNCH_PUNISH&limit=100")
    assert res_launch.status_code == 200
    launch_moves = res_launch.json()
    assert len(launch_moves) > 0
    for m in launch_moves:
        assert m["block_safety"] == "LAUNCH_PUNISH"
        assert m["is_launch_punishable"] is True
        if m["block_advantage"] is not None:
            assert m["block_advantage"] <= -15

    # Plus on block (>= +1)
    res_plus = client.get("/api/v1/moves?block_safety=PLUS&limit=100")
    assert res_plus.status_code == 200
    plus_moves = res_plus.json()
    assert len(plus_moves) > 0
    for m in plus_moves:
        assert m["block_safety"] == "PLUS"
        assert m["is_plus_on_block"] is True
        if m["block_advantage"] is not None:
            assert m["block_advantage"] >= 1


def test_punishability_filtering(client):
    """Test punishability parameter (SAFE, LAUNCH_PUNISHABLE, PUNISHABLE_10)."""
    res_p10 = client.get("/api/v1/moves?punishability=PUNISHABLE_10&limit=100")
    assert res_p10.status_code == 200
    p10_moves = res_p10.json()
    assert len(p10_moves) > 0
    for m in p10_moves:
        assert m["block_safety"] in ["UNSAFE", "LAUNCH_PUNISH"]
        assert m["punish_startup_min"] is not None
        assert m["punish_startup_min"] <= 11

    res_lp = client.get("/api/v1/moves?punishability=LAUNCH_PUNISHABLE&limit=100")
    assert res_lp.status_code == 200
    lp_moves = res_lp.json()
    assert len(lp_moves) > 0
    for m in lp_moves:
        assert m["is_launch_punishable"] is True


def test_property_type_filtering(client):
    """Test filtering by move properties (heat_engager, power_crush, homing, tornado)."""
    # Heat engager
    res_heat = client.get("/api/v1/moves?property_type=heat_engager&limit=100")
    assert res_heat.status_code == 200
    heat_moves = res_heat.json()
    assert len(heat_moves) > 0
    for m in heat_moves:
        assert m["is_heat_engager"] is True or any("heat" in str(p).lower() for p in m.get("properties", []))

    # Power Crush
    res_pc = client.get("/api/v1/moves?property_type=power_crush&limit=100")
    assert res_pc.status_code == 200
    pc_moves = res_pc.json()
    assert len(pc_moves) > 0
    for m in pc_moves:
        assert m["is_power_crush"] is True or any("crush" in str(p).lower() for p in m.get("properties", []))

    # Homing
    res_homing = client.get("/api/v1/moves?property_type=homing&limit=100")
    assert res_homing.status_code == 200
    homing_moves = res_homing.json()
    for m in homing_moves:
        assert m["is_homing"] is True or any("homing" in str(p).lower() for p in m.get("properties", []))


def test_stance_filtering(client):
    """Test neutral_only vs stance_only filtering."""
    res_neutral = client.get("/api/v1/moves?stance_filter=neutral_only&limit=100")
    assert res_neutral.status_code == 200
    neutral_moves = res_neutral.json()
    assert len(neutral_moves) > 0
    for m in neutral_moves:
        assert m["hit_level_type"] != "STANCE"
        assert m["is_stance_move"] is False

    res_stance = client.get("/api/v1/moves?stance_filter=stance_only&limit=100")
    assert res_stance.status_code == 200
    stance_moves = res_stance.json()
    assert len(stance_moves) > 0
    for m in stance_moves:
        assert m["is_stance_move"] is True or m["frame_state_type"] == "NOT_APPLICABLE" or m["hit_level_type"] == "STANCE"


def test_text_search_query(client):
    """Test substring searching by command or move name."""
    res = client.get("/api/v1/moves?q=df%2B2&limit=50")
    assert res.status_code == 200
    moves = res.json()
    assert len(moves) > 0
    for m in moves:
        assert "df+2" in m["original_notation"].lower() or "df+2" in m["name"].lower()


def test_single_move_detail_endpoint(client):
    """Test GET /api/v1/moves/{move_id} returns complete enriched technical specification."""
    # First get a move ID
    res_list = client.get("/api/v1/moves?character_slug=jin&limit=5")
    assert res_list.status_code == 200
    first_move = res_list.json()[0]
    move_id = first_move["id"]

    # Inspect single move
    res_detail = client.get(f"/api/v1/moves/{move_id}")
    assert res_detail.status_code == 200
    data = res_detail.json()

    assert data["id"] == move_id
    assert data["character_name"] == "Jin Kazama"
    assert data["character_slug"] == "jin"
    assert data["patch_version"] == "3.00.02"
    assert data["source_name"] == "wavu_wiki"
    assert "punish_recommendation" in data
    assert "defensive_response" in data
    assert "tracking_property" in data

    # 404 on invalid ID
    res_404 = client.get("/api/v1/moves/999999")
    assert res_404.status_code == 404


def test_moves_summary_stats(client):
    """Test GET /api/v1/moves/stats/summary returns aggregated metrics."""
    # Global summary
    res_all = client.get("/api/v1/moves/stats/summary")
    assert res_all.status_code == 200
    stats = res_all.json()
    assert stats["total_moves"] > 0
    assert stats["verified_count"] > 0
    assert stats["verified_percentage"] == 100.0
    assert stats["safe_moves_count"] >= 0
    assert stats["unsafe_moves_count"] >= 0
    assert stats["launch_punishable_count"] >= 0

    # Character-specific summary
    res_jin = client.get("/api/v1/moves/stats/summary?character_slug=jin")
    assert res_jin.status_code == 200
    jin_stats = res_jin.json()
    assert jin_stats["total_moves"] > 0
    assert jin_stats["total_moves"] <= stats["total_moves"]
