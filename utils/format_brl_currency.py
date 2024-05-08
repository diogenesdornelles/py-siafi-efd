from babel.numbers import format_currency  # type: ignore
from decimal import Decimal
from functools import lru_cache


@lru_cache
def format_brl_currency(value):
    if isinstance(value, (float, int)):
        return format_currency(Decimal(str(value)), "BRL", locale="pt_BR")
    return "R$ 0,00"
