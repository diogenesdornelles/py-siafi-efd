import pytest
from float_converter import float_converter



def test_integer_input():
    assert float_converter(42) == 42.0

def test_float_input():
    assert float_converter(3.14) == 3.14

def test_string_input_with_dot():
    assert float_converter("3.14") == 3.14

def test_string_input_with_comma():
    assert float_converter("3,14") == 3.14

def test_string_input_with_dot_and_comma():
    assert float_converter("1.234,56") == 1234.56

def test_string_input_with_multiple_dots():
    assert float_converter("1.234.567,89") == 1234567.89

def test_string_input_invalid():
    assert float_converter("invalid") == 0.0

def test_string_input_with_text_and_number():
    assert float_converter("abc123,45def") == 123.45

def test_string_input_empty():
    assert float_converter("") == 0.0

def test_none_input():
    assert float_converter(None) == 0.0

if __name__ == "__main__":
    pytest.main()