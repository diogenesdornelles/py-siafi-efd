from typing import Any, Hashable
from pandas import DataFrame
from sheets.siafi import Siafi
from sheets.efd import Efd
import numpy as np  # type: ignore
from components.component import Variables, Component
from pub_sub.pub_sub import pub_sub


class Parse:
    """ """

    def __init__(self, table: Component, info: Component) -> None:
        self._df: DataFrame | None = None
        self._siafi = None
        self._efd = None
        self._as_dict = {}
        self._info = info
        self._table = table
        self._describe = {}

    @property
    def df(self) -> DataFrame | None:
        return self._df

    @property
    def siafi(self) -> Siafi | None:
        return self._siafi

    @siafi.setter
    def siafi(self, value: Siafi) -> None:
        self._siafi = value
        self.pipeline()

    @property
    def efd(self) -> Efd | None:
        return self._efd

    @efd.setter
    def efd(self, value: Efd) -> None:
        self._efd = value
        self.pipeline()

    def pipeline(self) -> None:
        self.parse()
        self.sanitize_columns()
        self.set_dict()
        self.set_describe()
        self.set_view()

    @property
    def as_dict(self) -> dict[Hashable, Any] | None:
        return self._as_dict

    @property
    def table(self) -> Component:
        return self._table

    @property
    def info(self) -> Component:
        return self._info

    @property
    def describe(self) -> dict[Hashable, Any]:
        return self._describe

    def parse(self):
        if (isinstance(self._siafi, Siafi)) and (
            isinstance(self._efd, Efd)
            and (isinstance(self._efd.df, DataFrame))
            and (isinstance(self._siafi.df, DataFrame))
        ):
            self._df = self._siafi.df.merge(
                right=self._efd.df,
                how="outer",
                left_on="RECOLHEDOR",
                right_on="CNPJ",
                suffixes=("_SIAFI", "_EFD"),
            )

            self._df["DIFERENÇAS"] = self._df["VALOR_SIAFI"] - self._df["VALOR_EFD"]
            self._df["DIFERENÇAS"] = self._df["DIFERENÇAS"].round(2)
            self._df.reset_index(drop=True, inplace=True)
            self._df.set_index(np.arange(1, self._df.shape[0] + 1), inplace=True)

    def sanitize_columns(self):
        """_summary_"""
        if isinstance(self._df, DataFrame):
            self._df["RECOLHEDOR"] = self._df["RECOLHEDOR"].astype(
                "Int64",
                copy=False,
            )
            self._df["VALOR_SIAFI"] = self._df["VALOR_SIAFI"].astype(
                "Float64",
                copy=False,
            )
            self._df["CNPJ"] = self._df["CNPJ"].astype(
                "Int64",
                copy=False,
            )
            self._df["VALOR_EFD"] = self._df["VALOR_EFD"].astype(
                "Float64",
                copy=False,
            )
            self._df["DOCUMENTO"] = self._df["DOCUMENTO"].astype(
                "Int64",
                copy=False,
            )
            self._df["CNO"] = self._df["CNO"].astype(
                "Int64",
                copy=False,
            )
            self._df["DIFERENÇAS"] = self._df["DIFERENÇAS"].astype(
                "Float64",
                copy=False,
            )
            self._df.reset_index(drop=True, inplace=True)

    def set_dict(self) -> None:
        if isinstance(self._df, DataFrame):
            self._as_dict = self._df.to_dict(orient="list")

    def set_describe(self) -> None:
        if isinstance(self._df, DataFrame):
            df_siafi_only = self._df.query("VALOR_EFD == False")
            df_efd_only = self._df.query("VALOR_SIAFI == False")

            self._describe = self._df.describe().to_dict("dict")["DIFERENÇAS"]
            self._describe["sum"] = round(self._df["DIFERENÇAS"].sum(), 2)
            self._describe["mean"] = round(self._describe["mean"], 2)
            self._describe["max"] = round(self._describe["max"], 2)
            self._describe["min"] = round(self._describe["min"], 2)
            self._describe["count"] = int(self._describe["count"])

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
