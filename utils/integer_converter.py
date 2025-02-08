"""
This module contains functions for converting values to integer.

Author: Diogenes Dornelles Costa
Creation Date: May 15, 2024
Version: 1.0
"""

import re
from functools import lru_cache
from typing import Union


@lru_cache(maxsize=128)
def integer_converter(value: Union[int, float, str]) -> int:
    """Convert a value to an integer.

    The function accepts an integer, float, or string and attempts to convert it to an integer.
    If the value is a string, non-digit characters are removed before conversion.
    If conversion fails, the function returns 0.

    Args:
        value (Union[int, float, str]): The value to convert to an integer.

    Returns:
        int: The converted integer, or 0 if conversion is not possible.
    """
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        cleaned_value = re.sub(r"\D", "", value)
        if cleaned_value:
            try:
                return int(cleaned_value)
            except ValueError:
                pass  # Log the error if logging is required
    return 0
