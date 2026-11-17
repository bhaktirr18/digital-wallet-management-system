def test_dashboard_requires_login(client):
    response = client.get("/")

    assert response.status_code == 302
    assert "/login" in response.location


def test_deposit_page_requires_login(client):
    response = client.get("/wallet/deposit")

    assert response.status_code == 302
    assert "/login" in response.location


def test_transfer_page_requires_login(client):
    response = client.get("/wallet/transfer")

    assert response.status_code == 302
    assert "/login" in response.location


def test_history_page_requires_login(client):
    response = client.get("/wallet/history")

    assert response.status_code == 302
    assert "/login" in response.location


def test_dashboard_loads_after_login(client, test_user):
    client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.get("/")

    assert response.status_code == 200
    assert b"Welcome, Test User!" in response.data


def test_deposit_page_loads_after_login(client, test_user):
    client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.get("/wallet/deposit")

    assert response.status_code == 200
    assert b"Add Money" in response.data


def test_transfer_page_loads_after_login(client, test_user):
    client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.get("/wallet/transfer")

    assert response.status_code == 200
    assert b"Transfer Money" in response.data


def test_history_page_loads_after_login(client, test_user):
    client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.get("/wallet/history")

    assert response.status_code == 200
    assert b"Transaction History" in response.data