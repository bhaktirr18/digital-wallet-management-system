import pytest

from app.models import User, Wallet
from app.extensions import db
from app.services.wallet_service import (
    get_wallet_balance,
    deposit_money
)


def test_get_wallet_balance(app, test_user):
    with app.app_context():
        balance = get_wallet_balance(test_user.wallet.id)

        assert balance == 0


def test_deposit_money(app, test_user):
    with app.app_context():
        wallet_id = test_user.wallet.id

        balance = deposit_money(wallet_id, "500")

        assert balance == 50000


def test_deposit_money_with_decimal_amount(app, test_user):
    with app.app_context():
        wallet_id = test_user.wallet.id

        balance = deposit_money(wallet_id, "100.50")

        assert balance == 10050


def test_deposit_money_rejects_invalid_amount(app, test_user):
    with app.app_context():
        wallet_id = test_user.wallet.id

        with pytest.raises(ValueError):
            deposit_money(wallet_id, "-100")


def test_deposit_money_rejects_missing_wallet(app):
    with app.app_context():
        with pytest.raises(ValueError, match="Wallet not found"):
            deposit_money(9999, "100")