from collections import OrderedDict

from pyscript import document as docpy  # type: ignore

from components.component import Component

from .change_disabled import set_disabled, set_enabled


class PubSub:
    _instance = None

    def __new__(cls):
        """Creates a new instance of PubSub if it doesn't already exist.

        Returns:
            PubSub: An instance of the PubSub class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._components = OrderedDict()
        return cls._instance

    def __init__(self) -> None:
        """Initializes the PubSub instance."""
        self._components: OrderedDict[str, Component] = OrderedDict()
        self._root = docpy.getElementById("body")

    def subscribe(self, component: Component) -> None:
        """Subscribes a component to receive notifications.

        Args:
            component (Component): The component to be subscribed.

        Raises:
            ValueError: If the component is already subscribed.
            ValueError: If the component is not an instance of 'Component'.
        """
        if isinstance(component, Component):
            if component.name not in self._components:
                self._components[component.name] = component
                return
            else:
                raise ValueError("Component already subscribed")
        else:
            raise ValueError("Component must be an instance of 'Component'")

    def unsubscribe(self, name: str) -> None:
        """Unsubscribes a component.

        Args:
            name (str): The name of the component to unsubscribe.
        """
        self.unpublish(name)  # Remove the component instance from the screen
        if name in self._components:
            del self._components[name]

    def publish(self, name: str) -> bool:
        """Publishes a component on the screen.

        Args:
            name (str): The name of the component to publish.

        Raises:
            ValueError: If the component is not found or rendering fails.

        Returns:
            bool: True if publishing is successful, False otherwise.
        """
        if name in self._components:
            component = self._components[name]
            parent = docpy.getElementById(f"{component.parent_id}")
            if parent:
                parent.innerHTML = ""
                parent.innerHTML = component.render()
                set_enabled(component.btn_id)
                return True
        # If the component is not found or rendering fails
        raise ValueError(f"Component '{name}' not found or rendering failed.")

    def unpublish(self, name: str) -> bool:
        """Removes a component from the screen.

        Args:
            name (str): The name of the component to remove.

        Raises:
            ValueError: If the component is not found or cannot be removed.

        Returns:
            bool: True if unpublishing is successful, False otherwise.
        """
        if name in self._components:
            component = self._components[name]
            parent = docpy.getElementById(f"{component.parent_id}")
            child = docpy.getElementById(f"{component.id_}")
            if parent and child:
                parent.removeChild(child)
                set_disabled(component.btn_id)
                return True
            if child:
                child.remove()
                set_disabled(component.btn_id)
                return True
        # If the component is not found or cannot be removed
        raise ValueError(f"Failed to remove component '{name}'.")


pub_sub = PubSub()
