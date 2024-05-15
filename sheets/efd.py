import numpy as np  # type: ignore
from pandas import DataFrame

from components.component import Component, Variables
from pub_sub.pub_sub import pub_sub
from utils.float_converter import float_converter
from utils.integer_converter import integer_converter

from .table import Table


class Efd(Table):
    """_summary_"""

    def __init__(self, names: list[str], component: Component, info: Component) -> None:
        """_summary_

        Args:
            file (_type_): _description_
        """
        super().__init__(names, component, info)

    def pipeline(self) -> None:
        self.sanitize_columns()
        self.set_dict()
        self.set_describe()
        self.set_view()

    def sanitize_columns(self):
        """_summary_"""
        if isinstance(self._df, DataFrame):
            self._df["CNPJ"] = self._df["CNPJ"].apply(integer_converter)
            self._df["VALOR"] = self._df["VALOR"].apply(float_converter)
            self._df["VALOR"] = self._df["VALOR"].round(2)
            self._df["CNO"] = 0
            self._df.drop_duplicates(subset="CNPJ", keep="last", inplace=True)
            self._df.sort_values(by="CNPJ", inplace=True)
            self._df.reset_index(drop=True, inplace=True)
            self._df.set_index(np.arange(1, self._df.shape[0] + 1), inplace=True)
            self._df.fillna(0.00, inplace=True)
            

    def set_view(self) -> None:
        if isinstance(self._df, DataFrame):
            self._table.variables = Variables(
                table=self._as_dict,
                len=self._df.shape[0],
                columns=list(self._as_dict.keys()),
                ready=True,
            )
            self._info.variables = Variables(describe=self._describe, ready=True)
            pub_sub.subscribe(self._table)
            pub_sub.subscribe(self._info)
            pub_sub.publish(self._table.name)
            pub_sub.publish(self._info.name)
