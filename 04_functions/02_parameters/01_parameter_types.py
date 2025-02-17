# function parameters and arguments in python

# positional parameters
def greet(first_name, last_name):
    print(f"hello, {first_name} {last_name}!")

print("positional parameters:")
greet("john", "doe")  # arguments must be in correct order

# keyword arguments
print("\nkeyword arguments:")
greet(last_name="smith", first_name="jane")  # order doesn't matter

# default parameters
def greet_with_title(name, title="mr."):
    print(f"hello, {title} {name}!")

print("\ndefault parameters:")
greet_with_title("smith")  # uses default title
greet_with_title("johnson", "dr.")  # overrides default

# mixing positional and keyword arguments
def display_info(name, age, city):
    print(f"{name} is {age} years old and lives in {city}")

print("\nmixing argument types:")
display_info("alice", age=25, city="new york")  # valid
# display_info(name="bob", 30, "london")  # invalid: positional after keyword

# variable number of positional arguments (*args)
def sum_numbers(*numbers):
    """sum any number of positional arguments."""
    return sum(numbers)

print("\nvariable positional arguments:")
print(f"sum(1, 2): {sum_numbers(1, 2)}")
print(f"sum(1, 2, 3, 4): {sum_numbers(1, 2, 3, 4)}")

# variable number of keyword arguments (**kwargs)
def print_info(**info):
    """print any number of keyword arguments."""
    for key, value in info.items():
        print(f"{key}: {value}")

print("\nvariable keyword arguments:")
print_info(name="alice", age=25, city="new york", occupation="developer")

# combining all types of parameters
def process_data(required, *args, default="default", **kwargs):
    print(f"required: {required}")
    print(f"args: {args}")
    print(f"default: {default}")
    print(f"kwargs: {kwargs}")

print("\ncombining parameter types:")
process_data("must", 1, 2, 3, default="custom", x=10, y=20)

# parameter annotations (type hints)
def calculate_rectangle_area(length: float, width: float) -> float:
    """calculate rectangle area with type hints."""
    return length * width

print("\nfunction with type hints:")
area = calculate_rectangle_area(5.0, 3.0)
print(f"area: {area}")
print(f"type hints: {calculate_rectangle_area.__annotations__}")

# unpacking arguments
def point_distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

point1 = (0, 0)
point2 = (3, 4)

print("\nunpacking arguments:")
# unpack tuples as arguments
distance = point_distance(*point1, *point2)
print(f"distance between {point1} and {point2}: {distance}")

# keyword-only arguments
def configure_app(*, host="localhost", port=8080):
    """
    configure application with keyword-only arguments.
    must be called with keyword arguments.
    """
    print(f"configuring app with host={host} and port={port}")

print("\nkeyword-only arguments:")
configure_app(port=8000, host="127.0.0.1")
# configure_app("localhost", 8080)  # this would raise an error

# positional-only arguments (python 3.8+)
def divide(a, b, /):
    """
    divide a by b.
    must be called with positional arguments.
    """
    return a / b

print("\npositional-only arguments:")
print(f"10 / 2 = {divide(10, 2)}")
# print(divide(a=10, b=2))  # this would raise an error

# practice exercises:
# 1. create a function that:
#    - takes both required and optional parameters
#    - accepts variable positional arguments
#    - accepts variable keyword arguments
#    - implements a flexible data processing pipeline

# 2. create a function that:
#    - takes keyword-only configuration parameters
#    - validates parameter types
#    - provides default values
#    - raises appropriate errors for invalid input

# 3. create a function that:
#    - implements a mathematical operation
#    - uses positional-only parameters for operands
#    - uses keyword-only parameters for options
#    - includes type hints and documentation

# example solution for #1:
def process_student_data(name, age, /, *subjects, school="unknown", **scores):
    """
    process student data with various parameter types.
    
    args:
        name: student name (positional-only)
        age: student age (positional-only)
        *subjects: variable number of subjects
        school: optional school name (default: "unknown")
        **scores: variable number of subject scores
    """
    print(f"\nprocessing data for {name}:")
    print(f"age: {age}")
    print(f"school: {school}")
    print(f"subjects: {subjects}")
    print(f"scores: {scores}")
    
    if scores:
        average = sum(scores.values()) / len(scores)
        print(f"average score: {average:.2f}")

# testing the solution
process_student_data("alice", 15, 
                    "math", "science", "history",
                    school="high school",
                    math=95, science=88, history=92) 