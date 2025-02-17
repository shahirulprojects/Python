# introduction to classes and objects in python
# classes are blueprints for creating objects

# basic class definition
class Dog:
    # class attribute (shared by all instances)
    species = "Canis familiaris"
    
    # initializer method (constructor)
    def __init__(self, name, age):
        # instance attributes (unique to each instance)
        self.name = name
        self.age = age
    
    # instance method
    def bark(self):
        return f"{self.name} says woof!"
    
    # instance method with parameters
    def change_name(self, new_name):
        self.name = new_name
    
    # string representation
    def __str__(self):
        return f"{self.name} is {self.age} years old"
    
    # official string representation
    def __repr__(self):
        return f"Dog(name='{self.name}', age={self.age})"

# creating instances (objects)
dog1 = Dog("buddy", 5)
dog2 = Dog("max", 3)

# accessing attributes and methods
print("basic class usage:")
print(f"dog1 name: {dog1.name}")
print(f"dog2 age: {dog2.age}")
print(f"dog1 species: {dog1.species}")  # accessing class attribute
print(f"dog1 bark: {dog1.bark()}")

# modifying attributes
print("\nmodifying attributes:")
dog1.change_name("charlie")
print(f"dog1's new name: {dog1.name}")

# string representations
print("\nstring representations:")
print(str(dog1))  # uses __str__
print(repr(dog1))  # uses __repr__

# class with property decorators
class Circle:
    def __init__(self, radius):
        self._radius = radius  # protected attribute
    
    # getter property
    @property
    def radius(self):
        return self._radius
    
    # setter property
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("radius must be positive")
        self._radius = value
    
    # computed property
    @property
    def area(self):
        return 3.14159 * self._radius ** 2
    
    # computed property
    @property
    def circumference(self):
        return 2 * 3.14159 * self._radius

# using properties
print("\nusing properties:")
circle = Circle(5)
print(f"radius: {circle.radius}")
print(f"area: {circle.area:.2f}")
print(f"circumference: {circle.circumference:.2f}")

# trying to set invalid radius
try:
    circle.radius = -1
except ValueError as e:
    print(f"error: {e}")

# class with class methods and static methods
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    # instance method
    def display(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"
    
    # class method (can access class state)
    @classmethod
    def from_string(cls, date_string):
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    # static method (cannot access class or instance state)
    @staticmethod
    def is_valid_date(year, month, day):
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= 31):
            return False
        return True

# using different method types
print("\nusing different method types:")
# using constructor
date1 = Date(2024, 3, 15)
print(f"date1: {date1.display()}")

# using class method
date2 = Date.from_string("2024-03-16")
print(f"date2: {date2.display()}")

# using static method
print(f"is valid date? {Date.is_valid_date(2024, 13, 1)}")

# class with private attributes and name mangling
class BankAccount:
    def __init__(self, account_number, balance):
        self.__account_number = account_number  # private attribute
        self.__balance = balance  # private attribute
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self.__balance
    
    def get_account_info(self):
        return f"account: ***{str(self.__account_number)[-4:]} balance: ${self.__balance}"

# using private attributes
print("\nusing private attributes:")
account = BankAccount(12345678, 1000)
print(f"initial: {account.get_account_info()}")
account.deposit(500)
print(f"after deposit: {account.get_account_info()}")
account.withdraw(200)
print(f"after withdrawal: {account.get_account_info()}")

# practice exercises:
# 1. create a class that:
#    - represents a student
#    - stores grades for different subjects
#    - calculates gpa
#    - includes validation for grades

# 2. create a class that:
#    - implements a shopping cart
#    - adds/removes items
#    - calculates total
#    - applies discounts
#    - handles quantity updates

# 3. create a class that:
#    - represents a playlist
#    - adds/removes songs
#    - shuffles playlist
#    - filters by artist/genre
#    - calculates total duration

# example solution for #1:
class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.__grades = {}  # private dictionary for grades
    
    def add_grade(self, subject, grade):
        """add or update grade for a subject."""
        if not (0 <= grade <= 100):
            raise ValueError("grade must be between 0 and 100")
        self.__grades[subject] = grade
    
    def get_grade(self, subject):
        """get grade for a specific subject."""
        return self.__grades.get(subject)
    
    def get_gpa(self):
        """calculate gpa (assumes 100-point scale)."""
        if not self.__grades:
            return 0.0
        return sum(self.__grades.values()) / len(self.__grades)
    
    def get_report(self):
        """generate a grade report."""
        report = f"student: {self.name} (id: {self.student_id})\n"
        for subject, grade in sorted(self.__grades.items()):
            report += f"{subject}: {grade}\n"
        report += f"gpa: {self.get_gpa():.2f}"
        return report

# testing the solution
print("\ntesting student class:")
student = Student("alice smith", "a12345")
student.add_grade("math", 95)
student.add_grade("science", 88)
student.add_grade("history", 92)
print(student.get_report()) 