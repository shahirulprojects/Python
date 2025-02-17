# advanced string formatting in python

# string formatting with different data types
name = "Alice"
age = 25
height = 1.75
is_student = True

# formatting with different data types using f-strings
print(f"""
Personal Info:
-------------
Name: {name}
Age: {age}
Height: {height:.2f}m
Student: {is_student}
""")

# number formatting
number = 1234.5678

# controlling decimal places
print(f"Default: {number}")
print(f"2 decimal places: {number:.2f}")
print(f"3 decimal places: {number:.3f}")

# adding thousand separators
large_number = 1234567
print(f"With separators: {large_number:,}")
print(f"With separators and decimals: {number:,.2f}")

# padding and alignment
# left alignment with width 10
print(f"|{name:<10}|")  # left align
print(f"|{name:>10}|")  # right align
print(f"|{name:^10}|")  # center align

# padding with different characters
print(f"|{name:-<10}|")  # pad with -
print(f"|{name:*>10}|")  # pad with *
print(f"|{name:#^10}|")  # pad with #

# formatting percentages
score = 0.8756
print(f"Score: {score:.1%}")  # shows as percentage with 1 decimal place

# scientific notation
scientific_number = 12345.6789
print(f"Scientific notation: {scientific_number:e}")
print(f"Scientific notation (3 decimals): {scientific_number:.3e}")

# binary, octal, and hexadecimal
number = 42
print(f"""
Number Systems:
--------------
Decimal: {number:d}
Binary: {number:b}
Octal: {number:o}
Hexadecimal: {number:x}
Hexadecimal (uppercase): {number:X}
""")

# practice exercises:
# 1. create a table-like output for a store inventory with:
#    - product name (left-aligned)
#    - quantity (right-aligned)
#    - price (right-aligned with 2 decimal places)
# 2. format a large number (e.g., 1234567.89) in different ways:
#    - with thousand separators
#    - in scientific notation
#    - as a percentage
# 3. create a progress bar using string formatting
#    example: [====    ] 50%

# example solution for #1:
print("\nStore Inventory:")
print("-" * 30)
print(f"{'Product':<15}{'Quantity':>7}{'Price':>8}")
print("-" * 30)
print(f"{'Coffee':<15}{42:>7}{2.99:>8.2f}")
print(f"{'Tea':<15}{28:>7}{1.99:>8.2f}")
print(f"{'Cookies':<15}{63:>7}{0.99:>8.2f}")