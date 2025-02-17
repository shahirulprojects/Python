# in python, we can get input from users and display output in various ways

# getting input from the user
# input() always returns a string
name = input("What is your name? ")  # the text in quotes is the prompt shown to the user
print("Hello,", name)

# converting input to different types
# since input() always returns a string, we need to convert it for numbers
age_string = input("How old are you? ")
age = int(age_string)  # converts string to integer
print("Next year, you will be:", age + 1)

# we can do the conversion directly
height = float(input("What is your height in meters? "))  # converts input directly to float
print("Your height in centimeters is:", height * 100)

# formatting output
# method 1: using comma in print (adds space automatically)
print("Name:", name, "Age:", age)

# method 2: using + for concatenation (need to convert numbers to strings)
print("Name: " + name + " Age: " + str(age))

# method 3: using format() method (most flexible)
print("Name: {} Age: {}".format(name, age))

# method 4: using f-strings (easiest to read, python 3.6+)
print(f"Name: {name} Age: {age}")

# formatting numbers
price = 19.99
print(f"The price is ${price:.2f}")  # shows 2 decimal places

# tabulation and new lines
print("Menu:")
print("\tCoffee\t\t$2.99")  # \t adds a tab
print("\tTea\t\t$1.99")
print("\tCookie\t\t$0.99")

# printing on the same line
print("Loading", end="")  # end="" prevents new line
print(".", end="")
print(".", end="")
print(".")  # this one will end with new line

# practice exercises:
# 1. ask the user for their favorite color and print it back in a sentence
# 2. ask the user for two numbers, multiply them, and print the result
# 3. create a simple calculator that:
#    - asks for two numbers
#    - prints their sum, difference, product, and quotient
#    - formats the output nicely using f-strings

# example solution for #1:
color = input("What is your favorite color? ")
print(f"Wow! {color} is a beautiful color!") 