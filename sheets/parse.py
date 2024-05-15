from typing import Any, Hashable

import matplotlib.pyplot as plt
import numpy as np  # type: ignore
import pandas as pd
import seaborn as sns
from pandas import DataFrame

from components.component import Component, Variables
from pub_sub.pub_sub import pub_sub
from sheets.efd import Efd
from sheets.siafi import Siafi
from utils.format_brl_currency import format_brl_currency


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
        self._df_siafi_only = None
        self._df_efd_only = None
        self._df_siafi_greater = None
        self._df_efd_greater = None

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
        self.set_siafi_greater()
        self.set_efd_greater()
        self.set_dict()
        self.set_describe()
        self.set_plot()
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
            self._df.fillna(0.00, inplace=True)
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

    def set_siafi_greater(self) -> None:
        if isinstance(self._df, DataFrame):
            self._df_siafi_greater = self._df[
                self._df["VALOR_SIAFI"] > self._df["VALOR_EFD"]
            ]
            self._df_siafi_greater = self._df_siafi_greater.reset_index()

    def set_efd_greater(self) -> None:
        if isinstance(self._df, DataFrame):
            self._df_efd_greater = self._df[
                self._df["VALOR_EFD"] > self._df["VALOR_SIAFI"]
            ]
            self._df_efd_greater = self._df_efd_greater.reset_index()

    def set_dict(self) -> None:
        if isinstance(self._df, DataFrame):
            self._as_dict = self._df.to_dict(orient="list")

    def set_describe(self) -> None:
        if (
            isinstance(self._df, DataFrame)
            and isinstance(self._df_siafi_greater, DataFrame)
            and isinstance(self._df_efd_greater, DataFrame)
        ):
            self._describe["greater_siafi_sum"] = format_brl_currency(
                abs(round(self._df_siafi_greater["DIFERENÇAS"].sum(), 2))
            )
            self._describe["greater_efd_sum"] = format_brl_currency(
                abs(round(self._df_efd_greater["DIFERENÇAS"].sum(), 2))
            )
            self._describe["greater_siafi_count"] = int(self._df_siafi_greater.shape[0])
            self._describe["greater_efd_count"] = int(self._df_efd_greater.shape[0])
            self._describe["greater_siafi_recolhedor"] = self._df_siafi_greater[
                "RECOLHEDOR"
            ].values.tolist()
            self._describe["greater_efd_cnpj"] = self._df_efd_greater[
                "CNPJ"
            ].values.tolist()
            self._describe["sum"] = format_brl_currency(
                round(self._df["VALOR_SIAFI"].sum() - self._df["VALOR_EFD"].sum(), 2)
            )

    def set_plot(self) -> None:
        if isinstance(self._df, DataFrame):
            concatenated_df = pd.concat(
                [
                    self._df_efd_greater,
                    self._df_siafi_greater,
                ],
                axis=0,
            )
            concatenated_df.set_index(np.arange(1, concatenated_df.shape[0] + 1), inplace=True)
            plt.figure(figsize=(10, 6))
            data = [
                f"Rec-{rec}\nCNPJ-{cnpj}"
                for rec, cnpj in zip(
                    concatenated_df["RECOLHEDOR"], concatenated_df["CNPJ"]
                )
            ]
            ax = sns.barplot(
                x=data,
                y=concatenated_df["DIFERENÇAS"],
                palette=[
                    "red" if x < 0 else "blue" for x in concatenated_df["DIFERENÇAS"]
                ],
                hue=data
            )
            plt.xlabel("Recolhedor e CNPJ")
            plt.ylabel("Diferenças")
            plt.title("Diferenças entre VALOR_SIAFI e VALOR_EFD")
            plt.xticks(rotation=45, ha="right")

            for idx, diff in enumerate(concatenated_df["DIFERENÇAS"]):
                ax.text(
                    idx,
                    diff,
                    f"{diff:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=11,
                    color="black",
                )

            plt.axhline(
                0, color="black", linewidth=0.5
            )
            plt.tight_layout()
            plt.show()

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
