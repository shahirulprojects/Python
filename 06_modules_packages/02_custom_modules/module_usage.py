# demonstrating custom module usage
from my_module import (
    PI, GRAVITY, VERSION,
    greet, calculate_circle_area, calculate_square_area,
    Circle, Square
)

# using module constants
print("module constants:")
print(f"pi: {PI}")
print(f"gravity: {GRAVITY}")
print(f"version: {VERSION}")

# using module functions
print("\nmodule functions:")
print(greet("bob"))
print(f"circle area (r=3): {calculate_circle_area(3):.2f}")
print(f"square area (s=4): {calculate_square_area(4):.2f}")

# using module classes
print("\nmodule classes:")
shapes = [
    Circle(2),
    Square(3),
    Circle(4),
    Square(5)
]

for shape in shapes:
    print(f"{shape}: area = {shape.get_area():.2f}")

# demonstrating different import styles
print("\ndifferent import styles:")

# style 1: import specific items
from my_module import greet as say_hello
print(say_hello("charlie"))

# style 2: import entire module
import my_module
print(my_module.greet("david"))

# style 3: import with alias
import my_module as mm
print(mm.greet("eve"))

# trying to access private function (not recommended)
try:
    from my_module import _internal_helper
    print(_internal_helper())
except ImportError:
    print("could not import private function")

# practice exercises:
# 1. create a module that:
#    - implements mathematical operations
#    - includes function decorators for logging
#    - provides utility functions
#    - demonstrates proper documentation

# 2. create a module that:
#    - handles file operations
#    - implements context managers
#    - includes error handling
#    - provides progress feedback

# 3. create a module that:
#    - implements data structures
#    - includes iterator protocol
#    - provides serialization
#    - demonstrates proper testing

# example solution for #1:
# (create a new file called math_utils.py)
"""
import math
from functools import wraps
from typing import Callable, Any
import logging

# set up logging
logging.basicConfig(level=logging.INFO)

def log_call(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logging.info(f"calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@log_call
def factorial(n: int) -> int:
    '''calculate factorial of n.'''
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)

@log_call
def fibonacci(n: int) -> list:
    '''generate fibonacci sequence up to n terms.'''
    if n < 0:
        raise ValueError("number of terms cannot be negative")
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

class MathUtils:
    '''utility class for mathematical operations.'''
    
    @staticmethod
    @log_call
    def is_prime(n: int) -> bool:
        '''check if a number is prime.'''
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    @log_call
    def gcd(a: int, b: int) -> int:
        '''calculate greatest common divisor.'''
        while b:
            a, b = b, a % b
        return a
""" 