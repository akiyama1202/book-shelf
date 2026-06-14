from fastapi.testclient import TestClient


def test_register_success(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "secret123"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "user@example.com"
    assert "id" in body
    assert "created_at" in body
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_email(client: TestClient) -> None:
    payload = {"email": "user@example.com", "password": "secret123"}

    first = client.post("/api/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/auth/register", json=payload)
    assert second.status_code == 409


def test_register_invalid_email(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register",
        json={"email": "not-an-email", "password": "secret123"},
    )

    assert response.status_code == 422


def test_login_success(client: TestClient) -> None:
    client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "secret123"},
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]


def test_login_wrong_password(client: TestClient) -> None:
    client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "secret123"},
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_login_unknown_user(client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        json={"email": "unknown@example.com", "password": "secret123"},
    )

    assert response.status_code == 401
