"""
This module contains functions for formatting monetary values in different currencies.

Author: Diógenes Dornelles Costa
Creation Date: May 15, 2024
Version: 1.0
"""

from decimal import Decimal
from functools import lru_cache

from babel.numbers import format_currency  # type: ignore


@lru_cache(maxsize=None)
def format_brl_currency(value: float) -> str:
    """Format a numeric value as Brazilian Real (BRL) currency.

    Args:
        value (float): The numeric value to format as currency.

    Returns:
        str: The formatted currency string representing the value in BRL.
    """
    if not isinstance(value, float):
        return "R$ 0,00"
    try:
        # Ensure the value is a Decimal, which is required for precise currency formatting
        decimal_value = Decimal(value)
    except (TypeError, ValueError):
        # If value is not a valid number, return the default currency format
        return "R$ 0,00"

    # Format the Decimal value as currency in the Brazilian Real format
    return format_currency(decimal_value, "BRL", locale="pt_BR")
