# variables are containers for storing data values
# python is dynamically typed, meaning you don't need to declare variable types

# creating variables (notice how we don't need to specify the type)
name = "Alex"  # this is a string (text)
age = 25      # this is an integer (whole number)
height = 1.75  # this is a float (decimal number)
is_student = True  # this is a boolean (True/False)

# printing variables
print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Is student?", is_student)

# you can change variable values at any time
age = 26
print("New age:", age)

# variable naming rules:
valid_name = "This is fine"
my_name_2 = "This is also fine"
_private = "This is fine too"

# invalid names (these would cause errors):
# 2name = "Can't start with number"
# my-name = "Can't use hyphens"
# my name = "Can't use spaces"

# python is case-sensitive
Name = "John"
name = "Jane"
print("Name:", Name)  # prints "John"
print("name:", name)  # prints "Jane"

# multiple assignments
x, y, z = 1, 2, 3
print("x:", x)
print("y:", y)
print("z:", z)

# checking variable type
print("Type of name:", type(name))
print("Type of age:", type(age))
print("Type of height:", type(height))
print("Type of is_student:", type(is_student))

# practice exercises:
# 1. create a variable for your favorite number
# 2. create a variable for your favorite color
# 3. print both variables with descriptive messages
# 4. try changing their values and print again

# example:
favorite_number = 7
favorite_color = "blue"
print("My favorite number is:", favorite_number)
print("My favorite color is:", favorite_color) 