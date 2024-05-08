import re
from typing import Any
from functools import lru_cache


@lru_cache
def integer_converter(value: Any) -> int:
    """_summary_

    Args:
        value (int | float | str): _description_

    Returns:
        _type_: _description_
    """
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        cleaned_value = re.sub(r"\D", "", value)
        try:
            return int(cleaned_value)
        except ValueError as verror:
            print(verror)
            return 0
        except Exception as error:
            print(error)
            return 0
    return 0
