# conditional statements let us make decisions in our code
# they help our program take different actions based on conditions

# basic if statement
age = 18

if age >= 18:
    print("you are an adult")  # this code runs only if the condition is true
    print("you can vote")  # notice the indentation - it's important!

# if-else statement
temperature = 15

if temperature > 20:
    print("it's a warm day")
else:
    print("it's a cool day")  # this runs if temperature <= 20

# if-elif-else chain (multiple conditions)
score = 85

if score >= 90:
    print("grade: A")
elif score >= 80:
    print("grade: B")
elif score >= 70:
    print("grade: C")
elif score >= 60:
    print("grade: D")
else:
    print("grade: F")  # this runs if none of the above conditions are true

# comparison operators
x = 5
y = 10

print("\nComparison Examples:")
print(f"{x} > {y}:", x > y)   # greater than
print(f"{x} < {y}:", x < y)   # less than
print(f"{x} >= {y}:", x >= y) # greater than or equal to
print(f"{x} <= {y}:", x <= y) # less than or equal to
print(f"{x} == {y}:", x == y) # equal to
print(f"{x} != {y}:", x != y) # not equal to

# multiple conditions using and, or, not
age = 25
has_license = True

# using and (both conditions must be true)
if age >= 18 and has_license:
    print("\nyou can drive a car")

# using or (at least one condition must be true)
if age < 13 or age > 65:
    print("you get a discount")

# using not (inverts a condition)
if not has_license:
    print("you need to get a license")

# checking if a value is in a range
temperature = 25
if 20 <= temperature <= 30:
    print("\ntemperature is comfortable")

# checking if a value is in a collection
favorite_colors = ["blue", "green", "purple"]
if "blue" in favorite_colors:
    print("blue is one of your favorite colors")

# truthy and falsy values
# these values are considered false:
# - False
# - None
# - 0
# - empty sequences ([], "", (), {})
# everything else is considered true

# examples
empty_list = []
if empty_list:
    print("list has items")
else:
    print("\nlist is empty")

name = "Alice"
if name:
    print("name is not empty")

# practice exercises:
# 1. write a program that:
#    - asks for user's age
#    - prints "child" if age < 13
#    - prints "teenager" if age is between 13 and 19
#    - prints "adult" if age >= 20

# 2. create a simple password checker that:
#    - has a stored password
#    - asks user for password
#    - prints "access granted" if correct
#    - prints "access denied" if incorrect

# 3. write a program that checks if a number is:
#    - positive or negative
#    - even or odd
#    - divisible by 5

# example solution for #1:
age = int(input("\nWhat is your age? "))
if age < 13:
    print("you are a child")
elif age <= 19:
    print("you are a teenager")
else:
    print("you are an adult") 