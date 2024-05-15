from typing import Any, Hashable, Literal, TypedDict

from jinja2 import Environment, FileSystemLoader, Template  # type: ignore
from js import alert  # type: ignore

env = Environment(loader=FileSystemLoader("./templates"))


class Variables(TypedDict, total=False):
    table: dict[Hashable, Any]
    len: int
    columns: list[Hashable]
    describe: dict[Hashable, Any]
    ready: bool


class Component:
    def __init__(
        self,
        *, 
        name: str,
        template: str,
        _id: str,
        parent_id: str,
        btn_id: str = "",
        value: str = "",
        src: str = "",
        _class: str = "",
        display: Literal["flex", "hidden", "grid", "block"] = "block",
        variables: Variables = {
            "table": {},
            "len": 0,
            "columns": [""],
            "describe": {},
            "ready": False,
        },
    ):
        self._name = name
        self._id = _id
        self._class = _class
        self._display = display
        self._variables = variables
        self._parent_id = parent_id
        self._btn_id = btn_id
        self._value = value
        self._src = src
        self._env = Environment(loader=FileSystemLoader("./templates"))
        try:
            self._template: Template = self._env.get_template(template)
        except Exception as e:
            print(e)
            self._template: Template = self._env.get_template("empty.html")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def src(self) -> str:
        return self._name

    @src.setter
    def src(self, new_src: str) -> None:
        self._name = new_src

    @property
    def id_(self) -> str:
        return self._id

    @id_.setter
    def id_(self, new_id: str) -> None:
        self._id = new_id

    @property
    def class_(self) -> str:
        return self._class

    @class_.setter
    def class_(self, new_class: str) -> None:
        self._class = new_class

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value

    @property
    def display(self) -> str:
        return self._display

    @display.setter
    def display(self, new_display: Literal["flex", "hidden", "grid", "block"]) -> None:
        self._display = new_display

    @property
    def template(self) -> Template:
        return self._template

    @template.setter
    def template(self, new_template: str) -> None:
        try:
            self._template: Template = self._env.get_template(new_template)
        except Exception as e:
            print(e)
            self._template: Template = self._env.get_template("empty.html")

    @property
    def parent_id(self) -> str:
        return self._parent_id

    @parent_id.setter
    def parent_id(self, new_parent_id: str) -> None:
        self._parent_id = new_parent_id

    @property
    def btn_id(self) -> str:
        return self._btn_id

    @btn_id.setter
    def btn_id(self, new_btn_id: str) -> None:
        self._btn_id = new_btn_id

    @property
    def variables(self) -> Variables:
        return self._variables

    @variables.setter
    def variables(self, new_variables: Variables) -> None:
        self._variables = new_variables

    def unset_var(self) -> None:
        self._variables = Variables(
            table={}, len=0, columns=[""], describe={}, ready=False
        )

    def render(self) -> str:
        try:
            template = self._template.render(
                name=self._name,
                _id=self._id,
                _class=self._class,
                src=self._src,
                **self._variables
            )
            return template
        except TypeError as ts:
            alert(ts)
            return ""
