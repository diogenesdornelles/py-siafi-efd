import pytest
from integer_converter import integer_converter

def test_integer_input():
    assert integer_converter(42) == 42

def test_float_input():
    assert integer_converter(3.14) == 3

def test_string_input_with_digits():
    assert integer_converter("12345") == 12345

def test_string_input_with_mixed_characters():
    assert integer_converter("abc123def") == 123

def test_string_input_with_only_non_digits():
    assert integer_converter("abcdef") == 0

def test_string_input_with_special_characters():
    assert integer_converter("12!@#34") == 1234

def test_empty_string_input():
    assert integer_converter("") == 0

def test_none_input():
    assert integer_converter(None) == 0


if __name__ == "__main__":
    pytest.main()