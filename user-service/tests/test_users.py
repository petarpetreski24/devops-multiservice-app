def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "user-service"


def test_create_user(client):
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data


def test_create_user_duplicate_username(client):
    client.post("/users/", json={
        "username": "testuser",
        "email": "test1@example.com",
        "password": "pass123"
    })
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test2@example.com",
        "password": "pass123"
    })
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_user_duplicate_email(client):
    client.post("/users/", json={
        "username": "user1",
        "email": "test@example.com",
        "password": "pass123"
    })
    response = client.post("/users/", json={
        "username": "user2",
        "email": "test@example.com",
        "password": "pass123"
    })
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_list_users(client):
    client.post("/users/", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "pass123"
    })
    client.post("/users/", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "pass123"
    })
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_user(client):
    create_resp = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "pass123"
    })
    user_id = create_resp.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404


def test_update_user(client):
    create_resp = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "pass123"
    })
    user_id = create_resp.json()["id"]

    response = client.put(f"/users/{user_id}", json={
        "username": "updateduser"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"


def test_delete_user(client):
    create_resp = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "pass123"
    })
    user_id = create_resp.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_login_success(client):
    client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    })

    response = client.post("/users/login", json={
        "username": "testuser",
        "password": "securepass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    })

    response = client.post("/users/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
