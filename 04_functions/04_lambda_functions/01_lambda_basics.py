# lambda functions and functional programming concepts
from functools import reduce
from typing import Callable, List, Any

# basic lambda function
square = lambda x: x * x
print("basic lambda function:")
print(f"square of 5: {square(5)}")

# lambda with multiple parameters
multiply = lambda x, y: x * y
print("\nlambda with multiple parameters:")
print(f"4 * 3 = {multiply(4, 3)}")

# using lambda in sorting
students = [
    {"name": "alice", "grade": 85},
    {"name": "bob", "grade": 92},
    {"name": "charlie", "grade": 78}
]

# sort by grade
sorted_by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
print("\nsorting with lambda:")
for student in sorted_by_grade:
    print(f"{student['name']}: {student['grade']}")

# lambda with map
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, numbers))
print("\nmap with lambda:")
print(f"numbers: {numbers}")
print(f"squares: {squares}")

# lambda with filter
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("\nfilter with lambda:")
print(f"numbers: {numbers}")
print(f"even numbers: {even_numbers}")

# lambda with reduce
product = reduce(lambda x, y: x * y, numbers)
print("\nreduce with lambda:")
print(f"numbers: {numbers}")
print(f"product: {product}")

# combining map, filter, and reduce
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_of_even_squares = reduce(
    lambda x, y: x + y,
    map(lambda x: x * x,
        filter(lambda x: x % 2 == 0, numbers))
)
print("\ncombining functional operations:")
print(f"numbers: {numbers}")
print(f"sum of even squares: {sum_of_even_squares}")

# lambda in higher-order functions
def apply_operation(x: int, operation: Callable[[int], int]) -> int:
    return operation(x)

print("\nlambda in higher-order functions:")
print(f"double 5: {apply_operation(5, lambda x: x * 2)}")
print(f"square 5: {apply_operation(5, lambda x: x * x)}")

# lambda with conditional expressions
is_even = lambda x: "even" if x % 2 == 0 else "odd"
print("\nlambda with conditional:")
print(f"5 is {is_even(5)}")
print(f"6 is {is_even(6)}")

# lambda in list comprehension alternative
numbers = [1, 2, 3, 4, 5]
# list comprehension
squares1 = [x * x for x in numbers]
# lambda equivalent
squares2 = list(map(lambda x: x * x, numbers))
print("\nlist comprehension vs lambda:")
print(f"list comprehension: {squares1}")
print(f"lambda with map: {squares2}")

# lambda with custom sorting
words = ["apple", "banana", "cherry", "date"]
# sort by length, then alphabetically
sorted_words = sorted(words, 
                     key=lambda x: (len(x), x))
print("\ncustom sorting with lambda:")
print(f"original: {words}")
print(f"sorted: {sorted_words}")

# lambda in data transformation
data = [
    {"name": "alice", "age": 25},
    {"name": "bob", "age": 30},
    {"name": "charlie", "age": 35}
]

# transform to different format
transformed = list(map(
    lambda x: f"{x['name'].title()} is {x['age']} years old",
    data
))
print("\ndata transformation with lambda:")
for item in transformed:
    print(item)

# practice exercises:
# 1. create a program that:
#    - takes a list of strings
#    - uses lambda to filter strings by length
#    - uses lambda to transform strings
#    - combines multiple operations

# 2. create a program that:
#    - processes a list of numbers
#    - uses lambda for mathematical operations
#    - implements custom sorting logic
#    - uses reduce for aggregation

# 3. create a program that:
#    - handles a list of dictionaries
#    - filters based on multiple conditions
#    - transforms data structure
#    - sorts by multiple keys

# example solution for #1:
def process_strings(strings: List[str], min_length: int) -> List[str]:
    """
    process a list of strings using lambda functions.
    
    args:
        strings: list of strings to process
        min_length: minimum length for filtering
    
    returns:
        processed list of strings
    """
    return list(map(
        lambda s: s.title(),  # transform to title case
        filter(
            lambda s: len(s) >= min_length,  # filter by length
            strings
        )
    ))

# testing the solution
test_strings = ["cat", "dog", "elephant", "bird", "rhinoceros"]
processed = process_strings(test_strings, 4)
print("\nstring processing:")
print(f"original: {test_strings}")
print(f"processed (min length 4): {processed}")

# bonus: combining with reduce
longest_word = reduce(
    lambda x, y: x if len(x) > len(y) else y,
    test_strings
)
print(f"longest word: {longest_word}") 