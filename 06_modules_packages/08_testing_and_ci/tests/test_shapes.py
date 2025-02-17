# tests for geometry package shapes module
import pytest
from geometry_package.shapes import Circle, Square, Rectangle
from geometry_package.constants import PI

class TestCircle:
    """test cases for Circle class."""
    
    def test_circle_creation(self):
        """test circle creation with valid radius."""
        circle = Circle(5.0)
        assert circle.radius == 5.0
        assert circle.name == "circle"
    
    def test_circle_negative_radius(self):
        """test circle creation with negative radius."""
        with pytest.raises(ValueError):
            Circle(-1.0)
    
    def test_circle_area(self):
        """test circle area calculation."""
        circle = Circle(2.0)
        expected_area = PI * 4.0  # r² = 4
        assert abs(circle.area() - expected_area) < 1e-10
    
    def test_circle_perimeter(self):
        """test circle perimeter calculation."""
        circle = Circle(3.0)
        expected_perimeter = 2 * PI * 3.0
        assert abs(circle.perimeter() - expected_perimeter) < 1e-10
    
    def test_circle_to_dict(self):
        """test circle serialization to dictionary."""
        circle = Circle(4.0)
        data = circle.to_dict()
        assert data["type"] == "Circle"
        assert data["name"] == "circle"
        assert data["radius"] == 4.0
        assert "area" in data
        assert "perimeter" in data

class TestRectangle:
    """test cases for Rectangle class."""
    
    def test_rectangle_creation(self):
        """test rectangle creation with valid dimensions."""
        rect = Rectangle(4.0, 3.0)
        assert rect.width == 4.0
        assert rect.height == 3.0
        assert rect.name == "rectangle"
    
    def test_rectangle_negative_dimensions(self):
        """test rectangle creation with negative dimensions."""
        with pytest.raises(ValueError):
            Rectangle(-1.0, 5.0)
        with pytest.raises(ValueError):
            Rectangle(5.0, -1.0)
    
    def test_rectangle_area(self):
        """test rectangle area calculation."""
        rect = Rectangle(4.0, 3.0)
        assert rect.area() == 12.0
    
    def test_rectangle_perimeter(self):
        """test rectangle perimeter calculation."""
        rect = Rectangle(4.0, 3.0)
        assert rect.perimeter() == 14.0
    
    def test_rectangle_to_dict(self):
        """test rectangle serialization to dictionary."""
        rect = Rectangle(4.0, 3.0)
        data = rect.to_dict()
        assert data["type"] == "Rectangle"
        assert data["name"] == "rectangle"
        assert data["width"] == 4.0
        assert data["height"] == 3.0

class TestSquare:
    """test cases for Square class."""
    
    def test_square_creation(self):
        """test square creation with valid side."""
        square = Square(5.0)
        assert square.side == 5.0
        assert square.width == 5.0
        assert square.height == 5.0
        assert square.name == "square"
    
    def test_square_negative_side(self):
        """test square creation with negative side."""
        with pytest.raises(ValueError):
            Square(-1.0)
    
    def test_square_area(self):
        """test square area calculation."""
        square = Square(4.0)
        assert square.area() == 16.0
    
    def test_square_perimeter(self):
        """test square perimeter calculation."""
        square = Square(4.0)
        assert square.perimeter() == 16.0
    
    def test_square_to_dict(self):
        """test square serialization to dictionary."""
        square = Square(4.0)
        data = square.to_dict()
        assert data["type"] == "Square"
        assert data["name"] == "square"
        assert data["side"] == 4.0
        assert "width" in data
        assert "height" in data

@pytest.mark.parametrize("shape,params,expected_area", [
    (Circle, {"radius": 5.0}, PI * 25.0),
    (Square, {"side": 4.0}, 16.0),
    (Rectangle, {"width": 4.0, "height": 3.0}, 12.0),
])
def test_shape_areas(shape, params, expected_area):
    """test area calculations for different shapes."""
    shape_instance = shape(**params)
    assert abs(shape_instance.area() - expected_area) < 1e-10

def test_invalid_shape_creation():
    """test invalid shape creation scenarios."""
    with pytest.raises(ValueError):
        Circle(0)  # zero radius
    with pytest.raises(ValueError):
        Square(0)  # zero side
    with pytest.raises(ValueError):
        Rectangle(0, 5)  # zero width
    with pytest.raises(ValueError):
        Rectangle(5, 0)  # zero height 