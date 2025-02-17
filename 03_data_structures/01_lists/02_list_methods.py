# advanced list methods and operations in python

# copying lists
# simple assignment creates a reference
original = [1, 2, 3]
reference = original  # both variables point to the same list
reference[0] = 10
print("original:", original)  # original is also modified
print("reference:", reference)

# shallow copy
original = [1, 2, 3]
shallow_copy = original.copy()  # or list(original) or original[:]
shallow_copy[0] = 10
print("\nafter shallow copy:")
print("original:", original)  # original unchanged
print("shallow copy:", shallow_copy)

# deep copy (for nested lists)
from copy import deepcopy
nested = [[1, 2], [3, 4]]
deep_copy = deepcopy(nested)
deep_copy[0][0] = 10
print("\nafter deep copy:")
print("original nested:", nested)
print("deep copy:", deep_copy)

# list methods for adding elements
numbers = [1, 2, 3]
print("\noriginal numbers:", numbers)

# extend - add multiple elements from another list
numbers.extend([4, 5])
print("after extend:", numbers)

# insert - add element at specific position
numbers.insert(2, 10)  # insert 10 at index 2
print("after insert:", numbers)

# removing elements
# remove - removes first occurrence of value
numbers = [1, 2, 3, 2, 4, 2, 5]
print("\noriginal:", numbers)
numbers.remove(2)  # removes first 2
print("after remove(2):", numbers)

# clear - removes all elements
numbers.clear()
print("after clear:", numbers)

# advanced list operations
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# list comprehension with conditions
evens = [x for x in numbers if x % 2 == 0]
odds = [x for x in numbers if x % 2 != 0]
print("\neven numbers:", evens)
print("odd numbers:", odds)

# nested list comprehension
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

# flatten matrix using list comprehension
flattened = [num for row in matrix for num in row]
print("\noriginal matrix:", matrix)
print("flattened matrix:", flattened)

# transpose matrix using nested list comprehension
transposed = [[row[i] for row in matrix] for i in range(3)]
print("transposed matrix:", transposed)

# filtering and mapping combined
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# get squares of even numbers
even_squares = [x**2 for x in numbers if x % 2 == 0]
print("\neven squares:", even_squares)

# using map and filter (functional programming)
# same as above but using map and filter
even_squares_func = list(map(lambda x: x**2, 
                           filter(lambda x: x % 2 == 0, numbers)))
print("even squares (functional):", even_squares_func)

# list operations with strings
words = ["hello", "world", "python"]
# capitalize all words
capitalized = [word.capitalize() for word in words]
print("\noriginal words:", words)
print("capitalized words:", capitalized)

# join list elements into string
sentence = " ".join(capitalized)
print("joined into sentence:", sentence)

# split string into list
new_words = sentence.split()
print("split back to list:", new_words)

# practice exercises:
# 1. create a program that:
#    - has a list of temperatures in Celsius
#    - converts them to Fahrenheit using list comprehension
#    - prints both lists side by side

# 2. create a program that:
#    - has a list of words
#    - creates a new list with palindromes only
#    - (word reads same forwards and backwards)
#    - prints both lists

# 3. create a program that:
#    - has a 3x3 matrix (nested list)
#    - calculates the sum of each row
#    - calculates the sum of each column
#    - calculates the diagonal sums

# example solution for #1:
celsius = [0, 10, 20, 30, 40]
fahrenheit = [(c * 9/5) + 32 for c in celsius]

print("\ntemperature conversion:")
for c, f in zip(celsius, fahrenheit):
    print(f"{c}°C = {f:.1f}°F") 