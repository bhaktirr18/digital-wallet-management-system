from sqlalchemy import select

from app.extensions import db
from app.models import Wallet
from app.utils.money import rupees_to_paise
from app.utils.errors import (
    InsufficientBalanceError,
    RecipientNotFoundError
)


def get_wallet_balance(wallet_id):
    wallet = db.session.get(Wallet, wallet_id)

    if not wallet:
        raise ValueError("Wallet not found.")

    return wallet.balance_paise


def deposit_money(wallet_id, amount):
    amount_paise = rupees_to_paise(amount)

    wallet = db.session.execute(
        select(Wallet)
        .where(Wallet.id == wallet_id)
    ).scalar_one_or_none()

    if not wallet:
        raise ValueError("Wallet not found.")

    try:
        wallet.balance_paise += amount_paise
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return wallet.balance_paise


def transfer_money(sender_wallet_id, recipient_email, amount):
    amount_paise = rupees_to_paise(amount)
    recipient_email = recipient_email.strip().lower()

    sender = db.session.get(Wallet, sender_wallet_id)

    if not sender:
        raise ValueError("Sender wallet not found.")

    recipient = db.session.scalar(
        select(Wallet)
        .join(Wallet.user)
        .where(Wallet.user.has(email=recipient_email))
    )

    if not recipient:
        raise RecipientNotFoundError("Recipient account not found.")

    if sender.id == recipient.id:
        raise ValueError("You cannot transfer money to yourself.")

    try:
        if sender.balance_paise < amount_paise:
            raise InsufficientBalanceError("Insufficient wallet balance.")

        sender.balance_paise -= amount_paise
        recipient.balance_paise += amount_paise

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return sender.balance_paise