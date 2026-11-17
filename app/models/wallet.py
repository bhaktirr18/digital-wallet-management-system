
from datetime import datetime, timezone

from app.extensions import db


class Wallet(db.Model):
    __tablename__ = "wallets"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    balance_paise = db.Column(
        db.BigInteger,
        nullable=False,
        default=0
    )

    currency = db.Column(
        db.String(3),
        nullable=False,
        default="INR"
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship("User", back_populates="wallet")

    def __repr__(self):
        return f"<Wallet {self.id}: {self.balance_paise} paise>"
