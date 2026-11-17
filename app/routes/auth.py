from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from app.services.auth_service import register_user, authenticate_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        try:
            user = register_user(full_name, email, password)
            login_user(user)

            flash("Your account has been created successfully!", "success")
            return redirect(url_for("dashboard.index"))

        except ValueError as error:
            flash(str(error), "danger")

        except IntegrityError:
            flash("An account with this email already exists.", "danger")

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        try:
            user = authenticate_user(email, password)

            if user:
                login_user(user)
                flash("Welcome back!", "success")
                return redirect(url_for("dashboard.index"))

            flash("Invalid email or password.", "danger")

        except ValueError as error:
            flash(str(error), "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))