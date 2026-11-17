import pytest

from app.extensions import db
from app.models import User, Wallet
from app.services.transaction_service import (
    deposit_funds,
    transfer_funds
)
from app.utils.errors import DuplicateTransactionError


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


def test_duplicate_deposit_is_rejected(app, test_user):
    with app.app_context():
        wallet_id = test_user.wallet.id

        deposit_funds(wallet_id, "500", "deposit-key-001")

        with pytest.raises(DuplicateTransactionError):
            deposit_funds(wallet_id, "500", "deposit-key-001")

        wallet = db.session.get(Wallet, wallet_id)
        assert wallet.balance_paise == 50000


def test_duplicate_transfer_is_rejected(
    app, test_user, second_user
):
    with app.app_context():
        sender_id = test_user.wallet.id
        recipient_id = second_user.wallet.id

        deposit_funds(sender_id, "500", "deposit-key-002")

        transfer_funds(
            sender_id,
            "second@example.com",
            "100",
            "transfer-key-001"
        )

        with pytest.raises(DuplicateTransactionError):
            transfer_funds(
                sender_id,
                "second@example.com",
                "100",
                "transfer-key-001"
            )

        sender = db.session.get(Wallet, sender_id)
        recipient = db.session.get(Wallet, recipient_id)

        assert sender.balance_paise == 40000
        assert recipient.balance_paise == 10000