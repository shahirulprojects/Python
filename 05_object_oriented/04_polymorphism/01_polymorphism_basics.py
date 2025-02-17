# polymorphism in python
from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any

# basic polymorphism with inheritance
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def describe(self) -> str:
        return f"i am a {self.__class__.__name__}"

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

# using polymorphism with a list of shapes
shapes: List[Shape] = [Rectangle(5, 3), Circle(4)]
print("shape polymorphism:")
for shape in shapes:
    print(f"\n{shape.describe()}")
    print(f"area: {shape.area():.2f}")
    print(f"perimeter: {shape.perimeter():.2f}")

# duck typing polymorphism
class Dog:
    def speak(self) -> str:
        return "woof!"

class Cat:
    def speak(self) -> str:
        return "meow!"

class Duck:
    def speak(self) -> str:
        return "quack!"
    
    def swim(self) -> str:
        return "i'm swimming!"

def make_speak(animal: Any) -> str:
    return animal.speak()

# using duck typing
print("\nduck typing:")
animals = [Dog(), Cat(), Duck()]
for animal in animals:
    print(f"{animal.__class__.__name__} says: {make_speak(animal)}")

# operator overloading polymorphism
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Point':
        return Point(self.x * scalar, self.y * scalar)
    
    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

# using operator overloading
print("\noperator overloading:")
p1 = Point(1, 2)
p2 = Point(3, 4)
print(f"p1: {p1}")
print(f"p2: {p2}")
print(f"p1 + p2: {p1 + p2}")
print(f"p1 * 2: {p1 * 2}")
print(f"p1 == p2: {p1 == p2}")

# method overloading through default arguments
class Calculator:
    def add(self, a: float, b: float = 0, c: float = 0) -> float:
        return a + b + c
    
    def multiply(self, a: float, b: float = 1, c: float = 1) -> float:
        return a * b * c

# using method overloading
print("\nmethod overloading:")
calc = Calculator()
print(f"add(1): {calc.add(1)}")
print(f"add(1, 2): {calc.add(1, 2)}")
print(f"add(1, 2, 3): {calc.add(1, 2, 3)}")

# polymorphism with interfaces (protocols)
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str:
        pass

class Square:
    def __init__(self, side: float):
        self.side = side
    
    def draw(self) -> str:
        return f"drawing a square with side {self.side}"

class Triangle:
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height
    
    def draw(self) -> str:
        return f"drawing a triangle with base {self.base} and height {self.height}"

def draw_shape(shape: Drawable) -> None:
    print(shape.draw())

# using protocol polymorphism
print("\nprotocol polymorphism:")
shapes = [Square(5), Triangle(4, 3)]
for shape in shapes:
    draw_shape(shape)

# polymorphism with generic types
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self):
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        if not self.items:
            raise IndexError("pop from empty stack")
        return self.items.pop()
    
    def peek(self) -> T:
        if not self.items:
            raise IndexError("peek at empty stack")
        return self.items[-1]
    
    def is_empty(self) -> bool:
        return len(self.items) == 0

# using generic stack
print("\ngeneric polymorphism:")
# stack of integers
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(f"int stack peek: {int_stack.peek()}")

# stack of strings
str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")
print(f"string stack peek: {str_stack.peek()}")

# practice exercises:
# 1. create a hierarchy of payment methods that:
#    - implements different payment processors
#    - handles various payment types
#    - processes payments polymorphically
#    - includes validation and error handling

# 2. create a system of file handlers that:
#    - handles different file types
#    - implements common interface
#    - processes files polymorphically
#    - supports extensibility

# 3. create a notification system that:
#    - supports multiple notification types
#    - uses protocol for notification interface
#    - allows easy addition of new types
#    - includes priority and formatting

# example solution for #1:
class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        pass
    
    def format_amount(self, amount: float) -> str:
        return f"${amount:.2f}"

class CreditCard(PaymentMethod):
    def __init__(self, card_number: str, expiry: str, cvv: str):
        self.card_number = card_number
        self.expiry = expiry
        self.cvv = cvv
    
    def process_payment(self, amount: float) -> bool:
        if self.validate():
            print(f"processing credit card payment of {self.format_amount(amount)}")
            return True
        return False
    
    def validate(self) -> bool:
        # simplified validation
        return (len(self.card_number) == 16 and
                len(self.expiry) == 5 and
                len(self.cvv) == 3)

class PayPal(PaymentMethod):
    def __init__(self, email: str):
        self.email = email
    
    def process_payment(self, amount: float) -> bool:
        if self.validate():
            print(f"processing PayPal payment of {self.format_amount(amount)}")
            return True
        return False
    
    def validate(self) -> bool:
        return '@' in self.email

# testing payment methods
print("\ntesting payment methods:")
payments: List[PaymentMethod] = [
    CreditCard("1234567890123456", "12/25", "123"),
    PayPal("user@example.com")
]

for payment_method in payments:
    success = payment_method.process_payment(99.99)
    print(f"payment successful: {success}") 