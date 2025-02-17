# advanced encapsulation patterns in python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
import json

# advanced encapsulation with descriptor protocol
class ValidatedString:
    def __init__(self, min_length: int = 1, max_length: int = 100):
        self.min_length = min_length
        self.max_length = max_length
        self.name = None  # will be set by __set_name__
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        if not self.min_length <= len(value) <= self.max_length:
            raise ValueError(
                f"{self.name} must be between {self.min_length} "
                f"and {self.max_length} characters"
            )
        instance.__dict__[self.name] = value

# advanced encapsulation with metaclass
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# advanced encapsulation with context manager
class DatabaseConnection:
    def __init__(self, connection_string: str):
        self.__connection_string = connection_string
        self.__is_connected = False
        self.__transaction_count = 0
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
    
    def connect(self):
        # simulate database connection
        print(f"connecting to database: {self.__connection_string}")
        self.__is_connected = True
    
    def disconnect(self):
        if self.__is_connected:
            print("disconnecting from database")
            self.__is_connected = False
    
    def execute(self, query: str):
        if not self.__is_connected:
            raise RuntimeError("not connected to database")
        print(f"executing query: {query}")

# advanced encapsulation with property factory
def validated_property(name: str, validator):
    storage_name = f"_{name}"
    
    @property
    def prop(self):
        return getattr(self, storage_name)
    
    @prop.setter
    def prop(self, value):
        validator(value)
        setattr(self, storage_name, value)
    
    return prop

# example class using descriptor
class User:
    username = ValidatedString(min_length=3, max_length=20)
    password = ValidatedString(min_length=8, max_length=50)
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

# example class using singleton metaclass
class Configuration(metaclass=Singleton):
    def __init__(self):
        self.__settings: Dict[str, Any] = {}
        self.__load_time = datetime.now()
    
    def set(self, key: str, value: Any):
        self.__settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.__settings.get(key, default)
    
    @property
    def load_time(self) -> datetime:
        return self.__load_time

# example class using property factory
class Product:
    def validate_price(value):
        if not isinstance(value, (int, float)):
            raise TypeError("price must be a number")
        if value < 0:
            raise ValueError("price cannot be negative")
    
    def validate_stock(value):
        if not isinstance(value, int):
            raise TypeError("stock must be an integer")
        if value < 0:
            raise ValueError("stock cannot be negative")
    
    price = validated_property("price", validate_price)
    stock = validated_property("stock", validate_stock)
    
    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

# advanced encapsulation with state management
class AuditedAttribute:
    def __init__(self):
        self.name = None
        self.changes = []
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        old_value = instance.__dict__.get(self.name)
        instance.__dict__[self.name] = value
        self.changes.append({
            'timestamp': datetime.now(),
            'old_value': old_value,
            'new_value': value
        })

# example usage of advanced patterns
print("testing advanced encapsulation patterns:")

# testing validated string descriptor
try:
    user = User("alice", "secretpass123")
    print(f"\nuser created - username: {user.username}")
    user.username = "ab"  # will raise ValueError
except ValueError as e:
    print(f"validation error: {e}")

# testing singleton configuration
config1 = Configuration()
config2 = Configuration()
config1.set("theme", "dark")
print(f"\nconfigs are same object: {config1 is config2}")
print(f"theme from config2: {config2.get('theme')}")

# testing context manager
print("\ndatabase operations:")
with DatabaseConnection("mysql://localhost:3306/mydb") as db:
    db.execute("select * from users")

# testing property factory
try:
    product = Product("laptop", 999.99, 10)
    print(f"\nproduct created - price: ${product.price}, stock: {product.stock}")
    product.price = -100  # will raise ValueError
except ValueError as e:
    print(f"validation error: {e}")

# example of advanced state tracking
class AuditedUser:
    name = AuditedAttribute()
    email = AuditedAttribute()
    
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def get_audit_trail(self) -> Dict[str, List[Dict]]:
        return {
            'name': self.name.changes,
            'email': self.email.changes
        }

print("\nauditing changes:")
audited_user = AuditedUser("alice", "alice@example.com")
audited_user.name = "alice smith"
audited_user.email = "alice.smith@example.com"
print("audit trail:", json.dumps(audited_user.get_audit_trail(), default=str, indent=2))

# practice exercises:
# 1. create a class that:
#    - implements a caching descriptor
#    - stores computed values
#    - invalidates cache when dependencies change
#    - tracks cache hits and misses

# 2. create a class that:
#    - implements a proxy pattern
#    - controls access to expensive resources
#    - implements lazy loading
#    - logs all access attempts

# 3. create a class that:
#    - implements a state machine
#    - validates state transitions
#    - maintains state history
#    - provides undo/redo functionality

# example solution for #1:
class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
        self.cache = {}
        self.hits = 0
        self.misses = 0
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        if instance not in self.cache:
            self.cache[instance] = self.func(instance)
            self.misses += 1
        else:
            self.hits += 1
        
        return self.cache[instance]
    
    def invalidate(self, instance):
        self.cache.pop(instance, None)
    
    def get_stats(self):
        return {
            'hits': self.hits,
            'misses': self.misses,
            'cache_size': len(self.cache)
        }

class Circle:
    def __init__(self, radius: float):
        self._radius = radius
    
    @CachedProperty
    def area(self) -> float:
        print("calculating area...")  # simulate expensive computation
        return 3.14159 * self._radius ** 2
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        self._radius = value
        # invalidate cached properties
        type(self).area.invalidate(self)

# testing the cached property
print("\ntesting cached property:")
circle = Circle(5)
print(f"area: {circle.area}")  # will calculate
print(f"area: {circle.area}")  # will use cache
circle.radius = 6  # invalidates cache
print(f"area with new radius: {circle.area}")  # will calculate again
print("cache stats:", type(circle).area.get_stats()) 