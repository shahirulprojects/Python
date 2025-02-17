# comparison and logical operations in python
# this file covers how to compare values and combine logical conditions

# 1. comparison operators
# these operators compare values and return True or False

# equality comparison
x = 5
y = 10

is_equal = x == y          # false
is_not_equal = x != y      # true
is_greater = x > y         # false
is_less = x < y            # true
is_greater_equal = x >= y  # false
is_less_equal = x <= y     # true

# 2. comparing different types
# comparing numbers
integer_num = 42
float_num = 42.0
are_equal = integer_num == float_num  # true

# comparing strings (case-sensitive)
text1 = "hello"
text2 = "Hello"
strings_equal = text1 == text2  # false (case matters)
strings_equal_ignore_case = text1.lower() == text2.lower()  # true

# 3. logical operators
# and: both conditions must be true
is_adult = age >= 18
has_id = True
can_buy_alcohol = is_adult and has_id

# or: at least one condition must be true
is_weekend = True
is_holiday = False
can_sleep_in = is_weekend or is_holiday

# not: inverts a boolean value
is_working = True
is_free = not is_working

# 4. combining logical operations
def check_password(password):
    """
    checks if a password meets security requirements
    
    args:
        password (str): password to check
    
    returns:
        bool: true if password is valid
    """
    # multiple conditions combined
    has_minimum_length = len(password) >= 8
    has_uppercase = any(char.isupper() for char in password)
    has_number = any(char.isdigit() for char in password)
    
    # all conditions must be true
    return has_minimum_length and has_uppercase and has_number

# example usage
strong_password = "Python123"
weak_password = "password"
print(check_password(strong_password))  # true
print(check_password(weak_password))    # false

# 5. practical examples

def check_temperature(temp):
    """
    determines comfort level based on temperature
    
    args:
        temp (float): temperature in celsius
    
    returns:
        str: comfort level description
    """
    if temp < 0:
        return "freezing"
    elif temp < 10:
        return "very cold"
    elif temp < 20:
        return "cool"
    elif temp < 25:
        return "comfortable"
    elif temp < 30:
        return "warm"
    else:
        return "hot"

# example temperature checks
print(check_temperature(22))  # comfortable
print(check_temperature(35))  # hot

def is_valid_username(username):
    """
    checks if username meets requirements
    
    args:
        username (str): username to validate
    
    returns:
        bool: true if username is valid
    """
    # multiple conditions with and
    correct_length = 3 <= len(username) <= 20
    starts_with_letter = username[0].isalpha() if username else False
    only_valid_chars = username.replace('_', '').isalnum()
    
    return correct_length and starts_with_letter and only_valid_chars

# example username validation
print(is_valid_username("python_dev"))   # true
print(is_valid_username("123user"))      # false
print(is_valid_username("a"))            # false

# 6. short-circuit evaluation
# python uses short-circuit evaluation for logical operators
# this means it stops evaluating as soon as the result is known

def is_valid_index(lst, index):
    """
    safely checks if an index is valid for a list
    
    args:
        lst (list): list to check
        index (int): index to validate
    
    returns:
        bool: true if index is valid
    """
    # checks if list exists and index is in range
    # the second condition is only checked if the first is true
    return lst is not None and 0 <= index < len(lst)

# example usage
numbers = [1, 2, 3]
print(is_valid_index(numbers, 1))    # true
print(is_valid_index(None, 1))       # false (stops at first condition)

# 7. comparing objects
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        # defines how == works for Point objects
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

# example point comparison
p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

print(p1 == p2)  # true (same coordinates)
print(p1 == p3)  # false (different coordinates) 