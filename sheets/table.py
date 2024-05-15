from abc import ABC, abstractmethod
from typing import Any, Hashable

import pandas as pd
from pandas import DataFrame

from components.component import Component
from utils.format_brl_currency import format_brl_currency


class Table(ABC):
    """_summary_"""

    def __init__(
        self, names: list[str], table: Component, info: Component
    ) -> None:
        """_summary_

        Args:
            file (_type_): _description_
        """
        self._df: DataFrame | None = None
        self._file = None
        self._names = names
        self._as_dict = {}
        self._table = table
        self._info = info
        self._describe = {}
        self._plot = None

    @property
    def df(self) -> DataFrame | None:
        return self._df

    @property
    def file(self) -> Any:
        return self._file

    @file.setter
    def file(self, file: Any) -> None:
        self._file = file
        self._df = pd.read_excel(
            file,
            names=self._names,
            engine="openpyxl",
        )
        self.pipeline()

    @property
    def table(self) -> Component:
        return self._table

    @property
    def info(self) -> Component:
        return self._info

    @property
    def describe(self) -> dict[Hashable, Any]:
        return self._describe

    @property
    def as_dict(self) -> dict[Hashable, Any] | None:
        return self._as_dict

    @abstractmethod
    def pipeline(self) -> None: ...

    @abstractmethod
    def sanitize_columns(self) -> None: ...

    @abstractmethod
    def set_view(self) -> None: ...

    def set_dict(self) -> None:
        if isinstance(self._df, DataFrame):
            self._as_dict = self._df.to_dict(orient="list")

    def set_describe(self) -> None:
        if isinstance(self._df, DataFrame):
            self._describe = self._df.describe().to_dict("dict")["VALOR"]
            self._describe["sum"] = format_brl_currency(
                round(self._df["VALOR"].sum(), 2)
            )
            self._describe["mean"] = format_brl_currency(
                round(self._describe["mean"], 2)
            )
            self._describe["max"] = format_brl_currency(round(self._describe["max"], 2))
            self._describe["min"] = format_brl_currency(round(self._describe["min"], 2))
            self._describe["count"] = int(self._describe["count"])
