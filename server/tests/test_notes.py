def login_test_user(client):
    return client.post(
        "/login",
        json={
            "username": "test_user",
            "password": "password123",
        },
    )


def test_get_notes_requires_login(client):
    response = client.get("/notes")

    assert response.status_code == 401

    data = response.get_json()

    assert "errors" in data


def test_get_notes_returns_only_current_users_notes(client):
    login_test_user(client)

    response = client.get("/notes?page=1&per_page=10")

    assert response.status_code == 200

    data = response.get_json()

    assert data["total"] == 1
    assert data["notes"][0]["title"] == "Test User Note"
    assert data["notes"][0]["content"] == "This note belongs to test_user."


def test_create_note_for_current_user(client):
    login_test_user(client)

    response = client.post(
        "/notes",
        json={
            "title": "Created Note",
            "content": "Created during test.",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["title"] == "Created Note"
    assert data["content"] == "Created during test."


def test_update_current_users_note(client):
    login_test_user(client)

    notes_response = client.get("/notes?page=1&per_page=10")
    note_id = notes_response.get_json()["notes"][0]["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "Updated Note",
            "content": "Updated during test.",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["title"] == "Updated Note"
    assert data["content"] == "Updated during test."


def test_cannot_update_another_users_note(client):
    login_test_user(client)

    response = client.patch(
        "/notes/2",
        json={
            "title": "Bad Update",
            "content": "This should not work.",
        },
    )

    assert response.status_code == 404

    data = response.get_json()

    assert "errors" in data


def test_delete_current_users_note(client):
    login_test_user(client)

    notes_response = client.get("/notes?page=1&per_page=10")
    note_id = notes_response.get_json()["notes"][0]["id"]

    delete_response = client.delete(f"/notes/{note_id}")

    assert delete_response.status_code == 204

    get_response = client.get("/notes?page=1&per_page=10")
    data = get_response.get_json()

    assert data["total"] == 0


def test_cannot_delete_another_users_note(client):
    login_test_user(client)

    response = client.delete("/notes/2")

    assert response.status_code == 404

    data = response.get_json()

    assert "errors" in data