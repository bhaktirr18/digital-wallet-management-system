from sqlalchemy import select

from app.extensions import db
from app.models import User, Wallet
from app.utils.validators import (
    validate_full_name,
    validate_email,
    validate_password
)


def register_user(full_name, email, password):
    full_name = validate_full_name(full_name)
    email = validate_email(email)
    password = validate_password(password)

    existing_user = db.session.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise ValueError("An account with this email already exists.")

    user = User(
        full_name=full_name,
        email=email
    )

    user.set_password(password)

    wallet = Wallet(user=user)

    db.session.add(user)
    db.session.add(wallet)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return user


def authenticate_user(email, password):
    email = validate_email(email)

    user = db.session.scalar(
        select(User).where(User.email == email)
    )

    if user and user.check_password(password):
        return user

    return None