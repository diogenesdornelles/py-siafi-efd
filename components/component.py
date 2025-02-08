"""
This code defines classes and types for managing components and variables.

Imports:
- `Any`, `Hashable`, `Literal`, `TypedDict` from `typing`: Used for defining types.
- `Environment`, `FileSystemLoader`, `Template` from `jinja2`: Used for templating.
- `alert` from `js`: Type ignored; used for debugging.

Classes:
- `Variables`: TypedDict to represent variables.
- `Component`: Represents a UI component with methods to render and manage variables.

Variables TypedDict:
- `table`: Dictionary representing table data.
- `len`: Integer representing the length of data.
- `columns`: List of column names.
- `describe`: Dictionary representing descriptive statistics.
- `ready`: Boolean indicating whether the data is ready.

Component Class:
- `__init__`: Constructor method to initialize a Component instance.
- Properties: Getters and setters for component attributes.
- `unset_var()`: Method to reset variables to initial state.
- `render()`: Method to render the component template with provided variables.

Explanation:
- `Variables` is a TypedDict defining the structure of variables used within components.
- `Component` class represents a UI component with properties and methods for managing its attributes and rendering.
- The `render()` method uses Jinja2 templates to render the component with provided variables.
- Various properties provide getters and setters for component attributes such as name, ID, class, value, and display.
- `unset_var()` method resets variables to an initial state.
- Error handling is implemented for template rendering to catch any potential errors.
"""

from typing import Any, Hashable, Literal, TypedDict

from jinja2 import Environment, FileSystemLoader, Template  # type: ignore
from js import alert  # type: ignore

env = Environment(loader=FileSystemLoader("./templates"))


class Variables(TypedDict, total=False):
    """_summary_

    Args:
        TypedDict (_type_): _description_
        total (bool, optional): _description_. Defaults to False.
    """
    table: dict[Hashable, Any]
    len: int
    columns: list[Hashable]
    describe: dict[Hashable, Any]
    ready: bool


class Component:
    """A Python class that introduces methods and atributes to handle dinamic HMTL interacvity
    """
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
        """Initializes a new Component instance.

        Args:
            name (str): The name of the component.
            template (str): The template file name.
            _id (str): The ID of the component.
            parent_id (str): The ID of the parent component.
            btn_id (str, optional): The ID of the button. Defaults to "".
            value (str, optional): The value of the component. Defaults to "".
            src (str, optional): The source of the component. Defaults to "".
            _class (str, optional): The CSS class of the component. Defaults to "".
            display (Literal["flex", "hidden", "grid", "block"], optional): The display property of the component. Defaults to "block".
            variables (Variables, optional): The variables used in the component. Defaults to {}.
        """
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
        """Gets the name of the component.

        Returns:
            str: The name of the component.
        """
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Sets the name of the component.

        Args:
        new_name (str): The new name of the component.
        """
        self._name = new_name

    @property
    def src(self) -> str:
        """Gets the source of the component.

        Returns:
            str: The source of the component.
        """
        return self._name

    @src.setter
    def src(self, new_src: str) -> None:
        """Gets the ID of the component.

        Returns:
            str: The ID of the component.
        """
        self._name = new_src

    @property
    def id_(self) -> str:
        """Gets the ID of the component.

        Returns:
            str: The ID of the component.
        """
        return self._id

    @id_.setter
    def id_(self, new_id: str) -> None:
        """Sets the ID of the component.

        Args:
            new_id (str): The new ID of the component.
        """
        self._id = new_id

    @property
    def class_(self) -> str:
        """Gets the CSS class of the component.

        Returns:
            str: The CSS class of the component.
        """
        return self._class

    @class_.setter
    def class_(self, new_class: str) -> None:
        """Sets the CSS class of the component.

        Args:
            new_class (str): The new CSS class of the component.
        """
        self._class = new_class

    @property
    def value(self) -> str:
        """Gets the value of the component.

        Returns:
            str: The value of the component.
        """
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        """Sets the value of the component.

        Args:
            new_value (str): The new value of the component.
        """
        self._value = new_value

    @property
    def display(self) -> str:
        """Gets the display property of the component.

        Returns:
            str: The display property of the component.
        """
        return self._display

    @display.setter
    def display(self, new_display: Literal["flex", "hidden", "grid", "block"]) -> None:
        """Sets the display property of the component.

        Args:
            new_display (Literal["flex", "hidden", "grid", "block"]): The new display property of the component.
        """
        self._display = new_display

    @property
    def template(self) -> Template:
        """Gets the template of the component.

        Returns:
            Template: The template of the component.
        """
        return self._template

    @template.setter
    def template(self, new_template: str) -> None:
        """Sets the template of the component.

        Args:
            new_template (str): The new template of the component.
        """
        try:
            self._template: Template = self._env.get_template(new_template)
        except Exception as e:
            print(e)
            self._template: Template = self._env.get_template("empty.html")

    @property
    def parent_id(self) -> str:
        """Gets the ID of the parent component.

        Returns:
            str: The ID of the parent component.
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, new_parent_id: str) -> None:
        """Sets the ID of the parent component.

        Args:
            new_parent_id (str): The new ID of the parent component.
        """
        self._parent_id = new_parent_id

    @property
    def btn_id(self) -> str:
        """Gets the ID of the button.

        Returns:
            str: The ID of the button.
        """
        return self._btn_id

    @btn_id.setter
    def btn_id(self, new_btn_id: str) -> None:
        """Sets the ID of the button.

        Args:
            new_btn_id (str): The new ID of the button.
        """
        self._btn_id = new_btn_id

    @property
    def variables(self) -> Variables:
        """Gets the variables used in the component.

        Returns:
            Variables: The variables used in the component.
        """
        return self._variables

    @variables.setter
    def variables(self, new_variables: Variables) -> None:
        """Sets the variables used in the component.

        Args:
            new_variables (Variables): The new variables used in the component.
        """
        self._variables = new_variables

    def unset_var(self) -> None:
        """Resets the variables used in the component to default values."""
        self._variables = Variables(
            table={}, len=0, columns=[""], describe={}, ready=False
        )

    def render(self) -> str:
        """Renders the component template with its variables.

        Returns:
            str: The rendered component template.
        """
        try:
            template = self._template.render(
                name=self._name,
                _id=self._id,
                _class=self._class,
                src=self._src,
                **self._variables,
            )
            return template
        except TypeError as ts:
            alert(ts)
            return ""
