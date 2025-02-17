# dictionaries are key-value pairs in python
# they're unordered and mutable

# creating dictionaries
empty_dict = {}  # empty dictionary
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}
numbers = {1: "one", 2: "two", 3: "three"}
mixed = {
    "string": "hello",
    1: 42,
    (1, 2): "tuple key"  # tuples can be keys
}

# accessing dictionary values
print("person:", person)
print("name:", person["name"])
print("age:", person["age"])

# using get() method (safer - returns None or default if key not found)
print("\nusing get():")
print("city:", person.get("city"))
print("country:", person.get("country"))  # returns None
print("country:", person.get("country", "unknown"))  # returns default value

# modifying dictionaries
person["age"] = 26  # change existing value
person["country"] = "USA"  # add new key-value pair
print("\nupdated person:", person)

# dictionary methods
# keys, values, and items
print("\ndictionary components:")
print("keys:", list(person.keys()))
print("values:", list(person.values()))
print("items:", list(person.items()))

# checking if key exists
print("\nkey checks:")
print("has name?", "name" in person)
print("has address?", "address" in person)

# removing items
removed_age = person.pop("age")  # remove and return value
print("\nremoved age:", removed_age)
print("person after pop:", person)

# remove last inserted item (python 3.7+)
last_item = person.popitem()
print("removed last item:", last_item)
print("person after popitem:", person)

# clearing dictionary
person.clear()
print("after clear:", person)

# merging dictionaries
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# using update method
dict1.update(dict2)
print("\nmerged using update:", dict1)

# using | operator (python 3.9+)
dict3 = {"a": 1, "b": 2}
dict4 = {"c": 3, "d": 4}
merged = dict3 | dict4
print("merged using |:", merged)

# dictionary comprehension
numbers = {x: x**2 for x in range(5)}
print("\ndictionary comprehension:", numbers)

# nested dictionaries
users = {
    "alice": {
        "age": 25,
        "email": "alice@example.com"
    },
    "bob": {
        "age": 30,
        "email": "bob@example.com"
    }
}

print("\nnested dictionary:")
print("alice's email:", users["alice"]["email"])

# common patterns
# setting default value if key doesn't exist
counts = {}
words = ["apple", "banana", "apple", "cherry", "date", "banana"]

for word in words:
    counts[word] = counts.get(word, 0) + 1

print("\nword counts:", counts)

# using setdefault
inventory = {}
inventory.setdefault("apples", 0)  # sets only if key doesn't exist
inventory["apples"] += 1
print("\ninventory:", inventory)

# using defaultdict
from collections import defaultdict
default_counts = defaultdict(int)  # default value of 0 for new keys

for word in words:
    default_counts[word] += 1

print("counts using defaultdict:", dict(default_counts))

# practice exercises:
# 1. create a program that:
#    - reads a text
#    - counts the frequency of each character
#    - prints the characters sorted by frequency

# 2. create a simple phone book that:
#    - allows adding names and numbers
#    - allows looking up numbers by name
#    - allows deleting entries
#    - allows updating numbers

# 3. create a nested dictionary that:
#    - represents a small library
#    - has books organized by genre
#    - each book has title, author, year
#    - implement functions to add/remove books
#    - implement search by title/author

# example solution for #1:
text = "hello world"
char_frequency = {}

for char in text.lower():
    if char.isalnum():  # count only alphanumeric characters
        char_frequency[char] = char_frequency.get(char, 0) + 1

# sort by frequency
sorted_chars = sorted(char_frequency.items(), 
                     key=lambda x: x[1], 
                     reverse=True)

print("\ncharacter frequency:")
for char, freq in sorted_chars:
    print(f"'{char}': {freq}") 