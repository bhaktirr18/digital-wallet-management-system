import pytest

from app.utils.money import rupees_to_paise, format_paise


def test_rupees_to_paise():
    assert rupees_to_paise("100") == 10000


def test_rupees_to_paise_with_decimals():
    assert rupees_to_paise("100.50") == 10050


def test_rupees_to_paise_rejects_zero():
    with pytest.raises(ValueError):
        rupees_to_paise("0")


def test_rupees_to_paise_rejects_negative():
    with pytest.raises(ValueError):
        rupees_to_paise("-50")


def test_rupees_to_paise_rejects_invalid_input():
    with pytest.raises(ValueError):
        rupees_to_paise("abc")


def test_rupees_to_paise_rejects_more_than_two_decimals():
    with pytest.raises(ValueError):
        rupees_to_paise("10.555")


def test_format_paise():
    assert format_paise(10050) == "₹100.50"