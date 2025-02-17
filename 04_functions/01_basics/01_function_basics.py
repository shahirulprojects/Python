# introduction to python functions
# functions are reusable blocks of code that perform specific tasks

# basic function definition
def greet():
    print("hello, world!")

# calling a function
print("calling basic function:")
greet()

# function with parameters
def greet_person(name):
    print(f"hello, {name}!")

print("\ncalling function with parameter:")
greet_person("alice")

# function with multiple parameters
def greet_with_time(name, time_of_day):
    print(f"good {time_of_day}, {name}!")

print("\ncalling function with multiple parameters:")
greet_with_time("bob", "morning")

# function with return value
def add_numbers(a, b):
    return a + b

print("\nfunction with return value:")
result = add_numbers(5, 3)
print(f"5 + 3 = {result}")

# function with multiple return values
def get_coordinates():
    x = 10
    y = 20
    return x, y  # returns a tuple

print("\nfunction with multiple return values:")
x, y = get_coordinates()
print(f"coordinates: ({x}, {y})")

# function with default parameters
def greet_with_default(name="user"):
    print(f"hello, {name}!")

print("\nfunction with default parameter:")
greet_with_default()  # uses default value
greet_with_default("charlie")  # uses provided value

# docstrings - function documentation
def calculate_area(length, width):
    """
    calculate the area of a rectangle.
    
    args:
        length (float): the length of the rectangle
        width (float): the width of the rectangle
    
    returns:
        float: the area of the rectangle
    """
    return length * width

print("\nfunction with docstring:")
print(calculate_area.__doc__)
print(f"area of rectangle: {calculate_area(5, 3)}")

# scope and variables
global_var = "i am global"

def demonstrate_scope():
    local_var = "i am local"
    print(f"inside function - local: {local_var}")
    print(f"inside function - global: {global_var}")

print("\ndemonstrating scope:")
demonstrate_scope()
print(f"outside function - global: {global_var}")
# print(local_var)  # this would raise an error

# modifying global variables
counter = 0

def increment_counter():
    global counter  # declare global variable
    counter += 1
    print(f"counter is now: {counter}")

print("\nmodifying global variable:")
increment_counter()
increment_counter()

# nested functions
def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

print("\nnested functions:")
add_five = outer_function(5)
print(f"adding 5 to 3: {add_five(3)}")

# practice exercises:
# 1. create a function that:
#    - takes a list of numbers
#    - returns both the minimum and maximum
#    - handles empty lists appropriately

# 2. create a function that:
#    - takes a string
#    - counts vowels and consonants
#    - returns both counts
#    - ignores spaces and punctuation

# 3. create a function that:
#    - implements a simple calculator
#    - takes two numbers and an operator
#    - returns the result
#    - handles division by zero

# example solution for #1:
def find_min_max(numbers):
    """
    find the minimum and maximum values in a list.
    
    args:
        numbers (list): list of numbers
    
    returns:
        tuple: (minimum, maximum) or (none, none) if list is empty
    """
    if not numbers:
        return None, None
    
    return min(numbers), max(numbers)

# testing the solution
test_numbers = [4, 2, 7, 1, 9, 3]
minimum, maximum = find_min_max(test_numbers)
print(f"\ntest list: {test_numbers}")
print(f"minimum: {minimum}, maximum: {maximum}")
print(f"empty list: {find_min_max([])}") 