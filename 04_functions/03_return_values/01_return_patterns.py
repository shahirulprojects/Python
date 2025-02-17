# function return values and patterns in python

# basic return values
def square(n):
    return n * n

print("basic return value:")
result = square(5)
print(f"square of 5: {result}")

# multiple return values
def get_dimensions():
    length = 10
    width = 20
    height = 30
    return length, width, height  # returns tuple

print("\nmultiple return values:")
l, w, h = get_dimensions()  # tuple unpacking
print(f"dimensions: {l} x {w} x {h}")

# returning different types
def process_number(n):
    if n < 0:
        return None  # return None for invalid input
    elif n == 0:
        return 0  # return integer
    else:
        return float(n)  # return float

print("\nreturning different types:")
print(f"process -1: {process_number(-1)}")
print(f"process 0: {process_number(0)}")
print(f"process 5: {process_number(5)}")

# returning collections
def create_person(name, age):
    # return dictionary
    return {
        "name": name,
        "age": age,
        "greet": lambda: f"hello, i'm {name}"
    }

print("\nreturning dictionary:")
person = create_person("alice", 25)
print(f"person: {person}")
print(f"greeting: {person['greet']()}")

# returning functions (closures)
def create_multiplier(factor):
    def multiplier(x):
        return x * factor
    return multiplier

print("\nreturning function:")
double = create_multiplier(2)
triple = create_multiplier(3)
print(f"double 5: {double(5)}")
print(f"triple 5: {triple(5)}")

# returning generators
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print("\nreturning generator:")
fib = fibonacci(5)
print("fibonacci sequence:")
for num in fib:
    print(num, end=" ")
print()

# returning with context
class DatabaseConnection:
    def __enter__(self):
        print("connecting to database...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("closing database connection...")
    
    def query(self, sql):
        return f"executing query: {sql}"

def get_user_data(user_id):
    with DatabaseConnection() as db:
        result = db.query(f"select * from users where id = {user_id}")
        return result

print("\nreturning with context:")
data = get_user_data(123)
print(data)

# returning status codes
def save_file(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return True, "file saved successfully"
    except Exception as e:
        return False, str(e)

print("\nreturning status codes:")
success, message = save_file("test.txt", "hello world")
print(f"success: {success}, message: {message}")

# returning optional values
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    users = {1: "alice", 2: "bob"}
    return {"id": user_id, "name": users[user_id]} if user_id in users else None

print("\nreturning optional values:")
print(f"find user 1: {find_user(1)}")
print(f"find user 3: {find_user(3)}")

# practice exercises:
# 1. create a function that:
#    - takes a list of numbers
#    - returns multiple statistical values
#    - (mean, median, mode, standard deviation)
#    - handles empty lists and invalid inputs

# 2. create a function that:
#    - implements a custom iterator
#    - yields values with specific pattern
#    - allows for configuration
#    - includes error handling

# 3. create a function that:
#    - processes text data
#    - returns structured analysis
#    - includes word count, unique words
#    - returns generator for word patterns

# example solution for #1:
from statistics import mean, median, mode, stdev
from typing import Optional, Tuple

def calculate_statistics(numbers: list) -> Tuple[Optional[float], Optional[float], 
                                               Optional[float], Optional[float]]:
    """
    calculate statistical values for a list of numbers.
    
    args:
        numbers: list of numbers to analyze
    
    returns:
        tuple of (mean, median, mode, standard deviation)
        returns (none, none, none, none) for empty or invalid input
    """
    if not numbers:
        return None, None, None, None
    
    try:
        return (
            mean(numbers),
            median(numbers),
            mode(numbers),
            stdev(numbers) if len(numbers) > 1 else None
        )
    except Exception as e:
        print(f"error calculating statistics: {e}")
        return None, None, None, None

# testing the solution
test_data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
mean_val, median_val, mode_val, stdev_val = calculate_statistics(test_data)
print("\nstatistical analysis:")
print(f"data: {test_data}")
print(f"mean: {mean_val:.2f}")
print(f"median: {median_val:.2f}")
print(f"mode: {mode_val}")
print(f"standard deviation: {stdev_val:.2f}") 