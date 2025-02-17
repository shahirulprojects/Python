# match-case statements (structural pattern matching)
# introduced in python 3.10

# basic match-case
def check_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:  # default case (like else)
            return "Unknown Status"

print("HTTP Status Codes:")
print("200:", check_status(200))
print("404:", check_status(404))
print("999:", check_status(999))

# matching with multiple values
def check_command(command):
    match command:
        case "quit" | "exit" | "bye":
            return "Exiting program"
        case "help" | "?":
            return "Showing help"
        case _:
            return "Unknown command"

print("\nCommands:")
print("quit:", check_command("quit"))
print("?:", check_command("?"))
print("hello:", check_command("hello"))

# matching with patterns
def analyze_point(point):
    match point:
        case (0, 0):
            return "At origin"
        case (0, y):
            return f"On y-axis at y={y}"
        case (x, 0):
            return f"On x-axis at x={x}"
        case (x, y):
            return f"At point ({x}, {y})"
        case _:
            return "Not a point"

print("\nPoint Analysis:")
print("(0, 0):", analyze_point((0, 0)))
print("(0, 5):", analyze_point((0, 5)))
print("(3, 4):", analyze_point((3, 4)))

# matching with class patterns
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def analyze_shape(shape):
    match shape:
        case Point(x=0, y=0):
            return "Point at origin"
        case Point(x=x, y=y) if x == y:
            return f"Point on diagonal at {x}"
        case Point():
            return "Point at some location"
        case _:
            return "Not a point"

print("\nShape Analysis:")
print("Point(0, 0):", analyze_shape(Point(0, 0)))
print("Point(2, 2):", analyze_shape(Point(2, 2)))
print("Point(1, 2):", analyze_shape(Point(1, 2)))

# matching with lists and patterns
def analyze_coordinates(coords):
    match coords:
        case []:
            return "Empty sequence"
        case [x, y]:
            return f"Single point: ({x}, {y})"
        case [x, y, *rest]:
            return f"Line starting at ({x}, {y}) with {len(rest)} more points"
        case _:
            return "Invalid coordinates"

print("\nCoordinate Analysis:")
print("[]:", analyze_coordinates([]))
print("[1, 2]:", analyze_coordinates([1, 2]))
print("[1, 2, 3, 4]:", analyze_coordinates([1, 2, 3, 4]))

# matching with dictionaries
def analyze_person(person):
    match person:
        case {"name": str(name), "age": int(age)} if age < 18:
            return f"{name} is a minor"
        case {"name": str(name), "age": int(age)}:
            return f"{name} is an adult"
        case {"name": str(name)}:
            return f"{name}'s age is unknown"
        case _:
            return "Invalid person data"

print("\nPerson Analysis:")
print(analyze_person({"name": "Alice", "age": 15}))
print(analyze_person({"name": "Bob", "age": 25}))
print(analyze_person({"name": "Charlie"}))

# matching with complex patterns
def analyze_data(data):
    match data:
        case {"type": "user", "data": {"name": str(name), "age": int(age)}}:
            return f"User {name}, age {age}"
        case {"type": "point", "data": [x, y]}:
            return f"Point at ({x}, {y})"
        case {"type": str(type_name)}:
            return f"Unknown type: {type_name}"
        case _:
            return "Invalid data format"

print("\nData Analysis:")
print(analyze_data({"type": "user", "data": {"name": "Alice", "age": 25}}))
print(analyze_data({"type": "point", "data": [3, 4]}))
print(analyze_data({"type": "unknown"}))

# practice exercises:
# 1. create a calculator that:
#    - takes an operator and two numbers
#    - uses match to perform the operation
#    - handles division by zero
#    - supports basic and advanced operations

# 2. create a command parser that:
#    - processes different command formats
#    - extracts command arguments
#    - handles flags and options
#    - supports subcommands

# 3. create a data validator that:
#    - validates different data structures
#    - checks types and values
#    - provides detailed error messages
#    - supports nested structures

# example solution for #1:
def calculate(operation):
    match operation:
        case ("+", x, y):
            return x + y
        case ("-", x, y):
            return x - y
        case ("*", x, y):
            return x * y
        case ("/", x, y) if y != 0:
            return x / y
        case ("/", _, 0):
            return "Error: Division by zero"
        case ("**", x, y):
            return x ** y
        case _:
            return "Invalid operation"

print("\nCalculator:")
print("2 + 3 =", calculate(("+", 2, 3)))
print("5 - 2 =", calculate(("-", 5, 2)))
print("3 * 4 =", calculate(("*", 3, 4)))
print("6 / 2 =", calculate(("/", 6, 2)))
print("5 / 0 =", calculate(("/", 5, 0)))
print("2 ** 3 =", calculate(("**", 2, 3))) 