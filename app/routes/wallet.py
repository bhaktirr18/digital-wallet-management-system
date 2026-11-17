import secrets

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import select, or_

from app.extensions import db
from app.models import Transaction
from app.services.transaction_service import (
    deposit_funds,
    transfer_funds
)
from app.utils.errors import WalletError

wallet_bp = Blueprint("wallet", __name__, url_prefix="/wallet")


@wallet_bp.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "POST":
        amount = request.form.get("amount", "")
        idempotency_key = request.form.get("idempotency_key", "")

        try:
            deposit_funds(
                current_user.wallet.id,
                amount,
                idempotency_key
            )

            flash("Money added to your wallet successfully!", "success")
            return redirect(url_for("dashboard.index"))

        except (ValueError, WalletError) as error:
            flash(str(error), "danger")

        return render_template(
            "wallet/deposit.html",
            idempotency_key=idempotency_key
        )

    return render_template(
        "wallet/deposit.html",
        idempotency_key=secrets.token_urlsafe(32)
    )


@wallet_bp.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    if request.method == "POST":
        recipient_email = request.form.get("recipient_email", "")
        amount = request.form.get("amount", "")
        idempotency_key = request.form.get("idempotency_key", "")

        try:
            transfer_funds(
                current_user.wallet.id,
                recipient_email,
                amount,
                idempotency_key
            )

            flash("Money transferred successfully!", "success")
            return redirect(url_for("dashboard.index"))

        except (ValueError, WalletError) as error:
            flash(str(error), "danger")

        return render_template(
            "wallet/transfer.html",
            idempotency_key=idempotency_key
        )

    return render_template(
        "wallet/transfer.html",
        idempotency_key=secrets.token_urlsafe(32)
    )


@wallet_bp.route("/history")
@login_required
def history():
    wallet_id = current_user.wallet.id

    transactions = db.session.scalars(
        select(Transaction)
        .where(
            or_(
                Transaction.sender_wallet_id == wallet_id,
                Transaction.receiver_wallet_id == wallet_id
            )
        )
        .order_by(Transaction.created_at.desc())
    ).all()

    return render_template(
        "wallet/history.html",
        transactions=transactions
    )