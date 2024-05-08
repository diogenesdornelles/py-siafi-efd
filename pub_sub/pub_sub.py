from pyscript import document as docpy  # type: ignore
from components.component import Component
from collections import OrderedDict
from .change_disabled import set_enabled, set_disabled


class PubSub:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._components = OrderedDict()
        return cls._instance

    def __init__(self) -> None:
        self._components: OrderedDict[str, Component] = OrderedDict()
        self._root = docpy.getElementById("body")

    def subscribe(self, component: Component) -> None:
        if isinstance(component, Component):
            if component.name not in self._components:
                _ = self._components.setdefault(component.name, component)
            else:
                self._components[component.name] = component

    def unsubscribe(self, name: str) -> None:
        self.unpublish(name)
        if name in self._components:
            del self._components[name]

    def publish(self, name: str) -> bool:
        if name in self._components:
            component = self._components[name]
            parent = docpy.getElementById(f"{component.parent_id}")
            if parent:
                parent.innerHTML = ""
                parent.innerHTML = component.render()
                if component.btn_id:
                    set_enabled(component.btn_id)
                return True
        return False

    def unpublish(self, name: str) -> bool:
        if name in self._components:
            component = self._components[name]
            parent = docpy.getElementById(f"{component.parent_id}")
            child = docpy.getElementById(f"{component.id_}")
            if parent and child:
                parent.removeChild(child)
                if component.btn_id:
                    set_disabled(component.btn_id)
            return True
        return False

pub_sub = PubSub()
