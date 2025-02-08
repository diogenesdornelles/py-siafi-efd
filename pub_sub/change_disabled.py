"""
This module brings functions to enable and desable btns.

Author: Diógenes Dornelles Costa
Creation Date: May 15, 2024
Version: 1.0
"""

from pyscript import document as docpy  # type: ignore


def set_enabled(element_id: str) -> None:
    """Enables the HTML element with the specified ID.

    Args:
        element_id (str): The ID of the HTML element to be enabled.
    """
    try:
        docpy.getElementById(f"{element_id}").removeAttribute("disabled", False)
    except Exception as er:
        print(er)


def set_disabled(element_id: str) -> None:
    """Disables the HTML element with the specified ID.

    Args:
        element_id (str): The ID of the HTML element to be disabled.
    """
    try:
        docpy.getElementById(f"{element_id}").setAttribute("disabled", True)
    except Exception as er:
        print(er)
