import re


def validate_full_name(full_name):
    """Check whether the full name is valid."""

    if not full_name or not full_name.strip():
        raise ValueError("Full name is required.")

    if len(full_name.strip()) > 100:
        raise ValueError("Full name cannot exceed 100 characters.")

    return full_name.strip()


def validate_email(email):
    """Check whether the email address has a valid format."""

    if not email or not email.strip():
        raise ValueError("Email address is required.")

    email = email.strip().lower()

    email_pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

    if not re.match(email_pattern, email):
        raise ValueError("Enter a valid email address.")

    if len(email) > 120:
        raise ValueError("Email cannot exceed 120 characters.")

    return email


def validate_password(password):
    """Check basic password requirements."""

    if not password:
        raise ValueError("Password is required.")

    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    return password