
from app.extensions import db, login_manager

from app.models.user import User
from app.models.wallet import Wallet
from app.models.transaction import Transaction


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


__all__ = ["User", "Wallet", "Transaction"]
