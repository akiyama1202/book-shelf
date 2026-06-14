from fastapi.testclient import TestClient


def _register_and_login(client: TestClient, email: str, password: str = "secret123") -> str:
    client.post("/api/auth/register", json={"email": email, "password": password})
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _book_payload(**overrides: object) -> dict:
    payload = {
        "title": "吾輩は猫である",
        "author": "夏目漱石",
        "status": "unread",
        "rating": None,
        "memo": None,
        "tags": [],
    }
    payload.update(overrides)
    return payload


def test_create_book_success(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")

    response = client.post("/api/books", json=_book_payload(), headers=_auth_header(token))

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "吾輩は猫である"
    assert body["author"] == "夏目漱石"
    assert body["status"] == "unread"
    assert body["rating"] is None
    assert body["memo"] is None
    assert body["tags"] == []
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_create_book_with_tags(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")

    response = client.post(
        "/api/books",
        json=_book_payload(tags=["小説", "名作"]),
        headers=_auth_header(token),
    )

    assert response.status_code == 201
    body = response.json()
    tag_names = {tag["name"] for tag in body["tags"]}
    assert tag_names == {"小説", "名作"}


def test_create_book_validation_error(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")

    response = client.post(
        "/api/books",
        json=_book_payload(title=""),
        headers=_auth_header(token),
    )

    assert response.status_code == 422


def test_create_book_invalid_status(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")

    response = client.post(
        "/api/books",
        json=_book_payload(status="invalid_status"),
        headers=_auth_header(token),
    )

    assert response.status_code == 422


def test_create_book_invalid_rating(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")

    response = client.post(
        "/api/books",
        json=_book_payload(rating=6),
        headers=_auth_header(token),
    )

    assert response.status_code == 422


def test_get_books_returns_only_own_books(client: TestClient) -> None:
    token_a = _register_and_login(client, "user-a@example.com")
    token_b = _register_and_login(client, "user-b@example.com")

    client.post("/api/books", json=_book_payload(title="本A"), headers=_auth_header(token_a))
    client.post("/api/books", json=_book_payload(title="本B"), headers=_auth_header(token_b))

    response = client.get("/api/books", headers=_auth_header(token_a))

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["title"] == "本A"


def test_get_books_search_by_title(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    client.post(
        "/api/books",
        json=_book_payload(title="吾輩は猫である", author="夏目漱石"),
        headers=_auth_header(token),
    )
    client.post(
        "/api/books",
        json=_book_payload(title="坊っちゃん", author="夏目漱石"),
        headers=_auth_header(token),
    )

    response = client.get("/api/books", params={"search": "猫"}, headers=_auth_header(token))

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["title"] == "吾輩は猫である"


def test_get_books_search_by_author(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    client.post(
        "/api/books",
        json=_book_payload(title="ノルウェイの森", author="村上春樹"),
        headers=_auth_header(token),
    )
    client.post(
        "/api/books",
        json=_book_payload(title="坊っちゃん", author="夏目漱石"),
        headers=_auth_header(token),
    )

    response = client.get("/api/books", params={"search": "村上"}, headers=_auth_header(token))

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["author"] == "村上春樹"


def test_get_books_sort_by_title_asc(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    client.post("/api/books", json=_book_payload(title="B本"), headers=_auth_header(token))
    client.post("/api/books", json=_book_payload(title="A本"), headers=_auth_header(token))

    response = client.get(
        "/api/books",
        params={"sort_by": "title", "sort_order": "asc"},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    titles = [item["title"] for item in response.json()["items"]]
    assert titles == ["A本", "B本"]


def test_get_books_sort_by_title_desc(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    client.post("/api/books", json=_book_payload(title="B本"), headers=_auth_header(token))
    client.post("/api/books", json=_book_payload(title="A本"), headers=_auth_header(token))

    response = client.get(
        "/api/books",
        params={"sort_by": "title", "sort_order": "desc"},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    titles = [item["title"] for item in response.json()["items"]]
    assert titles == ["B本", "A本"]


def test_get_books_sort_by_author(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    client.post(
        "/api/books", json=_book_payload(title="本1", author="佐藤"), headers=_auth_header(token)
    )
    client.post(
        "/api/books", json=_book_payload(title="本2", author="鈴木"), headers=_auth_header(token)
    )

    response = client.get(
        "/api/books",
        params={"sort_by": "author", "sort_order": "asc"},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    authors = [item["author"] for item in response.json()["items"]]
    assert authors == ["佐藤", "鈴木"]


def test_get_books_sort_by_rating(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    client.post(
        "/api/books", json=_book_payload(title="本1", rating=3), headers=_auth_header(token)
    )
    client.post(
        "/api/books", json=_book_payload(title="本2", rating=5), headers=_auth_header(token)
    )
    client.post(
        "/api/books", json=_book_payload(title="本3", rating=1), headers=_auth_header(token)
    )

    response = client.get(
        "/api/books",
        params={"sort_by": "rating", "sort_order": "asc"},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    ratings = [item["rating"] for item in response.json()["items"]]
    assert ratings == [1, 3, 5]


def test_get_books_sort_by_created_at(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    client.post("/api/books", json=_book_payload(title="先に作成"), headers=_auth_header(token))
    client.post("/api/books", json=_book_payload(title="後に作成"), headers=_auth_header(token))

    response = client.get(
        "/api/books",
        params={"sort_by": "created_at", "sort_order": "asc"},
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    titles = [item["title"] for item in response.json()["items"]]
    assert titles == ["先に作成", "後に作成"]


def test_get_books_pagination(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    for i in range(5):
        client.post("/api/books", json=_book_payload(title=f"本{i}"), headers=_auth_header(token))

    response = client.get(
        "/api/books", params={"page": 1, "page_size": 2}, headers=_auth_header(token)
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 5
    assert body["page"] == 1
    assert body["page_size"] == 2
    assert len(body["items"]) == 2

    response_page2 = client.get(
        "/api/books", params={"page": 2, "page_size": 2}, headers=_auth_header(token)
    )
    body_page2 = response_page2.json()
    assert len(body_page2["items"]) == 2

    response_page3 = client.get(
        "/api/books", params={"page": 3, "page_size": 2}, headers=_auth_header(token)
    )
    body_page3 = response_page3.json()
    assert len(body_page3["items"]) == 1


def test_get_book_success(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    created = client.post("/api/books", json=_book_payload(), headers=_auth_header(token)).json()

    response = client.get(f"/api/books/{created['id']}", headers=_auth_header(token))

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created["id"]
    assert body["title"] == "吾輩は猫である"


def test_get_book_not_owned_returns_404(client: TestClient) -> None:
    token_a = _register_and_login(client, "user-a@example.com")
    token_b = _register_and_login(client, "user-b@example.com")
    created = client.post("/api/books", json=_book_payload(), headers=_auth_header(token_a)).json()

    response = client.get(f"/api/books/{created['id']}", headers=_auth_header(token_b))

    assert response.status_code == 404


def test_update_book_success(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    created = client.post("/api/books", json=_book_payload(), headers=_auth_header(token)).json()

    response = client.put(
        f"/api/books/{created['id']}",
        json=_book_payload(title="坊っちゃん", status="reading", rating=4, memo="面白い"),
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "坊っちゃん"
    assert body["status"] == "reading"
    assert body["rating"] == 4
    assert body["memo"] == "面白い"


def test_update_book_with_tags(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    created = client.post(
        "/api/books", json=_book_payload(tags=["小説"]), headers=_auth_header(token)
    ).json()

    response = client.put(
        f"/api/books/{created['id']}",
        json=_book_payload(tags=["エッセイ", "随筆"]),
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    body = response.json()
    tag_names = {tag["name"] for tag in body["tags"]}
    assert tag_names == {"エッセイ", "随筆"}


def test_update_book_not_owned_returns_404(client: TestClient) -> None:
    token_a = _register_and_login(client, "user-a@example.com")
    token_b = _register_and_login(client, "user-b@example.com")
    created = client.post("/api/books", json=_book_payload(), headers=_auth_header(token_a)).json()

    response = client.put(
        f"/api/books/{created['id']}",
        json=_book_payload(title="他人の本"),
        headers=_auth_header(token_b),
    )

    assert response.status_code == 404


def test_delete_book_success(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    created = client.post("/api/books", json=_book_payload(), headers=_auth_header(token)).json()

    response = client.delete(f"/api/books/{created['id']}", headers=_auth_header(token))

    assert response.status_code == 204

    get_response = client.get(f"/api/books/{created['id']}", headers=_auth_header(token))
    assert get_response.status_code == 404


def test_delete_book_not_owned_returns_404(client: TestClient) -> None:
    token_a = _register_and_login(client, "user-a@example.com")
    token_b = _register_and_login(client, "user-b@example.com")
    created = client.post("/api/books", json=_book_payload(), headers=_auth_header(token_a)).json()

    response = client.delete(f"/api/books/{created['id']}", headers=_auth_header(token_b))

    assert response.status_code == 404


def test_get_books_unauthenticated(client: TestClient) -> None:
    response = client.get("/api/books")

    assert response.status_code == 401


def test_create_book_unauthenticated(client: TestClient) -> None:
    response = client.post("/api/books", json=_book_payload())

    assert response.status_code == 401


def test_get_book_unauthenticated(client: TestClient) -> None:
    response = client.get("/api/books/1")

    assert response.status_code == 401


def test_update_book_unauthenticated(client: TestClient) -> None:
    response = client.put("/api/books/1", json=_book_payload())

    assert response.status_code == 401


def test_delete_book_unauthenticated(client: TestClient) -> None:
    response = client.delete("/api/books/1")

    assert response.status_code == 401
