
from datetime import datetime, timezone

from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    transaction_type = db.Column(
        db.String(20),
        nullable=False
    )

    amount_paise = db.Column(
        db.BigInteger,
        nullable=False
    )

    sender_wallet_id = db.Column(
        db.Integer,
        db.ForeignKey("wallets.id"),
        nullable=True
    )

    receiver_wallet_id = db.Column(
        db.Integer,
        db.ForeignKey("wallets.id"),
        nullable=True
    )

    idempotency_key = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    description = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    sender_wallet = db.relationship(
        "Wallet",
        foreign_keys=[sender_wallet_id]
    )

    receiver_wallet = db.relationship(
        "Wallet",
        foreign_keys=[receiver_wallet_id]
    )

    def __repr__(self):
        return (
            f"<Transaction {self.id}: "
            f"{self.transaction_type}, {self.amount_paise} paise>"
        )
