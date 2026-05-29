def test_signup_creates_user_and_logs_in(client):
    response = client.post(
        "/signup",
        json={
            "username": "new_test_user",
            "password": "password123",
            "password_confirmation": "password123",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["username"] == "new_test_user"
    assert "password_hash" not in data


def test_signup_rejects_duplicate_username(client):
    response = client.post(
        "/signup",
        json={
            "username": "test_user",
            "password": "password123",
            "password_confirmation": "password123",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data


def test_login_with_valid_credentials(client):
    response = client.post(
        "/login",
        json={
            "username": "test_user",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["username"] == "test_user"
    assert "password_hash" not in data


def test_login_rejects_invalid_credentials(client):
    response = client.post(
        "/login",
        json={
            "username": "test_user",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401

    data = response.get_json()

    assert "errors" in data


def test_check_session_returns_user_when_logged_in(client):
    client.post(
        "/login",
        json={
            "username": "test_user",
            "password": "password123",
        },
    )

    response = client.get("/check_session")

    assert response.status_code == 200

    data = response.get_json()

    assert data["username"] == "test_user"


def test_check_session_rejects_logged_out_user(client):
    response = client.get("/check_session")

    assert response.status_code == 401

    data = response.get_json()

    assert "errors" in data


def test_logout_clears_session(client):
    client.post(
        "/login",
        json={
            "username": "test_user",
            "password": "password123",
        },
    )

    logout_response = client.delete("/logout")

    assert logout_response.status_code == 204

    check_response = client.get("/check_session")

    assert check_response.status_code == 401