# advanced dictionary concepts and specialized dictionary types

# ordered dictionaries (python 3.7+ dictionaries maintain insertion order)
from collections import OrderedDict

# creating an ordered dictionary
ordered = OrderedDict()
ordered['a'] = 1
ordered['b'] = 2
ordered['c'] = 3

print("ordered dictionary:", ordered)

# comparing dictionaries
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 2, 'a': 1}
ordered1 = OrderedDict({'a': 1, 'b': 2})
ordered2 = OrderedDict({'b': 2, 'a': 1})

print("\ncomparisons:")
print("regular dictionaries equal:", dict1 == dict2)  # True
print("ordered dictionaries equal:", ordered1 == ordered2)  # False

# defaultdict - dictionary with default factory
from collections import defaultdict

# defaultdict with int factory (default value 0)
counts = defaultdict(int)
words = ['apple', 'banana', 'apple', 'cherry']
for word in words:
    counts[word] += 1

print("\nword counts using defaultdict:", dict(counts))

# defaultdict with list factory
groups = defaultdict(list)
pairs = [('a', 1), ('b', 2), ('a', 3), ('b', 4)]
for key, value in pairs:
    groups[key].append(value)

print("grouped items:", dict(groups))

# chainmap - search through multiple dictionaries
from collections import ChainMap

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
chain = ChainMap(dict1, dict2)

print("\nchainmap:")
print("value of 'a':", chain['a'])  # from dict1
print("value of 'b':", chain['b'])  # from dict1 (first occurrence)
print("value of 'c':", chain['c'])  # from dict2

# dictionary views
numbers = {1: 'one', 2: 'two', 3: 'three'}

# key view
keys = numbers.keys()
print("\ndictionary views:")
print("keys:", keys)

# value view
values = numbers.values()
print("values:", values)

# items view
items = numbers.items()
print("items:", items)

# views are dynamic (they update when dictionary changes)
numbers[4] = 'four'
print("\nafter adding item - keys:", keys)

# dictionary comprehension with conditions
squares = {x: x**2 for x in range(5) if x % 2 == 0}
print("\nsquares of even numbers:", squares)

# merging dictionaries with different strategies
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

# strategy 1: update (second dict overwrites first)
merged1 = dict1.copy()
merged1.update(dict2)
print("\nmerged (update):", merged1)

# strategy 2: using | operator (python 3.9+)
merged2 = dict1 | dict2
print("merged (|):", merged2)

# strategy 3: custom merge function
def merge_dicts(d1, d2, merge_fn=lambda x, y: y):
    result = d1.copy()
    for k, v in d2.items():
        if k in result:
            result[k] = merge_fn(result[k], v)
        else:
            result[k] = v
    return result

# merge with custom function (sum values if key exists in both)
merged3 = merge_dicts(dict1, dict2, lambda x, y: x + y)
print("merged (custom):", merged3)

# using dictionaries with custom objects
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# dictionary with custom objects as keys
points = {
    Point(0, 0): "origin",
    Point(1, 0): "right",
    Point(0, 1): "up"
}

print("\ndictionary with custom objects:")
print(points)
print("value at origin:", points[Point(0, 0)])

# practice exercises:
# 1. create a program that:
#    - implements a cache using defaultdict
#    - stores function results for different inputs
#    - handles cache expiration

# 2. create a program that:
#    - implements a nested defaultdict
#    - creates a tree-like structure
#    - allows easy navigation and modification

# 3. create a program that:
#    - uses ChainMap for configuration
#    - implements multiple levels (default, user, command-line)
#    - allows overriding values at different levels

# example solution for #1:
from time import time

class Cache:
    def __init__(self, expiration=10):  # 10 seconds expiration
        self.cache = defaultdict(dict)
        self.expiration = expiration
    
    def set(self, key, value):
        self.cache[key] = {
            'value': value,
            'timestamp': time()
        }
    
    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if time() - entry['timestamp'] < self.expiration:
                return entry['value']
            else:
                del self.cache[key]
        return None

# using the cache
cache = Cache(expiration=5)
cache.set('name', 'Alice')
print("\ncached value:", cache.get('name')) 