# strings in python are immutable sequences of characters
# they support a wide variety of methods and formatting options

# string creation
single_quotes = 'hello'
double_quotes = "hello"
triple_quotes = '''this is a
multi-line string'''
raw_string = r'C:\Users\name'  # raw string (ignores escapes)

# basic string operations
text = "Hello, World!"
print("original:", text)
print("length:", len(text))
print("uppercase:", text.upper())
print("lowercase:", text.lower())
print("title case:", text.title())
print("swapped case:", text.swapcase())

# string methods for checking content
print("\nchecking content:")
print("starts with 'Hello':", text.startswith("Hello"))
print("ends with 'World':", text.endswith("World"))
print("is alphabetic:", "Hello123".isalpha())
print("is alphanumeric:", "Hello123".isalnum())
print("is numeric:", "123".isnumeric())
print("is space:", "   ".isspace())

# finding and counting
text = "hello hello world"
print("\nfinding and counting:")
print("count of 'hello':", text.count("hello"))
print("position of 'world':", text.find("world"))  # returns -1 if not found
print("position of 'hello' (rfind):", text.rfind("hello"))  # searches from right
try:
    print("position of 'python':", text.index("python"))  # raises ValueError if not found
except ValueError as e:
    print("'python' not found (index raised ValueError)")

# splitting and joining
text = "apple,banana,orange"
words = text.split(",")
print("\nsplitting and joining:")
print("split result:", words)
print("joined with space:", " ".join(words))
print("split lines:", "line1\nline2\nline3".splitlines())

# stripping whitespace
text = "   hello world   "
print("\nstripping whitespace:")
print("original:", f"'{text}'")
print("left strip:", f"'{text.lstrip()}'")
print("right strip:", f"'{text.rstrip()}'")
print("both sides:", f"'{text.strip()}'")

# replacing text
text = "hello world world"
print("\nreplacing:")
print("replace 'world':", text.replace("world", "python"))
print("replace first 'world':", text.replace("world", "python", 1))

# string formatting methods
name = "Alice"
age = 25

# method 1: % operator (old style)
print("\nold style formatting:")
print("Hello, %s! You are %d years old." % (name, age))

# method 2: str.format()
print("\nstr.format() method:")
print("Hello, {}! You are {} years old.".format(name, age))
print("Hello, {1}! You are {0} years old.".format(age, name))  # positional
print("Hello, {n}! You are {a} years old.".format(n=name, a=age))  # named

# method 3: f-strings (python 3.6+)
print("\nf-strings:")
print(f"Hello, {name}! You are {age} years old.")
print(f"Hello, {name.upper()}! You are {age * 2} years old.")

# advanced string formatting
number = 42.12345
print("\nadvanced formatting:")
print(f"Number with 2 decimals: {number:.2f}")
print(f"Number with padding: {number:10.2f}")
print(f"Percentage: {0.15:.1%}")
print(f"Binary: {42:b}")
print(f"Hexadecimal: {42:x}")
print(f"With separators: {1000000:,}")

# alignment and padding
text = "python"
width = 10
print("\nalignment:")
print(f"Left aligned:   '{text:<{width}}'")
print(f"Right aligned:  '{text:>{width}}'")
print(f"Center aligned: '{text:^{width}}'")
print(f"Padded with *:  '{text:*^{width}}'")

# string methods for validation and cleaning
text = "   Hello,    World!   "
print("\ncleaning text:")
print("original:", text)
print("normalized:", " ".join(text.split()))  # removes extra spaces

# case conversion
text = "Python Programming"
print("\ncase conversion:")
print("capitalize:", text.capitalize())  # first char upper, rest lower
print("title:", text.title())  # each word capitalized
print("upper:", text.upper())  # all upper
print("lower:", text.lower())  # all lower

# practice exercises:
# 1. create a function that:
#    - takes a string
#    - removes all punctuation
#    - converts to lowercase
#    - splits into words
#    - returns list of unique words

# 2. create a program that:
#    - formats a table of data
#    - aligns columns properly
#    - adds borders
#    - handles different data types

# 3. create a function that:
#    - validates a password string
#    - checks length
#    - requires numbers and special characters
#    - requires mixed case
#    - returns True/False and reason if invalid

# example solution for #1:
import string

def process_text(text):
    # remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    
    # convert to lowercase and split
    words = text.lower().split()
    
    # return unique words
    return sorted(set(words))

sample_text = "Hello, World! Hello, Python! Python is great."
unique_words = process_text(sample_text)
print("\nUnique words:", unique_words) 