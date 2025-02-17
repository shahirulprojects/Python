# advanced tuple operations in python
# this file covers advanced tuple concepts and namedtuples

# 1. tuple unpacking
# tuples can be unpacked into individual variables
# this is a powerful feature for working with multiple values

# basic unpacking
coordinates = (10, 20)
x, y = coordinates    # x = 10, y = 20

# unpacking with * operator
numbers = (1, 2, 3, 4, 5)
first, *middle, last = numbers
# first = 1, middle = [2, 3, 4], last = 5

# 2. using collections.namedtuple
from collections import namedtuple

# creating a named tuple type
# this makes tuples more readable by giving names to positions
Point = namedtuple('Point', ['x', 'y'])

# creating instances
p1 = Point(10, 20)
p2 = Point(x=30, y=40)    # can use keyword arguments

# accessing values
print(p1.x)        # using dot notation: 10
print(p1[0])       # using index: 10
print(p2._asdict())    # convert to dictionary: {'x': 30, 'y': 40}

# 3. practical examples with namedtuples

# representing a student record
Student = namedtuple('Student', ['name', 'age', 'grades'])

def calculate_average(student):
    """
    calculates average grade for a student
    
    args:
        student (Student): student namedtuple
    
    returns:
        float: average grade
    """
    # using the named fields makes code more readable
    return sum(student.grades) / len(student.grades)

# creating a student record
alice = Student('alice', 20, (85, 92, 78))
print(f"average grade for {alice.name}: {calculate_average(alice)}")

# 4. tuple operations and methods

def compare_points(p1, p2):
    """
    compares two points and returns their relationship
    
    args:
        p1 (Point): first point
        p2 (Point): second point
    
    returns:
        str: description of their relationship
    """
    # tuples support comparison operations
    if p1 == p2:
        return "points are identical"
    
    # can compare individual components
    if p1.x == p2.x:
        return "points have same x coordinate"
    if p1.y == p2.y:
        return "points have same y coordinate"
    
    return "points are different"

# 5. using namedtuples for data processing

# representing weather data
WeatherData = namedtuple('WeatherData', ['date', 'temperature', 'humidity'])

def process_weather_data(data_points):
    """
    processes a list of weather measurements
    
    args:
        data_points (list): list of WeatherData tuples
    
    returns:
        dict: processed statistics
    """
    # using named fields makes the code self-documenting
    temperatures = [point.temperature for point in data_points]
    humidities = [point.humidity for point in data_points]
    
    return {
        'avg_temp': sum(temperatures) / len(temperatures),
        'avg_humidity': sum(humidities) / len(humidities),
        'max_temp': max(temperatures),
        'min_temp': min(temperatures)
    }

# example weather data
weather_records = [
    WeatherData('2024-02-01', 22.5, 65),
    WeatherData('2024-02-02', 24.0, 70),
    WeatherData('2024-02-03', 21.0, 75)
]

stats = process_weather_data(weather_records)

# 6. converting between namedtuples and dictionaries

def update_student_record(student, **updates):
    """
    creates a new student record with updated values
    
    args:
        student (Student): original student record
        **updates: keyword arguments with new values
    
    returns:
        Student: new student record
    """
    # convert to dictionary, update, and create new namedtuple
    student_dict = student._asdict()
    student_dict.update(updates)
    return Student(**student_dict)

# example usage
bob = Student('bob', 19, (88, 92, 85))
updated_bob = update_student_record(bob, age=20, grades=(90, 95, 88))

# 7. using namedtuples in data structures

# representing a rectangle
Rectangle = namedtuple('Rectangle', ['width', 'height', 'position'])
Position = namedtuple('Position', ['x', 'y'])

def calculate_area(rect):
    """
    calculates the area of a rectangle
    
    args:
        rect (Rectangle): rectangle to measure
    
    returns:
        float: area of rectangle
    """
    return rect.width * rect.height

def is_overlapping(rect1, rect2):
    """
    checks if two rectangles overlap
    
    args:
        rect1 (Rectangle): first rectangle
        rect2 (Rectangle): second rectangle
    
    returns:
        bool: true if rectangles overlap
    """
    # named fields make the logic easier to understand
    return not (
        rect1.position.x + rect1.width < rect2.position.x or
        rect2.position.x + rect2.width < rect1.position.x or
        rect1.position.y + rect1.height < rect2.position.y or
        rect2.position.y + rect2.height < rect1.position.y
    )

# example usage
rect1 = Rectangle(5, 3, Position(0, 0))
rect2 = Rectangle(4, 2, Position(3, 1))

print(f"rectangle 1 area: {calculate_area(rect1)}")
print(f"rectangles overlap: {is_overlapping(rect1, rect2)}")

# 8. immutability and performance

def optimize_points(points):
    """
    demonstrates why tuples are good for optimization
    
    args:
        points (list): list of Point tuples
    
    returns:
        set: unique points
    """
    # tuples are hashable, so they can be used in sets
    # this efficiently removes duplicates
    unique_points = set(points)
    return unique_points

# example usage
points = [
    Point(1, 2),
    Point(1, 2),    # duplicate
    Point(3, 4)
]

unique = optimize_points(points)
print(f"unique points: {unique}") 