
from decimal import Decimal, InvalidOperation


def rupees_to_paise(amount):
    """
    Convert a rupee amount into integer paise.
    Example: '100.50' becomes 10050.
    """

    try:
        value = Decimal(str(amount).strip())
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Enter a valid amount.")

    if not value.is_finite():
        raise ValueError("Enter a valid amount.")

    if value <= 0:
        raise ValueError("Amount must be greater than zero.")

    if value.as_tuple().exponent < -2:
        raise ValueError("Amount cannot have more than two decimal places.")

    return int(value * 100)


def format_paise(amount_paise):
    """Convert integer paise into a formatted rupee amount."""

    return f"₹{Decimal(amount_paise) / Decimal(100):,.2f}"
