from fastapi.testclient import TestClient


def _register_and_login(client: TestClient, email: str, password: str = "secret123") -> str:
    client.post("/api/auth/register", json={"email": email, "password": password})
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_get_tags_returns_only_own_tags(client: TestClient) -> None:
    token_a = _register_and_login(client, "user-a@example.com")
    token_b = _register_and_login(client, "user-b@example.com")

    client.post("/api/tags", json={"name": "Python"}, headers=_auth_header(token_a))
    client.post("/api/tags", json={"name": "FastAPI"}, headers=_auth_header(token_b))

    response = client.get("/api/tags", headers=_auth_header(token_a))

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["name"] == "Python"


def test_create_tag_success(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")

    response = client.post("/api/tags", json={"name": "Python"}, headers=_auth_header(token))

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Python"
    assert "id" in body


def test_create_tag_duplicate_name(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    client.post("/api/tags", json={"name": "Python"}, headers=_auth_header(token))

    response = client.post("/api/tags", json={"name": "Python"}, headers=_auth_header(token))

    assert response.status_code == 409


def test_rename_tag_success(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    created = client.post("/api/tags", json={"name": "Python"}, headers=_auth_header(token))
    tag_id = created.json()["id"]

    response = client.put(
        f"/api/tags/{tag_id}", json={"name": "FastAPI"}, headers=_auth_header(token)
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == tag_id
    assert body["name"] == "FastAPI"


def test_rename_tag_duplicate_name(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    client.post("/api/tags", json={"name": "Python"}, headers=_auth_header(token))
    created = client.post("/api/tags", json={"name": "FastAPI"}, headers=_auth_header(token))
    tag_id = created.json()["id"]

    response = client.put(
        f"/api/tags/{tag_id}", json={"name": "Python"}, headers=_auth_header(token)
    )

    assert response.status_code == 409


def test_rename_tag_not_owned_returns_404(client: TestClient) -> None:
    token_a = _register_and_login(client, "user-a@example.com")
    token_b = _register_and_login(client, "user-b@example.com")
    created = client.post("/api/tags", json={"name": "Python"}, headers=_auth_header(token_a))
    tag_id = created.json()["id"]

    response = client.put(
        f"/api/tags/{tag_id}", json={"name": "FastAPI"}, headers=_auth_header(token_b)
    )

    assert response.status_code == 404


def test_delete_tag_success(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    created = client.post("/api/tags", json={"name": "Python"}, headers=_auth_header(token))
    tag_id = created.json()["id"]

    response = client.delete(f"/api/tags/{tag_id}", headers=_auth_header(token))

    assert response.status_code == 204

    list_response = client.get("/api/tags", headers=_auth_header(token))
    assert list_response.json() == []


def test_delete_tag_not_owned_returns_404(client: TestClient) -> None:
    token_a = _register_and_login(client, "user-a@example.com")
    token_b = _register_and_login(client, "user-b@example.com")
    created = client.post("/api/tags", json={"name": "Python"}, headers=_auth_header(token_a))
    tag_id = created.json()["id"]

    response = client.delete(f"/api/tags/{tag_id}", headers=_auth_header(token_b))

    assert response.status_code == 404


def test_get_tags_unauthenticated(client: TestClient) -> None:
    response = client.get("/api/tags")

    assert response.status_code == 401


def test_create_tag_unauthenticated(client: TestClient) -> None:
    response = client.post("/api/tags", json={"name": "Python"})

    assert response.status_code == 401


def test_update_tag_unauthenticated(client: TestClient) -> None:
    response = client.put("/api/tags/1", json={"name": "Python"})

    assert response.status_code == 401


def test_delete_tag_unauthenticated(client: TestClient) -> None:
    response = client.delete("/api/tags/1")

    assert response.status_code == 401
