# custom module example
"""
this is a custom module that demonstrates module creation and usage.
it includes various functions, classes, and variables that can be imported.
"""

# module-level variables
PI = 3.14159
GRAVITY = 9.81
VERSION = "1.0.0"

# module-level functions
def greet(name: str) -> str:
    """return a greeting message."""
    return f"hello, {name}!"

def calculate_circle_area(radius: float) -> float:
    """calculate the area of a circle."""
    return PI * radius ** 2

def calculate_square_area(side: float) -> float:
    """calculate the area of a square."""
    return side ** 2

# module-level class
class Shape:
    """base class for geometric shapes."""
    def __init__(self, name: str):
        self.name = name
    
    def get_area(self) -> float:
        """calculate the area of the shape."""
        raise NotImplementedError("subclasses must implement get_area()")
    
    def __str__(self) -> str:
        return f"{self.name} shape"

class Circle(Shape):
    """circle shape class."""
    def __init__(self, radius: float):
        super().__init__("circle")
        self.radius = radius
    
    def get_area(self) -> float:
        return calculate_circle_area(self.radius)

class Square(Shape):
    """square shape class."""
    def __init__(self, side: float):
        super().__init__("square")
        self.side = side
    
    def get_area(self) -> float:
        return calculate_square_area(self.side)

# private function (by convention, starts with _)
def _internal_helper() -> str:
    """this is an internal helper function."""
    return "this function is not meant to be used outside the module"

# module initialization code
if __name__ == "__main__":
    # this code only runs when the module is run directly
    print("testing module functionality:")
    
    # test functions
    print("\nfunction tests:")
    print(greet("alice"))
    print(f"circle area (r=5): {calculate_circle_area(5):.2f}")
    print(f"square area (s=4): {calculate_square_area(4):.2f}")
    
    # test classes
    print("\nclass tests:")
    circle = Circle(3)
    square = Square(2)
    
    print(f"{circle}: area = {circle.get_area():.2f}")
    print(f"{square}: area = {square.get_area():.2f}")
    
    # test private function
    print("\nprivate function test:")
    print(_internal_helper()) 