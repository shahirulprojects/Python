# for loops are used to iterate over a sequence (list, tuple, string, etc.)
# they help us perform the same action for each item in a sequence

# basic for loop with a list
fruits = ["apple", "banana", "orange", "grape"]
for fruit in fruits:
    print(f"i like {fruit}s")

# looping through a string (character by character)
name = "Python"
print("\nspelling out Python:")
for letter in name:
    print(letter)

# using range() function
# range(stop) - starts from 0
print("\ncounting to 5:")
for i in range(6):  # goes from 0 to 5
    print(i)

# range(start, stop) - starts from start number
print("\ncounting from 1 to 5:")
for i in range(1, 6):  # goes from 1 to 5
    print(i)

# range(start, stop, step) - with step size
print("\neven numbers up to 10:")
for i in range(0, 11, 2):  # step of 2
    print(i)

# counting backwards
print("\ncounting backwards:")
for i in range(5, 0, -1):  # negative step
    print(i)

# using enumerate() to get both index and value
fruits = ["apple", "banana", "orange"]
print("\nfruit inventory:")
for index, fruit in enumerate(fruits):
    print(f"fruit #{index + 1}: {fruit}")

# nested for loops (loop inside a loop)
print("\nmultiplication table:")
for i in range(1, 4):  # outer loop
    for j in range(1, 4):  # inner loop
        print(f"{i} x {j} = {i * j}")
    print("-" * 15)  # separator between rows

# looping through a dictionary
student_scores = {
    "alice": 85,
    "bob": 92,
    "charlie": 78
}

# loop through keys
print("\nstudent names:")
for student in student_scores:
    print(student)

# loop through values
print("\nall scores:")
for score in student_scores.values():
    print(score)

# loop through both keys and values
print("\nstudent grades:")
for student, score in student_scores.items():
    print(f"{student}: {score}")

# using for loops with list comprehension
numbers = [1, 2, 3, 4, 5]
squares = [num * num for num in numbers]  # creates a new list with squares
print("\noriginal numbers:", numbers)
print("squared numbers:", squares)

# practice exercises:
# 1. create a program that:
#    - asks user for a number n
#    - prints the sum of all numbers from 1 to n
#    - prints the factorial of n (1 * 2 * 3 * ... * n)

# 2. create a program that prints this pattern:
# *
# **
# ***
# ****
# *****

# 3. create a program that:
#    - has a list of words
#    - prints each word and its length
#    - identifies the longest word

# example solution for #1:
n = int(input("\nenter a number: "))
sum_numbers = 0
factorial = 1

for i in range(1, n + 1):
    sum_numbers += i
    factorial *= i

print(f"sum of numbers from 1 to {n}: {sum_numbers}")
print(f"factorial of {n}: {factorial}") 