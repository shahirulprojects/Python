# inheritance and method overriding in python
from abc import ABC, abstractmethod
from typing import List

# base class (parent class)
class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def speak(self) -> str:
        return "some generic animal sound"
    
    def get_info(self) -> str:
        return f"{self.name} is {self.age} years old"

# derived class (child class)
class Dog(Animal):
    def __init__(self, name: str, age: int, breed: str):
        # call parent class's __init__
        super().__init__(name, age)
        self.breed = breed
    
    # override parent's method
    def speak(self) -> str:
        return "woof!"
    
    # extend parent's method
    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info} and is a {self.breed}"

# another derived class
class Cat(Animal):
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age)
        self.color = color
    
    def speak(self) -> str:
        return "meow!"
    
    def get_info(self) -> str:
        return f"{super().get_info()} and has {self.color} fur"

# testing inheritance
print("basic inheritance:")
dog = Dog("buddy", 5, "golden retriever")
cat = Cat("whiskers", 3, "orange")

print(f"dog: {dog.get_info()}")
print(f"dog says: {dog.speak()}")
print(f"cat: {cat.get_info()}")
print(f"cat says: {cat.speak()}")

# multiple inheritance
class Swimming:
    def swim(self):
        return "i can swim!"

class Flying:
    def fly(self):
        return "i can fly!"

# class inheriting from multiple base classes
class Duck(Animal, Swimming, Flying):
    def speak(self):
        return "quack!"

print("\nmultiple inheritance:")
duck = Duck("donald", 2)
print(f"duck says: {duck.speak()}")
print(f"duck swimming: {duck.swim()}")
print(f"duck flying: {duck.fly()}")

# abstract base class
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def description(self) -> str:
        return f"i am a shape with area {self.area():.2f}"

# concrete classes implementing abstract class
class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius

print("\nabstract classes:")
shapes: List[Shape] = [Rectangle(5, 3), Circle(4)]
for shape in shapes:
    print(f"{type(shape).__name__}:")
    print(f"area: {shape.area():.2f}")
    print(f"perimeter: {shape.perimeter():.2f}")

# method resolution order (MRO)
class A:
    def method(self):
        return "method from A"

class B(A):
    def method(self):
        return "method from B"

class C(A):
    def method(self):
        return "method from C"

class D(B, C):
    pass

print("\nmethod resolution order:")
d = D()
print(f"D's method call: {d.method()}")
print(f"MRO for D: {[cls.__name__ for cls in D.__mro__]}")

# inheritance with private members
class Parent:
    def __init__(self):
        self.__private = "private"  # private attribute
        self._protected = "protected"  # protected attribute
    
    def get_private(self):
        return self.__private

class Child(Parent):
    def access_members(self):
        # can access protected member
        print(f"protected member: {self._protected}")
        # cannot access private member directly
        # but can access through public method
        print(f"private member: {self.get_private()}")

print("\naccess control:")
child = Child()
child.access_members()

# practice exercises:
# 1. create a hierarchy of classes that:
#    - represents different types of vehicles
#    - includes common attributes and methods
#    - implements specific behavior for each type
#    - uses abstract methods where appropriate

# 2. create a system of classes that:
#    - models a library
#    - has different types of media (books, dvds, etc.)
#    - implements common functionality
#    - handles specific features of each media type

# 3. create a class hierarchy that:
#    - represents different employee types
#    - calculates salary differently for each type
#    - handles benefits and bonuses
#    - includes abstract methods for required behavior

# example solution for #1:
class Vehicle(ABC):
    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year
    
    @abstractmethod
    def start(self) -> str:
        pass
    
    @abstractmethod
    def stop(self) -> str:
        pass
    
    def get_info(self) -> str:
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    def __init__(self, make: str, model: str, year: int, num_doors: int):
        super().__init__(make, model, year)
        self.num_doors = num_doors
    
    def start(self) -> str:
        return "starting car engine..."
    
    def stop(self) -> str:
        return "stopping car engine..."

class Motorcycle(Vehicle):
    def __init__(self, make: str, model: str, year: int, has_sidecar: bool):
        super().__init__(make, model, year)
        self.has_sidecar = has_sidecar
    
    def start(self) -> str:
        return "kickstarting motorcycle..."
    
    def stop(self) -> str:
        return "stopping motorcycle..."

# testing the solution
print("\ntesting vehicle hierarchy:")
vehicles: List[Vehicle] = [
    Car("toyota", "camry", 2024, 4),
    Motorcycle("harley-davidson", "sportster", 2023, False)
]

for vehicle in vehicles:
    print(f"\n{vehicle.get_info()}:")
    print(vehicle.start())
    print(vehicle.stop()) 