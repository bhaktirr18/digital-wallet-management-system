from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import User, Wallet, Transaction
from app.utils.money import rupees_to_paise
from app.utils.errors import (
    InsufficientBalanceError,
    RecipientNotFoundError,
    DuplicateTransactionError
)


def deposit_funds(wallet_id, amount, idempotency_key):
    amount_paise = rupees_to_paise(amount)

    if not idempotency_key:
        raise ValueError("Transaction key is required.")

    try:
        existing = db.session.scalar(
            select(Transaction).where(
                Transaction.idempotency_key == idempotency_key
            )
        )

        if existing:
            raise DuplicateTransactionError(
                "This transaction has already been processed."
            )

        result = db.session.execute(
            update(Wallet)
            .where(Wallet.id == wallet_id)
            .values(
                balance_paise=Wallet.balance_paise + amount_paise
            )
        )

        if result.rowcount != 1:
            raise ValueError("Wallet not found.")

        transaction = Transaction(
            transaction_type="deposit",
            amount_paise=amount_paise,
            receiver_wallet_id=wallet_id,
            idempotency_key=idempotency_key,
            description="Demo wallet deposit"
        )

        db.session.add(transaction)
        db.session.commit()

        return transaction

    except IntegrityError:
        db.session.rollback()
        raise DuplicateTransactionError(
            "This transaction has already been processed."
        )

    except Exception:
        db.session.rollback()
        raise


def transfer_funds(sender_wallet_id, recipient_email, amount, idempotency_key):
    amount_paise = rupees_to_paise(amount)
    recipient_email = recipient_email.strip().lower()

    if not idempotency_key:
        raise ValueError("Transaction key is required.")

    try:
        existing = db.session.scalar(
            select(Transaction).where(
                Transaction.idempotency_key == idempotency_key
            )
        )

        if existing:
            raise DuplicateTransactionError(
                "This transaction has already been processed."
            )

        sender = db.session.get(Wallet, sender_wallet_id)

        if not sender:
            raise ValueError("Sender wallet not found.")

        recipient = db.session.scalar(
            select(Wallet)
            .join(User, Wallet.user_id == User.id)
            .where(User.email == recipient_email)
        )

        if not recipient:
            raise RecipientNotFoundError(
                "Recipient account not found."
            )

        if sender.id == recipient.id:
            raise ValueError("You cannot transfer money to yourself.")

        debit_result = db.session.execute(
            update(Wallet)
            .where(
                Wallet.id == sender_wallet_id,
                Wallet.balance_paise >= amount_paise
            )
            .values(
                balance_paise=Wallet.balance_paise - amount_paise
            )
        )

        if debit_result.rowcount != 1:
            raise InsufficientBalanceError(
                "Insufficient wallet balance."
            )

        db.session.execute(
            update(Wallet)
            .where(Wallet.id == recipient.id)
            .values(
                balance_paise=Wallet.balance_paise + amount_paise
            )
        )

        transaction = Transaction(
            transaction_type="transfer",
            amount_paise=amount_paise,
            sender_wallet_id=sender_wallet_id,
            receiver_wallet_id=recipient.id,
            idempotency_key=idempotency_key,
            description=f"Transfer to {recipient_email}"
        )

        db.session.add(transaction)
        db.session.commit()

        return transaction

    except IntegrityError:
        db.session.rollback()
        raise DuplicateTransactionError(
            "This transaction has already been processed."
        )

    except Exception:
        db.session.rollback()
        raise