from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login_flow() -> None:
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "demo@example.com", "password": "strongpass123"},
    )
    assert reg.status_code == 200
    tokens = reg.json()
    assert "access_token" in tokens

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "demo@example.com", "password": "strongpass123"},
    )
    assert login.status_code == 200
