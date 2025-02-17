# class decorators in python
from typing import Any, Callable, Type, TypeVar, cast
from functools import wraps
import logging
from datetime import datetime

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# type variable for class types
T = TypeVar('T')

def singleton(cls: Type[T]) -> Type[T]:
    """decorator to implement singleton pattern."""
    instances = {}
    
    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return cast(Type[T], get_instance)

def log_methods(cls: Type[T]) -> Type[T]:
    """decorator to log all method calls of a class."""
    # get all method names
    method_names = [
        attr for attr in dir(cls) 
        if callable(getattr(cls, attr)) and not attr.startswith('__')
    ]
    
    # wrap each method with logging
    for method_name in method_names:
        method = getattr(cls, method_name)
        
        @wraps(method)
        def wrapped(self: Any, *args: Any, **kwargs: Any) -> Any:
            logging.info(
                f"calling {cls.__name__}.{method_name} "
                f"with args: {args}, kwargs: {kwargs}"
            )
            result = method(self, *args, **kwargs)
            logging.info(
                f"{cls.__name__}.{method_name} returned: {result}"
            )
            return result
        
        setattr(cls, method_name, wrapped)
    
    return cls

def validate_attributes(cls: Type[T]) -> Type[T]:
    """decorator to validate class attributes."""
    original_init = cls.__init__
    
    @wraps(original_init)
    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        # call original __init__
        original_init(self, *args, **kwargs)
        
        # validate attributes
        for name, value in self.__dict__.items():
            # get type hint if available
            type_hint = cls.__annotations__.get(name)
            if type_hint and not isinstance(value, type_hint):
                raise TypeError(
                    f"attribute {name} should be {type_hint.__name__}, "
                    f"got {type(value).__name__}"
                )
    
    cls.__init__ = new_init
    return cls

def frozen(cls: Type[T]) -> Type[T]:
    """decorator to make class immutable."""
    original_setattr = cls.__setattr__
    
    def new_setattr(self: Any, name: str, value: Any) -> None:
        if hasattr(self, name):
            raise AttributeError(
                f"can't modify frozen class attribute '{name}'"
            )
        original_setattr(self, name, value)
    
    cls.__setattr__ = new_setattr
    return cls

def register(registry: dict) -> Callable[[Type[T]], Type[T]]:
    """decorator to register classes in a registry."""
    def decorator(cls: Type[T]) -> Type[T]:
        registry[cls.__name__] = cls
        return cls
    return decorator

# example usage
class_registry = {}

@singleton
class DatabaseConnection:
    """singleton database connection class."""
    def __init__(self, host: str = "localhost"):
        self.host = host
        self.connected = False
    
    def connect(self) -> bool:
        if not self.connected:
            logging.info(f"connecting to database at {self.host}")
            self.connected = True
        return self.connected

@log_methods
class Calculator:
    """calculator with logged methods."""
    def add(self, a: float, b: float) -> float:
        return a + b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b

@validate_attributes
class Person:
    """person class with validated attributes."""
    name: str
    age: int
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

@frozen
class Configuration:
    """immutable configuration class."""
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

@register(class_registry)
class Worker:
    """registered worker class."""
    def __init__(self, name: str):
        self.name = name
    
    def work(self) -> str:
        return f"{self.name} is working"

def main():
    """demonstrate class decorator usage."""
    # 1. singleton decorator
    print("1. testing singleton decorator:")
    db1 = DatabaseConnection("localhost")
    db2 = DatabaseConnection("127.0.0.1")  # same instance
    print(f"same instance: {db1 is db2}")
    db1.connect()
    print(f"db2 connected: {db2.connected}")
    
    # 2. log methods decorator
    print("\n2. testing log methods decorator:")
    calc = Calculator()
    result = calc.add(5, 3)
    print(f"5 + 3 = {result}")
    result = calc.multiply(4, 2)
    print(f"4 * 2 = {result}")
    
    # 3. validate attributes decorator
    print("\n3. testing validate attributes decorator:")
    try:
        # valid person
        person = Person("Alice", 25)
        print(f"created person: {person.name}, {person.age}")
        
        # invalid person
        person = Person("Bob", "30")  # should raise TypeError
    except TypeError as e:
        print(f"validation error: {e}")
    
    # 4. frozen decorator
    print("\n4. testing frozen decorator:")
    config = Configuration("localhost", 8080)
    try:
        config.port = 9090  # should raise AttributeError
    except AttributeError as e:
        print(f"modification error: {e}")
    
    # 5. register decorator
    print("\n5. testing register decorator:")
    print("registered classes:", list(class_registry.keys()))
    worker_class = class_registry["Worker"]
    worker = worker_class("John")
    print(worker.work())

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a class decorator that:
#    - implements observer pattern
#    - manages subscribers
#    - handles event notifications
#    - supports multiple event types

# 2. create a class decorator that:
#    - implements proxy pattern
#    - controls access to methods
#    - logs method access
#    - supports lazy initialization

# 3. create a class decorator that:
#    - implements factory pattern
#    - manages object creation
#    - supports subclass registration
#    - handles dependency injection 