# set performance considerations and multiset implementations
from collections import Counter
import time
import sys

# performance comparison: lists vs sets
# creating test data
test_data = list(range(10000))
search_items = list(range(5000, 5100))  # items to search for

# list performance
test_list = test_data.copy()
start_time = time.time()
for item in search_items:
    item in test_list  # searching in list
list_time = time.time() - start_time
print(f"list search time: {list_time:.4f} seconds")

# set performance
test_set = set(test_data)
start_time = time.time()
for item in search_items:
    item in test_set  # searching in set
set_time = time.time() - start_time
print(f"set search time: {set_time:.4f} seconds")
print(f"set is {list_time/set_time:.1f}x faster")

# memory usage comparison
list_size = sys.getsizeof(test_list) + sum(sys.getsizeof(i) for i in test_list)
set_size = sys.getsizeof(test_set) + sum(sys.getsizeof(i) for i in test_set)
print(f"\nmemory usage:")
print(f"list: {list_size:,} bytes")
print(f"set: {set_size:,} bytes")

# set operations performance
set1 = set(range(10000))
set2 = set(range(5000, 15000))

# measuring union performance
start_time = time.time()
union_result = set1 | set2
union_time = time.time() - start_time
print(f"\nunion operation time: {union_time:.4f} seconds")

# measuring intersection performance
start_time = time.time()
intersection_result = set1 & set2
intersection_time = time.time() - start_time
print(f"intersection operation time: {intersection_time:.4f} seconds")

# multiset implementation using Counter
print("\nmultiset examples using Counter:")
# creating a multiset
items = ['apple', 'banana', 'apple', 'cherry', 'date', 'banana']
multiset = Counter(items)
print("multiset:", multiset)

# adding elements
multiset.update(['apple', 'banana'])
print("after adding items:", multiset)

# removing elements
multiset.subtract(['apple'])
print("after removing one apple:", multiset)

# multiset operations
basket1 = Counter(['apple', 'apple', 'banana'])
basket2 = Counter(['apple', 'banana', 'banana'])

print("\nmultiset operations:")
print("basket1:", basket1)
print("basket2:", basket2)
print("sum of baskets:", basket1 + basket2)
print("difference of baskets:", basket1 - basket2)
print("intersection of baskets:", basket1 & basket2)
print("union of baskets:", basket1 | basket2)

# custom multiset implementation
class Multiset:
    def __init__(self, items=None):
        self.items = Counter(items if items else [])
    
    def add(self, item, count=1):
        self.items[item] += count
    
    def remove(self, item, count=1):
        if self.items[item] >= count:
            self.items[item] -= count
            if self.items[item] == 0:
                del self.items[item]
            return True
        return False
    
    def count(self, item):
        return self.items[item]
    
    def __str__(self):
        return str(dict(self.items))

# using custom multiset
print("\ncustom multiset example:")
ms = Multiset(['a', 'a', 'b', 'b', 'b'])
print("initial:", ms)
ms.add('c', 3)
print("after adding 3 'c's:", ms)
ms.remove('b', 2)
print("after removing 2 'b's:", ms)

# performance tips for sets:
# 1. use sets for membership testing
# 2. use sets for removing duplicates
# 3. use sets for mathematical set operations
# 4. use frozenset for immutable sets (can be used as dictionary keys)
# 5. use Counter for multisets when order doesn't matter

# practice exercises:
# 1. create a program that:
#    - compares performance of different set operations
#    - measures time and memory usage
#    - creates a performance report
#    - suggests optimal data structure

# 2. implement a multiset that:
#    - maintains insertion order
#    - supports all standard multiset operations
#    - provides efficient lookup
#    - handles negative counts

# 3. create a program that:
#    - processes a large text file
#    - counts word frequency
#    - compares Counter vs custom implementation
#    - measures performance differences

# example solution for #1:
def performance_test(n):
    # create test data
    data = list(range(n))
    
    # test list vs set for membership
    test_values = list(range(n//2, n//2 + 100))
    
    # list performance
    lst = data.copy()
    start = time.time()
    for val in test_values:
        _ = val in lst
    list_time = time.time() - start
    
    # set performance
    st = set(data)
    start = time.time()
    for val in test_values:
        _ = val in st
    set_time = time.time() - start
    
    return {
        'size': n,
        'list_time': list_time,
        'set_time': set_time,
        'speedup': list_time/set_time
    }

# run tests with different sizes
sizes = [1000, 10000, 100000]
print("\nperformance comparison:")
for size in sizes:
    result = performance_test(size)
    print(f"\nsize: {result['size']:,}")
    print(f"list time: {result['list_time']:.4f}s")
    print(f"set time: {result['set_time']:.4f}s")
    print(f"speedup: {result['speedup']:.1f}x") 