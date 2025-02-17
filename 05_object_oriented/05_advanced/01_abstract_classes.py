#!/usr/bin/env python3

# abstract base classes in python
# these are classes that can't be instantiated directly and force subclasses to implement certain methods
# they're useful for defining interfaces that derived classes must follow

from abc import ABC, abstractmethod

class Shape(ABC):
    # abstract base class for shapes
    # by inheriting from ABC, we make this an abstract class
    
    def __init__(self, color):
        # even abstract classes can have concrete methods and attributes
        self.color = color
    
    @abstractmethod
    def area(self):
        # abstract method that all shapes must implement
        # this method has no implementation in the base class
        # all subclasses must provide their own implementation
        pass
    
    @abstractmethod
    def perimeter(self):
        # another abstract method that subclasses must implement
        pass
    
    def describe(self):
        # concrete method that all shapes inherit
        # this doesn't need to be implemented by subclasses
        return f"i am a {self.color} {self.__class__.__name__.lower()}"

class Circle(Shape):
    def __init__(self, radius, color):
        # initialize circle with radius and color
        super().__init__(color)  # call parent class constructor
        self.radius = radius
    
    def area(self):
        # implement the required area method
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        # implement the required perimeter method
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width, height, color):
        # initialize rectangle with width, height and color
        super().__init__(color)
        self.width = width
        self.height = height
    
    def area(self):
        # implement the required area method
        return self.width * self.height
    
    def perimeter(self):
        # implement the required perimeter method
        return 2 * (self.width + self.height)

# practical examples showing how abstract classes work
def demonstrate_abstract_classes():
    try:
        # this will raise an error because we can't instantiate an abstract class
        shape = Shape("red")
    except TypeError as e:
        print(f"can't create a shape directly: {e}")
    
    # create concrete shape instances
    circle = Circle(radius=5, color="blue")
    rectangle = Rectangle(width=4, height=6, color="green")
    
    # use the concrete implementations
    print(f"\ncircle details:")
    print(f"description: {circle.describe()}")
    print(f"area: {circle.area():.2f}")
    print(f"perimeter: {circle.perimeter():.2f}")
    
    print(f"\nrectangle details:")
    print(f"description: {rectangle.describe()}")
    print(f"area: {rectangle.area()}")
    print(f"perimeter: {rectangle.perimeter()}")
    
    # demonstrate polymorphism with abstract base class
    shapes = [circle, rectangle]
    print("\niterating through shapes:")
    for shape in shapes:
        # we can work with different shapes through their common interface
        print(f"{shape.describe()} with area {shape.area():.2f}")

if __name__ == "__main__":
    demonstrate_abstract_classes() 