import re
from functools import lru_cache
from typing import Any


@lru_cache
def float_converter(value: Any) -> float:
    """Converts a string containing a float value into a float.

    Args:
        value (int | float | str): The value to convert, which could be an integer, float, or a string.
    Returns:
        float: The converted float value.
    """
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        _match = re.search(r"(?P<with_comma>[\d.,]+)|(?P<without_comma>[\d.]+)", value)
        if _match:
            cleaned_value = _match.group("with_comma") or _match.group("without_comma")
            if "," in cleaned_value:
                cleaned_value = cleaned_value.replace(".", "")
                cleaned_value = cleaned_value.replace(
                    ",", ".", cleaned_value.count(".") - 1
                )
            else:
                cleaned_value = cleaned_value.replace(
                    ".", "", cleaned_value.count(".") - 1
                )
            try:
                return float(cleaned_value)
            except ValueError as verror:
                print(verror)
                return 0.0
            except Exception as error:
                print(error)
                return 0.0
    return 0.0
