# advanced plugin system using entry points
import pkg_resources
from typing import Dict, Type, List
from abc import ABC, abstractmethod

# plugin base class
class ShapePlugin(ABC):
    """base class for shape plugins."""
    
    @abstractmethod
    def get_name(self) -> str:
        """get the name of the shape."""
        pass
    
    @abstractmethod
    def calculate_area(self, **params) -> float:
        """calculate the area of the shape."""
        pass
    
    @abstractmethod
    def get_parameters(self) -> List[str]:
        """get the required parameters for the shape."""
        pass

# plugin manager
class PluginManager:
    """manages shape plugins using entry points."""
    
    def __init__(self):
        self.plugins: Dict[str, Type[ShapePlugin]] = {}
        self._load_plugins()
    
    def _load_plugins(self):
        """load plugins from entry points."""
        for entry_point in pkg_resources.iter_entry_points('geometry.plugins'):
            try:
                plugin_class = entry_point.load()
                if issubclass(plugin_class, ShapePlugin):
                    plugin = plugin_class()
                    self.plugins[plugin.get_name()] = plugin_class
                    print(f"loaded plugin: {plugin.get_name()}")
            except Exception as e:
                print(f"error loading plugin {entry_point.name}: {e}")
    
    def get_plugin(self, name: str) -> Type[ShapePlugin]:
        """get a plugin by name."""
        if name not in self.plugins:
            raise ValueError(f"plugin '{name}' not found")
        return self.plugins[name]
    
    def list_plugins(self) -> List[str]:
        """list all available plugins."""
        return list(self.plugins.keys())
    
    def calculate_area(self, shape: str, **params) -> float:
        """calculate area using the specified plugin."""
        plugin_class = self.get_plugin(shape)
        plugin = plugin_class()
        return plugin.calculate_area(**params)

# example plugin implementation
class CirclePlugin(ShapePlugin):
    """circle shape plugin."""
    
    def get_name(self) -> str:
        return "circle"
    
    def calculate_area(self, **params) -> float:
        if "radius" not in params:
            raise ValueError("radius parameter required")
        return 3.14159 * params["radius"] ** 2
    
    def get_parameters(self) -> List[str]:
        return ["radius"]

# example usage
def main():
    """demonstrate plugin system usage."""
    # initialize plugin manager
    manager = PluginManager()
    
    # list available plugins
    print("\navailable plugins:")
    for plugin_name in manager.list_plugins():
        plugin = manager.get_plugin(plugin_name)()
        params = plugin.get_parameters()
        print(f"- {plugin_name} (parameters: {', '.join(params)})")
    
    # use a plugin
    try:
        area = manager.calculate_area("circle", radius=5)
        print(f"\ncircle area: {area:.2f}")
    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
    main()

# to register a plugin, add this to setup.py:
"""
setup(
    ...
    entry_points={
        'geometry.plugins': [
            'circle=geometry_package.plugins.circle:CirclePlugin',
            'rectangle=geometry_package.plugins.rectangle:RectanglePlugin',
        ],
    },
    ...
)
""" 