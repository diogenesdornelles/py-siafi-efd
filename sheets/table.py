"""
This module contains an abstract class that should be implemented by Siafi and Efd sheets.

Author: Diógenes Dornelles Costa
Creation Date: May 15, 2024
Version: 1.0
"""

from abc import ABC, abstractmethod
from typing import Any, Hashable

import pandas as pd
from pandas import DataFrame

from components.component import Component
from utils.format_brl_currency import format_brl_currency
from js import alert, window  # type: ignore


class Table(ABC):
    """Abstract base class for tables."""

    def __init__(self, names: list[str], table: Component, info: Component) -> None:
        """Initialize Table instance.

        Args:
            names (list[str]): Column names for the table.
            table (Component): Table component.
            info (Component): Information component.
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
        """Get the DataFrame representing the table.

        Returns:
            DataFrame | None: DataFrame representing the table.
        """
        return self._df

    @property
    def file(self) -> Any:
        """Get the file associated with the table.

        Returns:
            Any: File associated with the table.
        """
        return self._file

    @file.setter
    def file(self, file: Any) -> None:
        """Set the file associated with the table.

        Args:
            file (Any): File to be associated with the table.
        Returns: None
        """
        self._file = file
        try:
            self._df = pd.read_excel(
                file, names=self._names, engine="openpyxl", usecols=[0, 1, 2]
            )
        except Exception as er:
            alert(f"Erro: {er}")
            window.location.reload()
        self.pipeline()

    @property
    def table(self) -> Component:
        """Get the table component.

        Returns:
            Component: Table component.
        """
        return self._table

    @property
    def info(self) -> Component:
        """Get the information component.

        Returns:
            Component: Information component.
        """
        return self._info

    @property
    def describe(self) -> dict[Hashable, Any]:
        """Get descriptive statistics of the table.

        Returns:
            dict[Hashable, Any]: Descriptive statistics of the table.
        """
        return self._describe

    @property
    def as_dict(self) -> dict[Hashable, Any] | None:
        """Get the table represented as a dictionary.

        Returns:
            dict[Hashable, Any] | None: Table represented as a dictionary.
        """
        return self._as_dict

    @abstractmethod
    def pipeline(self) -> None:
        """Abstract method representing the pipeline for processing the table. Returns None"""

    @abstractmethod
    def sanitize_columns(self) -> None:
        """Abstract method for sanitizing table columns. Returns None"""

    @abstractmethod
    def set_view(self) -> None:
        """Abstract method for setting the table view. Returns None"""

    def set_dict(self) -> None:
        """Convert the table to a dictionary. Returns None"""
        if isinstance(self._df, DataFrame):
            self._as_dict = self._df.to_dict(orient="list")

    def set_describe(self) -> None:
        """Generate descriptive statistics of the table. Returns None"""
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
