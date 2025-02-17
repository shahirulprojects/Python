# common list patterns and best practices in python

# pattern 1: initializing lists
# bad way (repetitive)
numbers = [0, 0, 0, 0, 0]

# good way (using multiplication)
numbers = [0] * 5
print("initialized list:", numbers)

# pattern 2: creating a range of numbers
# bad way
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# good way
numbers = list(range(1, 11))
print("\nrange of numbers:", numbers)

# pattern 3: finding unique elements
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_numbers = list(set(numbers))  # convert to set and back to list
print("\noriginal numbers:", numbers)
print("unique numbers:", unique_numbers)

# pattern 4: counting elements
from collections import Counter
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
count = Counter(numbers)
print("\nelement counts:", count)
print("most common element:", count.most_common(1)[0])

# pattern 5: finding common elements between lists
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
common = list(set(list1) & set(list2))
print("\nlist1:", list1)
print("list2:", list2)
print("common elements:", common)

# pattern 6: removing duplicates while maintaining order
from dict.fromkeys import dict
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_ordered = list(dict.fromkeys(numbers))
print("\noriginal:", numbers)
print("unique ordered:", unique_ordered)

# pattern 7: grouping elements
from itertools import groupby
numbers = [1, 1, 2, 2, 2, 3, 4, 4, 5]
# group consecutive numbers
grouped = [(k, list(g)) for k, g in groupby(numbers)]
print("\ngrouped consecutive numbers:", grouped)

# pattern 8: chunking a list
def chunk_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
chunks = chunk_list(numbers, 3)
print("\noriginal list:", numbers)
print("chunked list:", chunks)

# pattern 9: finding index of all occurrences
def find_all_indexes(lst, value):
    return [i for i, x in enumerate(lst) if x == value]

numbers = [1, 2, 3, 2, 4, 2, 5]
indexes = find_all_indexes(numbers, 2)
print("\nlist:", numbers)
print("indexes of 2:", indexes)

# pattern 10: rotating a list
def rotate_list(lst, k):
    k = k % len(lst)  # handle k > len(lst)
    return lst[k:] + lst[:k]

numbers = [1, 2, 3, 4, 5]
rotated = rotate_list(numbers, 2)
print("\noriginal list:", numbers)
print("rotated by 2:", rotated)

# pattern 11: sliding window
def sliding_window(lst, window_size):
    return [lst[i:i+window_size] 
            for i in range(len(lst)-window_size+1)]

numbers = [1, 2, 3, 4, 5]
windows = sliding_window(numbers, 3)
print("\nlist:", numbers)
print("sliding windows of size 3:", windows)

# pattern 12: list flattening (for nested lists)
def flatten(lst):
    return [item for sublist in lst for item in sublist]

nested = [[1, 2], [3, 4], [5, 6]]
flattened = flatten(nested)
print("\nnested list:", nested)
print("flattened:", flattened)

# practice exercises:
# 1. create a function that:
#    - takes a list of numbers
#    - returns a list of running averages
#    - (each element is average of all previous elements)

# 2. create a function that:
#    - takes two sorted lists
#    - merges them into a single sorted list
#    - without using sort()

# 3. create a function that:
#    - takes a list of strings
#    - groups them by their first letter
#    - returns a dictionary of lists

# example solution for #1:
def running_average(numbers):
    averages = []
    total = 0
    for i, num in enumerate(numbers, 1):
        total += num
        averages.append(total / i)
    return averages

numbers = [2, 4, 6, 8, 10]
averages = running_average(numbers)
print("\nnumbers:", numbers)
print("running averages:", [f"{avg:.2f}" for avg in averages]) 