# sets are unordered collections of unique elements
# they're mutable but can only contain immutable elements

# creating sets
empty_set = set()  # empty set (can't use {} as that creates empty dict)
numbers = {1, 2, 3, 4, 5}  # set of numbers
fruits = {"apple", "banana", "orange"}  # set of strings
mixed = {1, "hello", (1, 2)}  # set with different types

# sets automatically remove duplicates
numbers_with_duplicates = {1, 2, 2, 3, 3, 3, 4, 4, 4, 4}
print("original with duplicates:", numbers_with_duplicates)

# creating set from list
numbers_list = [1, 2, 2, 3, 3, 3]
unique_numbers = set(numbers_list)
print("unique numbers from list:", unique_numbers)

# adding elements to a set
fruits = {"apple", "banana"}
print("\noriginal fruits:", fruits)

fruits.add("orange")  # add single element
print("after adding orange:", fruits)

fruits.update(["mango", "grape"])  # add multiple elements
print("after update:", fruits)

# removing elements
fruits.remove("banana")  # raises error if not found
print("\nafter removing banana:", fruits)

fruits.discard("kiwi")  # no error if not found
print("after discarding kiwi:", fruits)

popped = fruits.pop()  # remove and return arbitrary element
print("popped item:", popped)
print("after pop:", fruits)

fruits.clear()  # remove all elements
print("after clear:", fruits)

# set operations
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

# union (all elements from both sets)
union = a | b  # or a.union(b)
print("\nunion:", union)

# intersection (elements common to both sets)
intersection = a & b  # or a.intersection(b)
print("intersection:", intersection)

# difference (elements in a but not in b)
difference = a - b  # or a.difference(b)
print("difference (a-b):", difference)

# symmetric difference (elements in either set but not both)
symmetric_difference = a ^ b  # or a.symmetric_difference(b)
print("symmetric difference:", symmetric_difference)

# set comparisons
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}
c = {1, 2, 3}

# subset (all elements of a are in b)
print("\nsubset checks:")
print("a is subset of b:", a <= b)  # or a.issubset(b)
print("a is subset of c:", a <= c)

# proper subset (all elements of a are in b, and b has more)
print("\nproper subset checks:")
print("a is proper subset of b:", a < b)
print("a is proper subset of c:", a < c)

# superset (all elements of b are in a)
print("\nsuperset checks:")
print("b is superset of a:", b >= a)  # or b.issuperset(a)

# set comprehension
numbers = {x for x in range(10) if x % 2 == 0}
print("\neven numbers using set comprehension:", numbers)

# frozen sets (immutable sets)
frozen = frozenset([1, 2, 3])
print("\nfrozen set:", frozen)
# frozen.add(4)  # this would raise an error

# practical examples
# finding unique characters in string
text = "hello world"
unique_chars = set(text)
print("\nunique characters in '{}':".format(text), unique_chars)

# finding common characters in strings
text1 = "hello"
text2 = "world"
common_chars = set(text1) & set(text2)
print("common characters in '{}' and '{}':".format(text1, text2), common_chars)

# practice exercises:
# 1. create a program that:
#    - takes two strings
#    - finds characters that appear in both strings
#    - finds characters unique to each string
#    - prints the results

# 2. create a program that:
#    - has a list of students in different classes
#    - finds students who take all classes
#    - finds students who take at least one class
#    - finds students who take only specific classes

# 3. create a spell checker that:
#    - has a set of known words
#    - takes a text
#    - identifies words not in the dictionary
#    - suggests similar words (bonus)

# example solution for #1:
def analyze_strings(str1, str2):
    set1 = set(str1.lower())
    set2 = set(str2.lower())
    
    common = set1 & set2
    unique_to_first = set1 - set2
    unique_to_second = set2 - set1
    
    print(f"\nAnalyzing '{str1}' and '{str2}':")
    print("Common characters:", common)
    print(f"Characters unique to '{str1}':", unique_to_first)
    print(f"Characters unique to '{str2}':", unique_to_second)

analyze_strings("Python", "JavaScript") 