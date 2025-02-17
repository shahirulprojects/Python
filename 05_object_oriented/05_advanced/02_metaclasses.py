#!/usr/bin/env python3

# metaclasses in python
# these are classes for classes - they allow you to customize class creation
# they're advanced features that let you control how classes are defined

class LoggedMeta(type):
    # metaclass that adds logging to all method calls
    
    def __new__(cls, name, bases, attrs):
        # this method is called when a new class is created
        # we'll wrap all methods with logging functionality
        
        # iterate through all attributes
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                # if it's a method (but not a special method), wrap it with logging
                attrs[attr_name] = cls.log_method(attr_value)
        
        # create the class using the modified attributes
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def log_method(method):
        # wrapper function that adds logging
        def logged_method(*args, **kwargs):
            # print information about the method call
            print(f"calling method: {method.__name__}")
            print(f"with args: {args[1:]} and kwargs: {kwargs}")  # args[1:] to skip 'self'
            
            # call the original method
            result = method(*args, **kwargs)
            
            # print information about the return value
            print(f"method {method.__name__} returned: {result}\n")
            return result
        
        return logged_method

# singleton metaclass - ensures only one instance of a class can exist
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        # this method is called when creating a new instance
        if cls not in cls._instances:
            # if no instance exists, create one
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# example class using the logging metaclass
class Calculator(metaclass=LoggedMeta):
    def add(self, x, y):
        return x + y
    
    def multiply(self, x, y):
        return x * y

# example class using the singleton metaclass
class Configuration(metaclass=Singleton):
    def __init__(self):
        self.settings = {}
    
    def set_setting(self, key, value):
        self.settings[key] = value
    
    def get_setting(self, key):
        return self.settings.get(key)

# practical examples showing how metaclasses work
def demonstrate_metaclasses():
    print("demonstrating logged metaclass:")
    calc = Calculator()
    calc.add(5, 3)
    calc.multiply(4, 2)
    
    print("\ndemonstrating singleton metaclass:")
    # create two configuration instances
    config1 = Configuration()
    config2 = Configuration()
    
    # prove they're the same instance
    print(f"are config1 and config2 the same object? {config1 is config2}")
    
    # modify settings through one instance
    config1.set_setting("theme", "dark")
    
    # access settings through the other instance
    print(f"theme setting from config2: {config2.get_setting('theme')}")

# example of a metaclass that enforces attribute types
class TypeChecked(type):
    def __new__(cls, name, bases, attrs):
        # get type annotations from the class
        annotations = attrs.get('__annotations__', {})
        
        # create new methods that check types
        for attr_name, attr_value in attrs.items():
            if attr_name in annotations:
                # wrap the attribute with type checking
                attrs[attr_name] = cls.make_type_checked_property(
                    attr_name,
                    attr_value,
                    annotations[attr_name]
                )
        
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def make_type_checked_property(name, value, expected_type):
        private_name = f'_{name}'
        
        def getter(self):
            return getattr(self, private_name)
        
        def setter(self, value):
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"{name} must be of type {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
            setattr(self, private_name, value)
        
        return property(getter, setter)

# example class using the type checking metaclass
class Person(metaclass=TypeChecked):
    name: str
    age: int
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

if __name__ == "__main__":
    demonstrate_metaclasses()
    
    # demonstrate type checking
    print("\ndemonstrating type checking metaclass:")
    try:
        # this works fine
        person = Person("alice", 30)
        print(f"created person: {person.name}, {person.age}")
        
        # this will raise a TypeError
        person.age = "thirty"
    except TypeError as e:
        print(f"type error caught: {e}") 