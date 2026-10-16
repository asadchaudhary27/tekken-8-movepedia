import pytest
from fastapi.testclient import TestClient
from backend.app.core.security import generate_totp_secret, pyotp


def test_admin_login_and_profile_flow(client: TestClient):
    """Verify login with username and email, JWT token retrieval and /me endpoint."""
    # 1. Login with username
    res = client.post("/api/v1/admin/login", json={
        "username_or_email": "alpha",
        "password": "Alpha_1122#"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["access_token"] is not None
    assert data["requires_2fa"] is False
    assert data["user"]["username"] == "alpha"
    assert data["user"]["email"] == "asadqaisar17@gmail.com"

    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Login with email
    res_email = client.post("/api/v1/admin/login", json={
        "username_or_email": "asadqaisar17@gmail.com",
        "password": "Alpha_1122#"
    })
    assert res_email.status_code == 200
    assert res_email.json()["access_token"] is not None

    # 3. Access protected /me endpoint
    res_me = client.get("/api/v1/admin/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["username"] == "alpha"
    assert res_me.json()["role"] == "SuperAdmin"


def test_admin_login_failures(client: TestClient):
    """Verify invalid password and nonexistent accounts receive 401."""
    res_bad_pass = client.post("/api/v1/admin/login", json={
        "username_or_email": "alpha",
        "password": "IncorrectPassword999"
    })
    assert res_bad_pass.status_code == 401
    assert "invalid" in res_bad_pass.json()["detail"].lower()

    res_bad_user = client.post("/api/v1/admin/login", json={
        "username_or_email": "ghost_admin_999",
        "password": "AnyPassword"
    })
    assert res_bad_user.status_code == 401


def test_admin_user_management_crud(client: TestClient):
    """Verify SuperAdmin can create, list, and delete secondary admin accounts."""
    login_res = client.post("/api/v1/admin/login", json={
        "username_or_email": "alpha",
        "password": "Alpha_1122#"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create secondary editor
    create_res = client.post("/api/v1/admin/users", headers=headers, json={
        "username": "lab_editor_test",
        "email": "editor_test@tekken.gg",
        "password": "EditorSecurePass123#",
        "role": "Editor"
    })
    assert create_res.status_code == 200
    new_user_id = create_res.json()["id"]
    assert create_res.json()["username"] == "lab_editor_test"

    # 2. List users
    list_res = client.get("/api/v1/admin/users", headers=headers)
    assert list_res.status_code == 200
    usernames = [u["username"] for u in list_res.json()]
    assert "lab_editor_test" in usernames

    # 3. Test login with new secondary editor
    editor_login = client.post("/api/v1/admin/login", json={
        "username_or_email": "lab_editor_test",
        "password": "EditorSecurePass123#"
    })
    assert editor_login.status_code == 200
    assert editor_login.json()["user"]["role"] == "Editor"

    # 4. Clean up / delete secondary user
    del_res = client.delete(f"/api/v1/admin/users/{new_user_id}", headers=headers)
    assert del_res.status_code == 200


def test_admin_2fa_setup_flow(client: TestClient):
    """Verify TOTP secret generation, QR code rendering, and verification."""
    login_res = client.post("/api/v1/admin/login", json={
        "username_or_email": "alpha",
        "password": "Alpha_1122#"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Setup 2FA
    setup_res = client.post("/api/v1/admin/2fa/setup", headers=headers)
    assert setup_res.status_code == 200
    data = setup_res.json()
    assert "secret" in data
    assert data["qr_code_base64"].startswith("data:image/png;base64,")

    # Generate valid test code
    secret = data["secret"]
    valid_code = pyotp.TOTP(secret).now()

    # Enable 2FA
    enable_res = client.post("/api/v1/admin/2fa/enable", headers=headers, json={"code": valid_code})
    assert enable_res.status_code == 200
    assert "ENABLED" in enable_res.json()["message"]

    # Verify login now prompts for 2FA
    login_prompt = client.post("/api/v1/admin/login", json={
        "username_or_email": "alpha",
        "password": "Alpha_1122#"
    })
    assert login_prompt.status_code == 200
    assert login_prompt.json()["requires_2fa"] is True

    # Complete login with 2FA code
    code_now = pyotp.TOTP(secret).now()
    login_with_code = client.post("/api/v1/admin/login", json={
        "username_or_email": "alpha",
        "password": "Alpha_1122#",
        "totp_code": code_now
    })
    assert login_with_code.status_code == 200
    assert login_with_code.json()["access_token"] is not None

    # Disable 2FA to return account to default low-friction state
    disable_res = client.post("/api/v1/admin/2fa/disable", headers=headers, json={"password": "Alpha_1122#"})
    assert disable_res.status_code == 200
    assert "DISABLED" in disable_res.json()["message"]


def test_database_backup_endpoint(client: TestClient):
    """Verify SuperAdmin can download database backup."""
    login_res = client.post("/api/v1/admin/login", json={
        "username_or_email": "alpha",
        "password": "Alpha_1122#"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/admin/database/backup", headers=headers)
    assert res.status_code == 200
    assert len(res.content) > 1000
