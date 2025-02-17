# utility functions for geometry package
from typing import Union, List, Dict, Any
import json
from .shapes import Shape, Circle, Rectangle, Square

def calculate_area(shape: Shape) -> float:
    """calculate area of any shape."""
    return shape.area()

def calculate_perimeter(shape: Shape) -> float:
    """calculate perimeter of any shape."""
    return shape.perimeter()

def create_shape(shape_type: str, **kwargs) -> Shape:
    """factory function to create shapes."""
    shape_map = {
        "circle": Circle,
        "rectangle": Rectangle,
        "square": Square
    }
    
    if shape_type not in shape_map:
        raise ValueError(f"unknown shape type: {shape_type}")
    
    return shape_map[shape_type](**kwargs)

def serialize_shape(shape: Shape, format: str = "json") -> Union[Dict[str, Any], str]:
    """serialize a shape to dictionary or JSON string."""
    data = shape.to_dict()
    if format.lower() == "json":
        return json.dumps(data, indent=2)
    return data

def calculate_total_area(shapes: List[Shape]) -> float:
    """calculate total area of multiple shapes."""
    return sum(shape.area() for shape in shapes)

def calculate_total_perimeter(shapes: List[Shape]) -> float:
    """calculate total perimeter of multiple shapes."""
    return sum(shape.perimeter() for shape in shapes)

def sort_shapes_by_area(shapes: List[Shape]) -> List[Shape]:
    """sort shapes by their area."""
    return sorted(shapes, key=lambda s: s.area())

def find_largest_shape(shapes: List[Shape]) -> Shape:
    """find the shape with the largest area."""
    if not shapes:
        raise ValueError("empty shape list")
    return max(shapes, key=lambda s: s.area())

def generate_shape_report(shapes: List[Shape]) -> str:
    """generate a report of shapes and their properties."""
    report = "Shape Report\n"
    report += "=" * 40 + "\n"
    
    for i, shape in enumerate(shapes, 1):
        report += f"\nShape {i}:\n"
        report += f"Type: {shape.__class__.__name__}\n"
        report += f"Area: {shape.area():.2f}\n"
        report += f"Perimeter: {shape.perimeter():.2f}\n"
        report += "-" * 20
    
    report += f"\n\nTotal Shapes: {len(shapes)}\n"
    report += f"Total Area: {calculate_total_area(shapes):.2f}\n"
    report += f"Total Perimeter: {calculate_total_perimeter(shapes):.2f}\n"
    
    return report 