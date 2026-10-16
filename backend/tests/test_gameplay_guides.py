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
