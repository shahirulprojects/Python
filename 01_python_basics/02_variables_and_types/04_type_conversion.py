# type conversion in python
# this file explains how to convert between different data types safely

# 1. basic type conversion
# converting strings to numbers
text_number = "42"
integer_number = int(text_number)    # converts to integer: 42
float_number = float(text_number)    # converts to float: 42.0

# converting numbers to strings
age = 25
age_text = str(age)    # converts to string: "25"

# 2. handling potential conversion errors
def safe_string_to_number(text):
    # tries to convert a string to a number safely
    try:
        return float(text)
    except ValueError:
        # returns None if conversion fails
        return None

# examples of safe conversion
valid_number = safe_string_to_number("123.45")    # returns 123.45
invalid_number = safe_string_to_number("hello")    # returns None

# 3. common type conversions
# boolean conversions
empty_string = bool("")        # false
non_empty_string = bool("hi")  # true
zero_number = bool(0)          # false
non_zero_number = bool(42)     # true

# list conversions
# converting string to list of characters
name = "python"
char_list = list(name)    # ['p', 'y', 't', 'h', 'o', 'n']

# converting string to list of words
sentence = "hello world python"
word_list = sentence.split()    # ['hello', 'world', 'python']

# 4. practical examples

def process_user_age():
    # gets user age and converts it safely
    age_input = input("what's your age? ")
    
    # try to convert to integer
    try:
        age = int(age_input)
        if age < 0 or age > 150:
            return "please enter a realistic age"
        return f"you are {age} years old"
    except ValueError:
        return "please enter a valid number"

def calculate_total_cost(prices):
    """
    converts a list of price strings to numbers and calculates total
    
    args:
        prices (list): list of string prices (e.g., ['10.99', '24.50'])
    
    returns:
        float: total cost, or None if any conversion fails
    """
    try:
        # converts each price to float and sums them
        return sum(float(price) for price in prices)
    except ValueError:
        return None

# example usage
price_list = ['10.99', '24.50', '5.99']
total = calculate_total_cost(price_list)    # returns 41.48

# 5. type checking
def show_type_info(value):
    # demonstrates different ways to check types
    print(f"value: {value}")
    print(f"type: {type(value)}")
    print(f"is string? {isinstance(value, str)}")
    print(f"is number? {isinstance(value, (int, float))}")

# examples
show_type_info("hello")    # string
show_type_info(42)         # integer
show_type_info(3.14)       # float

# 6. converting between collections
# list to tuple conversion
numbers_list = [1, 2, 3]
numbers_tuple = tuple(numbers_list)    # (1, 2, 3)

# list to set (removes duplicates)
numbers_with_duplicates = [1, 2, 2, 3, 3, 3]
unique_numbers = set(numbers_with_duplicates)    # {1, 2, 3}

# set back to list
unique_list = list(unique_numbers)    # [1, 2, 3]

# 7. advanced conversions
# binary string to integer
binary_string = "1010"
decimal_number = int(binary_string, 2)    # 10

# hexadecimal string to integer
hex_string = "1A"
hex_number = int(hex_string, 16)    # 26

# number to binary string
number = 10
binary = bin(number)[2:]    # "1010"

# number to hexadecimal string
hex_value = hex(number)[2:]    # "a" 