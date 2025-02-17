# tests for geometry package plugin system
import pytest
from geometry_package.plugin_system import ShapePlugin, PluginManager

# mock plugins for testing
class MockCirclePlugin(ShapePlugin):
    def get_name(self) -> str:
        return "circle"
    
    def calculate_area(self, **params) -> float:
        if "radius" not in params:
            raise ValueError("radius required")
        return 3.14159 * params["radius"] ** 2
    
    def get_parameters(self) -> list:
        return ["radius"]

class MockRectanglePlugin(ShapePlugin):
    def get_name(self) -> str:
        return "rectangle"
    
    def calculate_area(self, **params) -> float:
        if "width" not in params or "height" not in params:
            raise ValueError("width and height required")
        return params["width"] * params["height"]
    
    def get_parameters(self) -> list:
        return ["width", "height"]

# mock entry points
class MockEntryPoint:
    def __init__(self, name, plugin_class):
        self.name = name
        self._plugin_class = plugin_class
    
    def load(self):
        return self._plugin_class

@pytest.fixture
def mock_entry_points(monkeypatch):
    """fixture to mock pkg_resources.iter_entry_points."""
    def mock_iter_entry_points(group):
        if group == "geometry.plugins":
            return [
                MockEntryPoint("circle", MockCirclePlugin),
                MockEntryPoint("rectangle", MockRectanglePlugin)
            ]
        return []
    
    import pkg_resources
    monkeypatch.setattr(pkg_resources, "iter_entry_points", mock_iter_entry_points)

class TestPluginSystem:
    """test cases for plugin system."""
    
    def test_plugin_loading(self, mock_entry_points):
        """test plugin loading from entry points."""
        manager = PluginManager()
        assert len(manager.plugins) == 2
        assert "circle" in manager.plugins
        assert "rectangle" in manager.plugins
    
    def test_plugin_listing(self, mock_entry_points):
        """test listing available plugins."""
        manager = PluginManager()
        plugins = manager.list_plugins()
        assert len(plugins) == 2
        assert "circle" in plugins
        assert "rectangle" in plugins
    
    def test_get_plugin(self, mock_entry_points):
        """test getting specific plugin."""
        manager = PluginManager()
        circle_plugin = manager.get_plugin("circle")
        assert issubclass(circle_plugin, ShapePlugin)
        assert circle_plugin().get_name() == "circle"
    
    def test_invalid_plugin(self, mock_entry_points):
        """test getting non-existent plugin."""
        manager = PluginManager()
        with pytest.raises(ValueError):
            manager.get_plugin("triangle")
    
    def test_circle_area_calculation(self, mock_entry_points):
        """test area calculation using circle plugin."""
        manager = PluginManager()
        area = manager.calculate_area("circle", radius=5)
        expected_area = 3.14159 * 25
        assert abs(area - expected_area) < 1e-10
    
    def test_rectangle_area_calculation(self, mock_entry_points):
        """test area calculation using rectangle plugin."""
        manager = PluginManager()
        area = manager.calculate_area("rectangle", width=4, height=3)
        assert area == 12
    
    def test_missing_parameters(self, mock_entry_points):
        """test error handling for missing parameters."""
        manager = PluginManager()
        with pytest.raises(ValueError):
            manager.calculate_area("circle")  # missing radius
        with pytest.raises(ValueError):
            manager.calculate_area("rectangle", width=4)  # missing height
    
    def test_plugin_parameters(self, mock_entry_points):
        """test getting plugin parameters."""
        manager = PluginManager()
        circle_plugin = manager.get_plugin("circle")()
        rect_plugin = manager.get_plugin("rectangle")()
        
        assert circle_plugin.get_parameters() == ["radius"]
        assert rect_plugin.get_parameters() == ["width", "height"]

# integration test example
def test_plugin_integration(mock_entry_points):
    """test complete plugin workflow."""
    manager = PluginManager()
    
    # list plugins
    plugins = manager.list_plugins()
    assert len(plugins) == 2
    
    # calculate areas
    circle_area = manager.calculate_area("circle", radius=2)
    rect_area = manager.calculate_area("rectangle", width=3, height=4)
    
    # verify results
    assert abs(circle_area - (3.14159 * 4)) < 1e-10
    assert rect_area == 12 