import pytest

from app.extensions import db
from app.models import User, Wallet
from app.services.wallet_service import deposit_money
from app.services.transaction_service import transfer_funds
from app.utils.errors import InsufficientBalanceError, RecipientNotFoundError


@pytest.fixture
def second_user(app):
    user = User(
        full_name="Second User",
        email="second@example.com"
    )
    user.set_password("password123")

    db.session.add(user)
    db.session.flush()

    wallet = Wallet(user=user)
    db.session.add(wallet)
    db.session.commit()

    return user


def test_successful_transfer(app, test_user, second_user):
    with app.app_context():
        sender_id = test_user.wallet.id
        recipient_id = second_user.wallet.id

        deposit_money(sender_id, "500")

        transfer_funds(
            sender_id,
            "second@example.com",
            "200",
            "transfer-test-001"
        )

        sender = db.session.get(Wallet, sender_id)
        recipient = db.session.get(Wallet, recipient_id)

        assert sender.balance_paise == 30000
        assert recipient.balance_paise == 20000


def test_transfer_rejects_insufficient_balance(
    app, test_user, second_user
):
    with app.app_context():
        with pytest.raises(InsufficientBalanceError):
            transfer_funds(
                test_user.wallet.id,
                "second@example.com",
                "100",
                "transfer-test-002"
            )


def test_transfer_rejects_unknown_recipient(app, test_user):
    with app.app_context():
        with pytest.raises(RecipientNotFoundError):
            transfer_funds(
                test_user.wallet.id,
                "unknown@example.com",
                "100",
                "transfer-test-003"
            )


def test_transfer_rejects_self_transfer(app, test_user):
    with app.app_context():
        with pytest.raises(ValueError, match="yourself"):
            transfer_funds(
                test_user.wallet.id,
                "test@example.com",
                "100",
                "transfer-test-004"
            )


def test_transfer_rejects_negative_amount(
    app, test_user, second_user
):
    with app.app_context():
        with pytest.raises(ValueError):
            transfer_funds(
                test_user.wallet.id,
                "second@example.com",
                "-100",
                "transfer-test-005"
            )