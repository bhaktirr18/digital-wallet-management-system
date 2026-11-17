from app.models import User, Wallet
from app.extensions import db


def test_user_registration(client, app):
    response = client.post(
        "/register",
        data={
            "full_name": "New User",
            "email": "newuser@example.com",
            "password": "password123",
            "confirm_password": "password123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(
            email="newuser@example.com"
        ).first()

        assert user is not None
        assert user.full_name == "New User"
        assert user.check_password("password123")
        assert user.wallet is not None


def test_duplicate_registration(client, test_user):
    response = client.post(
        "/register",
        data={
            "full_name": "Another User",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }
    )

    assert response.status_code == 200
    assert b"already exists" in response.data


def test_user_login(client, test_user):
    response = client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "password123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Welcome back!" in response.data


def test_login_with_wrong_password(client, test_user):
    response = client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )

    assert b"Invalid email or password." in response.data


def test_user_logout(client, test_user):
    client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/logout",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"You have been logged out." in response.data