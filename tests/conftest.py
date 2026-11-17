import pytest

from app import create_app
from app.extensions import db
from app.models import User, Wallet


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_user(app):
    user = User(
        full_name="Test User",
        email="test@example.com"
    )
    user.set_password("password123")

    db.session.add(user)
    db.session.flush()

    wallet = Wallet(user=user)
    db.session.add(wallet)
    db.session.commit()

    return user