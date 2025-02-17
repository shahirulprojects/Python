# python's philosophy and style guide
# this file introduces the core principles that make python special :)

# importing this will show python's philosophy
import this

# let's break down the key principles in beginner-friendly terms

# 1. code readability
# python emphasizes clean, readable code that's easy to understand
example_good = [num for num in range(5) if num % 2 == 0]  # clear list comprehension
example_bad = [n for n in range(5) if not n%2]  # harder to understand

# 2. explicit is better than implicit
def good_function(number, multiply_by=2):
    # explicitly shows what we're doing
    result = number * multiply_by
    return result

def bad_function(n, m=2):
    # too implicit, harder to understand
    return n*m

# 3. simple is better than complex
# simple way to get even numbers
def get_even_numbers_simple(numbers):
    # loops through numbers and keeps only even ones
    return [num for num in numbers if num % 2 == 0]

# overly complex way to do the same thing
def get_even_numbers_complex(numbers):
    # unnecessarily complicated
    result = []
    for i in range(len(numbers)):
        current = numbers[i]
        if (current // 2) * 2 == current:
            result.append(current)
    return result

# 4. flat is better than nested
# good: flat structure
def process_user_input_flat(user_input):
    if not user_input:
        return "no input provided"
    if not user_input.isdigit():
        return "input must be a number"
    return int(user_input)

# bad: deeply nested structure
def process_user_input_nested(user_input):
    if user_input:
        if user_input.isdigit():
            return int(user_input)
        else:
            return "input must be a number"
    else:
        return "no input provided"

# 5. spacing and indentation matter
# python uses indentation to define blocks of code
def good_spacing():
    # standard 4-space indentation
    for i in range(3):
        # clear visual hierarchy
        print(i)
        if i == 1:
            print("found one")

# practical examples of python style
def calculate_average(numbers):
    """
    calculates the average of a list of numbers
    
    args:
        numbers (list): list of numbers to average
    
    returns:
        float: the average value
    """
    # guard clause for empty list
    if not numbers:
        return 0
    
    # calculate sum and length in separate steps for clarity
    total = sum(numbers)
    count = len(numbers)
    
    # explicit return with clear variable names
    return total / count

# example usage with good naming conventions
student_scores = [85, 92, 78, 90, 88]
average_score = calculate_average(student_scores)

# good variable naming
first_name = "john"  # clear and descriptive
x = "john"          # too vague

# using type hints (python 3.5+) for better code documentation
def greet(name: str, times: int = 1) -> str:
    """
    creates a greeting message
    
    args:
        name: the person's name
        times: number of times to repeat the greeting
    
    returns:
        formatted greeting string
    """
    return f"hello, {name}! " * times 