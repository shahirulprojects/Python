# advanced loop patterns and itertools module
from itertools import (count, cycle, repeat, chain, 
                      combinations, permutations, product,
                      islice, takewhile, dropwhile)

# infinite iterators
# count: counts indefinitely from a starting number
counter = count(1)  # starts from 1
print("count example:")
for i in islice(counter, 5):  # take first 5 items
    print(i, end=" ")
print()

# cycle: cycles through an iterator indefinitely
colors = cycle(['red', 'green', 'blue'])
print("\ncycle example:")
for i in range(6):  # print first 6 items
    print(next(colors), end=" ")
print()

# repeat: repeats an object indefinitely or n times
repeater = repeat("hello", 3)
print("\nrepeat example:", list(repeater))

# combining iterators
# chain: combines multiple iterators
numbers = [1, 2, 3]
letters = ['a', 'b', 'c']
combined = chain(numbers, letters)
print("\nchain example:", list(combined))

# islice: slices an iterator
counter = count(1)
print("\nislice example:")
print("First 5 numbers:", list(islice(counter, 5)))
print("Numbers 5-10:", list(islice(count(1), 5, 11)))

# combinations and permutations
items = [1, 2, 3]
print("\ncombinations and permutations:")
print("combinations(2):", list(combinations(items, 2)))
print("permutations(2):", list(permutations(items, 2)))
print("cartesian product:", list(product(items, repeat=2)))

# filtering iterators
numbers = count(1)
print("\nfiltering iterators:")
# takewhile: take items while condition is true
even_numbers = takewhile(lambda x: x <= 5, numbers)
print("takewhile <= 5:", list(even_numbers))

numbers = count(1)
# dropwhile: drop items while condition is true
odd_numbers = dropwhile(lambda x: x < 5, numbers)
print("dropwhile < 5:", list(islice(odd_numbers, 5)))

# advanced enumerate
items = ['a', 'b', 'c']
print("\nadvanced enumerate:")
# start enumeration from specific number
for i, item in enumerate(items, start=1):
    print(f"Item {i}: {item}")

# zip with multiple iterables
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
cities = ['New York', 'London', 'Paris']
print("\nzip with multiple iterables:")
for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} years old and lives in {city}")

# zip_longest (includes all items, fills missing with None or fillvalue)
from itertools import zip_longest
list1 = [1, 2, 3]
list2 = ['a', 'b']
print("\nzip_longest example:")
print(list(zip_longest(list1, list2, fillvalue='*')))

# grouping elements
from itertools import groupby

# sort data first (groupby assumes sorted data)
data = sorted([1, 1, 1, 2, 2, 3, 4, 4, 4, 4])
print("\ngroupby example:")
for key, group in groupby(data):
    print(f"Number {key} appears {len(list(group))} times")

# nested loops with control
print("\nnested loop control:")
def find_number(matrix, target):
    for i, row in enumerate(matrix):
        for j, num in enumerate(row):
            if num == target:
                return f"Found at position ({i}, {j})"
    return "Not found"

matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]
print(find_number(matrix, 5))
print(find_number(matrix, 10))

# loop with else
print("\nloop with else:")
def find_prime(numbers):
    for num in numbers:
        if num < 2:
            continue
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                break
        else:  # executed if no break occurred
            return f"Found prime: {num}"
    else:  # executed if no return occurred
        return "No primes found"

print(find_prime([4, 6, 8, 9, 11]))
print(find_prime([4, 6, 8, 9]))

# practice exercises:
# 1. create a function that:
#    - generates all possible combinations of letters
#    - takes length as parameter
#    - filters out invalid combinations
#    - uses itertools efficiently

# 2. create a program that:
#    - processes a log file
#    - groups entries by date
#    - counts occurrences of each type
#    - uses groupby and counter

# 3. create a function that:
#    - implements a sliding window
#    - calculates moving average
#    - handles different window sizes
#    - uses deque and itertools

# example solution for #3:
from collections import deque

def moving_average(numbers, window_size):
    window = deque(maxlen=window_size)
    averages = []
    
    for num in numbers:
        window.append(num)
        if len(window) == window_size:
            averages.append(sum(window) / window_size)
    
    return averages

numbers = [1, 2, 3, 4, 5, 6, 7]
print("\nmoving averages (window=3):", 
      [f"{x:.2f}" for x in moving_average(numbers, 3)]) 