# lists are ordered collections of items in python
# they can store different types of data and can be modified

# creating lists
empty_list = []  # empty list
numbers = [1, 2, 3, 4, 5]  # list of numbers
fruits = ["apple", "banana", "orange"]  # list of strings
mixed = [1, "hello", 3.14, True]  # list with different types

# accessing list elements (indexing)
# remember: python uses 0-based indexing
first_fruit = fruits[0]  # gets first item
last_fruit = fruits[-1]  # gets last item
print("fruits:", fruits)
print("first fruit:", first_fruit)
print("last fruit:", last_fruit)

# modifying lists
fruits[1] = "grape"  # changing an element
print("\nafter modification:", fruits)

# list methods
# adding elements
fruits.append("mango")  # adds to end
print("\nafter append:", fruits)

fruits.insert(1, "banana")  # insert at specific position
print("after insert:", fruits)

# removing elements
fruits.remove("grape")  # removes first occurrence of value
print("\nafter remove:", fruits)

popped_fruit = fruits.pop()  # removes and returns last item
print("popped fruit:", popped_fruit)
print("after pop:", fruits)

popped_index = fruits.pop(1)  # pop from specific index
print("popped from index 1:", popped_index)
print("after pop index:", fruits)

# list operations
numbers = [1, 2, 3]
more_numbers = [4, 5, 6]

# concatenation
combined = numbers + more_numbers
print("\ncombined lists:", combined)

# repetition
repeated = numbers * 2
print("repeated list:", repeated)

# list methods for ordering
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
print("\noriginal numbers:", numbers)

numbers.sort()  # sorts in place
print("sorted numbers:", numbers)

numbers.reverse()  # reverses in place
print("reversed numbers:", numbers)

# creating a new sorted list (original unchanged)
original = [3, 1, 4, 1, 5]
sorted_numbers = sorted(original)
print("\noriginal:", original)
print("new sorted:", sorted_numbers)

# list slicing [start:end:step]
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print("\noriginal:", numbers)
print("first three:", numbers[:3])  # from start to index 3 (exclusive)
print("last three:", numbers[-3:])  # last three items
print("middle:", numbers[3:7])  # from index 3 to 7 (exclusive)
print("every second:", numbers[::2])  # every second item
print("reversed:", numbers[::-1])  # reverse the list

# useful list operations
numbers = [1, 2, 3, 2, 4, 2, 5]
print("\nnumber list:", numbers)
print("length:", len(numbers))  # number of items
print("count of 2:", numbers.count(2))  # count occurrences
print("index of 4:", numbers.index(4))  # find position of 4

# checking membership
print("\nis 3 in numbers?", 3 in numbers)
print("is 6 in numbers?", 6 in numbers)

# list comprehension (creating lists based on existing ones)
numbers = [1, 2, 3, 4, 5]
squares = [num * num for num in numbers]
even_numbers = [num for num in numbers if num % 2 == 0]

print("\noriginal numbers:", numbers)
print("squares:", squares)
print("even numbers:", even_numbers)

# practice exercises:
# 1. create a program that:
#    - asks user for 5 numbers
#    - stores them in a list
#    - prints the sum, average, minimum, and maximum

# 2. create a program that:
#    - has a list of words
#    - creates a new list with only words longer than 4 letters
#    - prints both lists

# 3. create a shopping list program that:
#    - starts with an empty list
#    - allows user to add items
#    - allows user to remove items
#    - allows user to view the list
#    - sorts the list alphabetically

# example solution for #1:
numbers = []
print("\nenter 5 numbers:")
for i in range(5):
    num = float(input(f"number {i+1}: "))
    numbers.append(num)

print("\nstatistics:")
print(f"numbers: {numbers}")
print(f"sum: {sum(numbers)}")
print(f"average: {sum(numbers)/len(numbers)}")
print(f"minimum: {min(numbers)}")
print(f"maximum: {max(numbers)}") 