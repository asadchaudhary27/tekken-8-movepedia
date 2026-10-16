"""
Unit and integration tests for Pro Gameplay Guides & Master Compendium API.
Verifies all 12 endpoints and relational cross-character data.
"""

from fastapi.testclient import TestClient


def test_guides_index(client: TestClient):
    response = client.get("/api/v1/guides/index")
    assert response.status_code == 200
    data = response.json()
    assert "total_sidesteps" in data
    assert data["total_sidesteps"] >= 40
    assert data["total_throw_breaks"] >= 20
    assert data["total_anti_cheese_guides"] >= 15
    assert data["hardware_and_zero_lag"] is True


def test_guides_sidesteps(client: TestClient):
    # All sidesteps
    response = client.get("/api/v1/guides/sidesteps")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 40

    # Filtered by character
    res_jin = client.get("/api/v1/guides/sidesteps?q=Jin")
    assert res_jin.status_code == 200
    jin_data = res_jin.json()
    assert len(jin_data) > 0
    assert "Jin" in jin_data[0]["character"]
    assert "SSL" in jin_data[0]["weak_side"]


def test_guides_throw_breaks(client: TestClient):
    # All throw breaks
    response = client.get("/api/v1/guides/throw-breaks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 20

    # Filtered by King
    res_king = client.get("/api/v1/guides/throw-breaks?q=King")
    assert res_king.status_code == 200
    king_data = res_king.json()
    assert len(king_data) > 0
    assert any("Giant Swing" in t["throw_name"] or "Tombstone" in t["throw_name"] for t in king_data)


def test_guides_anti_cheese(client: TestClient):
    # All anti cheese
    response = client.get("/api/v1/guides/anti-cheese")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 15

    # Filtered by Hwoarang
    res_hwo = client.get("/api/v1/guides/anti-cheese?q=Hwoarang")
    assert res_hwo.status_code == 200
    hwo_data = res_hwo.json()
    assert len(hwo_data) > 0
    assert "d+3,4" in hwo_data[0]["cheese_move"]


def test_guides_installs(client: TestClient):
    response = client.get("/api/v1/guides/installs")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    claudio = [i for i in data if "Claudio" in i["character"]]
    assert len(claudio) > 0
    assert "Starburst" in claudio[0]["install_name"]


def test_guides_wall_combos(client: TestClient):
    response = client.get("/api/v1/guides/wall-combos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 25


def test_guides_ten_hit_combos(client: TestClient):
    response = client.get("/api/v1/guides/ten-hit-combos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10


def test_guides_heat_smashes(client: TestClient):
    response = client.get("/api/v1/guides/heat-smashes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_guides_movement_bible(client: TestClient):
    response = client.get("/api/v1/guides/movement-bible")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    assert any("Korean Backdash" in m["technique"] for m in data)


def test_guides_hardware_settings(client: TestClient):
    response = client.get("/api/v1/guides/hardware-settings")
    assert response.status_code == 200
    data = response.json()
    assert "pc_zero_lag_config" in data or "controllers" in data


def test_guides_emergency_protocol(client: TestClient):
    response = client.get("/api/v1/guides/emergency-protocol")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_guides_character_tactics_slug(client: TestClient):
    response = client.get("/api/v1/guides/character/jin")
    assert response.status_code == 200
    data = response.json()
    assert data["character_slug"] == "jin"
    assert data["sidestep"] is not None
    assert "SSL" in data["sidestep"]["weak_side"]
    assert data["anti_cheese"] is not None
    assert "heat_smash" in data
    assert data["heat_smash"] is not None
    assert "i16" in data["heat_smash"]["startup_frames"]
    assert "blender_scenarios" in data
    assert isinstance(data["blender_scenarios"], list)


def test_character_heat_smashes_roster(client: TestClient):
    # Test all 43 character heat smashes
    response = client.get("/api/v1/guides/character-heat-smashes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 43
    # Check Jack-8 fastest heat smash (i10)
    jack = [h for h in data if h["character_slug"] == "jack-8"]
    assert len(jack) == 1
    assert jack[0]["startup_frames"] == "i10"

    # Test filtering by category
    res_fast = client.get("/api/v1/guides/character-heat-smashes?category=Fastest")
    assert res_fast.status_code == 200
    fast_data = res_fast.json()
    assert len(fast_data) >= 7

    # Test view=characters on main heat-smashes endpoint
    res_view = client.get("/api/v1/guides/heat-smashes?view=characters")
    assert res_view.status_code == 200
    assert len(res_view.json()) == 43


def test_movement_bible_techniques(client: TestClient):
    response = client.get("/api/v1/guides/movement-bible")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 7
    kbd = [m for m in data if m["technique_slug"] == "korean-backdash"]
    assert len(kbd) == 1
    assert "socd_shortcut" in kbd[0]
    assert "Hold Back" in kbd[0]["socd_shortcut"]
    assert "warning" in kbd[0]
    assert "sway" in kbd[0]["warning"].lower()

    # Test search filter
    res_wave = client.get("/api/v1/guides/movement-bible?q=wavedash")
    assert res_wave.status_code == 200
    assert len(res_wave.json()) >= 1


def test_emergency_blender_protocol(client: TestClient):
    response = client.get("/api/v1/guides/emergency-protocol")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 20

    # Test specific scenario fields
    kaz = [b for b in data if b["character_slug"] == "kazuya"]
    assert len(kaz) >= 1
    assert "panic_trigger" in kaz[0]
    assert "verified_safe_response" in kaz[0]
    assert "risk_reward" in kaz[0]
    assert "drill" in kaz[0]

    # Test filter by character
    res_kaz = client.get("/api/v1/guides/emergency-protocol?character=kazuya")
    assert res_kaz.status_code == 200
    assert len(res_kaz.json()) >= 1
