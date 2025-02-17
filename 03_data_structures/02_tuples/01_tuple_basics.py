# tuples are immutable sequences in python
# they're like lists, but can't be changed after creation

# creating tuples
empty_tuple = ()  # empty tuple
single_item = (1,)  # note the comma - needed for single item
numbers = (1, 2, 3, 4, 5)  # tuple of numbers
mixed = (1, "hello", 3.14, True)  # tuple with different types
nested = (1, (2, 3), (4, 5))  # nested tuple

# tuple packing - parentheses are optional
coordinates = 3, 4  # creates tuple (3, 4)
print("coordinates:", coordinates)

# tuple unpacking
x, y = coordinates  # assigns x = 3, y = 4
print("x:", x, "y:", y)

# multiple assignment using tuples
a, b, c = 1, 2, 3
print("\na:", a, "b:", b, "c:", c)

# swapping variables using tuples
a, b = b, a  # swap values
print("after swap - a:", a, "b:", b)

# accessing tuple elements (similar to lists)
point = (1, 2, 3)
print("\nfirst element:", point[0])
print("last element:", point[-1])

# slicing tuples
numbers = (0, 1, 2, 3, 4, 5)
print("\nfirst three:", numbers[:3])
print("last three:", numbers[-3:])

# tuple methods
numbers = (1, 2, 2, 3, 4, 2, 5)
print("\ncount of 2:", numbers.count(2))  # count occurrences
print("index of 4:", numbers.index(4))  # find position

# converting between tuples and lists
numbers_list = list(numbers)  # tuple to list
numbers_tuple = tuple(numbers_list)  # list to tuple
print("\nlist:", numbers_list)
print("tuple:", numbers_tuple)

# using tuples as dictionary keys (lists can't be used as keys)
locations = {
    (0, 0): "origin",
    (1, 0): "right",
    (0, 1): "up"
}
print("\nlocation at (0, 0):", locations[(0, 0)])

# returning multiple values from functions
def get_coordinates():
    return (3, 4)  # returns tuple

x, y = get_coordinates()  # unpacks returned tuple
print("\nreturned coordinates - x:", x, "y:", y)

# tuple comparison
tuple1 = (1, 2, 3)
tuple2 = (1, 2, 4)
tuple3 = (1, 2, 3)

print("\ntuple comparisons:")
print("tuple1 == tuple2:", tuple1 == tuple2)
print("tuple1 == tuple3:", tuple1 == tuple3)
print("tuple1 < tuple2:", tuple1 < tuple2)  # compares elements in order

# named tuples (more readable tuples)
from collections import namedtuple

# creating a named tuple type
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print("\nnamed tuple point:", p)
print("x coordinate:", p.x)  # access by name
print("y coordinate:", p[1])  # access by index

# practice exercises:
# 1. create a function that:
#    - takes a list of (x, y) coordinates as tuples
#    - calculates the distance from origin (0, 0) for each point
#    - returns a list of distances

# 2. create a program that:
#    - defines a named tuple for storing student records
#    - creates several student records
#    - sorts them by grade
#    - prints the sorted records

# 3. create a function that:
#    - takes two points as tuples
#    - calculates the midpoint
#    - returns the midpoint as a tuple

# example solution for #1:
import math

def calculate_distances(points):
    distances = []
    for x, y in points:
        distance = math.sqrt(x**2 + y**2)
        distances.append(round(distance, 2))
    return distances

points = [(1, 1), (2, 2), (3, 4)]
distances = calculate_distances(points)
print("\npoints:", points)
print("distances from origin:", distances) 