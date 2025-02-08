import pytest
from format_brl_currency import format_brl_currency

def test_positive_float():
    assert format_brl_currency(1234.56).replace('\xa0', ' ') == "R$ 1.234,56"

def test_negative_float():
    assert format_brl_currency(-1234.56).replace('\xa0', ' ') == "-R$ 1.234,56"

def test_zero():
    assert format_brl_currency(0).replace('\xa0', ' ') == "R$ 0,00"

def test_large_number():
    assert format_brl_currency(1234567890.12).replace('\xa0', ' ') == "R$ 1.234.567.890,12"

def test_invalid_string():
    assert format_brl_currency("invalid").replace('\xa0', ' ') == "R$ 0,00"

def test_none_value():
    assert format_brl_currency(None).replace('\xa0', ' ') == "R$ 0,00"

def test_integer_value():
    assert format_brl_currency(1234.0).replace('\xa0', ' ') == "R$ 1.234,00"

if __name__ == "__main__":
    pytest.main()