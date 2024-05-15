from pyscript import document as docpy  # type: ignore


def set_enabled(element_id: str) -> None:
    try:
        docpy.getElementById(f"{element_id}").removeAttribute("disabled", False)
    except Exception as er:
        print(er)


def set_disabled(element_id: str) -> None:
    """_summary_

    Args:
        element_id (str): _description_
    """
    try:
        docpy.getElementById(f"{element_id}").setAttribute("disabled", True)
    except Exception as er:
        print(er)
