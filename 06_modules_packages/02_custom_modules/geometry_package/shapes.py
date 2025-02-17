# shape classes for geometry package
from abc import ABC, abstractmethod
from typing import Dict, Any
from .constants import PI

class Shape(ABC):
    """abstract base class for geometric shapes."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def area(self) -> float:
        """calculate the area of the shape."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """calculate the perimeter of the shape."""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """convert shape to dictionary representation."""
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "area": self.area(),
            "perimeter": self.perimeter()
        }
    
    def __str__(self) -> str:
        return f"{self.name} (area: {self.area():.2f}, perimeter: {self.perimeter():.2f})"

class Circle(Shape):
    """circle shape class."""
    
    def __init__(self, radius: float):
        super().__init__("circle")
        self.radius = radius
    
    def area(self) -> float:
        return PI * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * PI * self.radius
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["radius"] = self.radius
        return data

class Rectangle(Shape):
    """rectangle shape class."""
    
    def __init__(self, width: float, height: float):
        super().__init__("rectangle")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "width": self.width,
            "height": self.height
        })
        return data

class Square(Rectangle):
    """square shape class (special case of rectangle)."""
    
    def __init__(self, side: float):
        super().__init__(side, side)
        self.name = "square"
        self.side = side
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["side"] = self.side
        return data 