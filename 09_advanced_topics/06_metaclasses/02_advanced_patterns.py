from typing import Any, Dict, Type, TypeVar, Optional
from datetime import datetime
import functools
import inspect

# welcome to advanced metaclass patterns! here we'll explore some really cool
# real-world use cases for metaclasses that you might actually use in your projects :D

T = TypeVar('T')  # type variable for better type hints

class ValidationError(Exception):
    """custom error for validation failures"""
    pass

# this metaclass adds automatic validation to class attributes
class ValidatingMetaclass(type):
    # we store the validation rules here
    _validators: Dict[str, Dict[str, Any]] = {}
    
    def __new__(
        mcs: Type[Any],
        name: str,
        bases: tuple,
        namespace: Dict[str, Any]
    ) -> Type[Any]:
        # find all attributes that need validation
        for key, value in namespace.items():
            if hasattr(value, '_validate'):
                mcs._validators.setdefault(name, {})[key] = value._validate
        
        # create the class with validation
        return super().__new__(mcs, name, bases, namespace)
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        # this runs when we create an instance
        instance = super().__call__(*args, **kwargs)
        
        # validate all attributes
        for attr, validator in cls._validators.get(cls.__name__, {}).items():
            value = getattr(instance, attr, None)
            if not validator(value):
                raise ValidationError(
                    f"validation failed for {attr}: {value}"
                )
        
        return instance

# decorator to add validation rules to attributes
def validate_with(validator: callable) -> callable:
    def decorator(f: T) -> T:
        f._validate = validator
        return f
    return decorator

# metaclass that adds automatic property creation
class AutoPropertyMetaclass(type):
    def __new__(
        mcs: Type[Any],
        name: str,
        bases: tuple,
        namespace: Dict[str, Any]
    ) -> Type[Any]:
        # find all attributes that should be properties
        for key, value in list(namespace.items()):
            if not key.startswith('_') and not callable(value):
                # create private variable
                private_key = f'_{key}'
                namespace[private_key] = value
                
                # create property with getter and setter
                namespace[key] = property(
                    # getter returns private variable
                    lambda self, pk=private_key: getattr(self, pk),
                    # setter validates and sets private variable
                    lambda self, value, pk=private_key: setattr(self, pk, value)
                )
        
        return super().__new__(mcs, name, bases, namespace)

# metaclass that adds logging to all methods
class LoggingMetaclass(type):
    def __new__(
        mcs: Type[Any],
        name: str,
        bases: tuple,
        namespace: Dict[str, Any]
    ) -> Type[Any]:
        # wrap all methods with logging
        for key, value in namespace.items():
            if callable(value) and not key.startswith('_'):
                namespace[key] = mcs._add_logging(value)
        
        return super().__new__(mcs, name, bases, namespace)
    
    @staticmethod
    def _add_logging(method: callable) -> callable:
        # get method's signature for better logging
        sig = inspect.signature(method)
        
        @functools.wraps(method)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # log method call with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] calling {method.__name__}{sig}")
            
            # call method and log result
            result = method(*args, **kwargs)
            print(f"[{timestamp}] {method.__name__} returned: {result}")
            
            return result
        
        return wrapper

# now let's use these metaclasses in real-world examples

# example 1: data validation
class User(metaclass=ValidatingMetaclass):
    @validate_with(lambda x: isinstance(x, str) and len(x) >= 3)
    def username(self) -> None:
        pass
    
    @validate_with(lambda x: isinstance(x, str) and '@' in x)
    def email(self) -> None:
        pass
    
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

# example 2: automatic properties
class Configuration(metaclass=AutoPropertyMetaclass):
    # these will automatically become properties
    host = "localhost"
    port = 8080
    debug = True

# example 3: method logging
class PaymentProcessor(metaclass=LoggingMetaclass):
    def process_payment(self, amount: float) -> bool:
        # simulate payment processing
        return amount > 0
    
    def refund_payment(self, transaction_id: str) -> bool:
        # simulate refund
        return len(transaction_id) > 0

def main():
    # test validation
    try:
        user = User("al", "invalid_email")  # this will fail
    except ValidationError as e:
        print(f"validation failed as expected: {e}")
    
    user = User("alice", "alice@example.com")  # this works
    print(f"created valid user: {user.username}")
    
    # test auto properties
    config = Configuration()
    print(f"\noriginal host: {config.host}")
    config.host = "127.0.0.1"  # this works through property
    print(f"new host: {config.host}")
    
    # test method logging
    processor = PaymentProcessor()
    processor.process_payment(100.0)
    processor.refund_payment("txn_123")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a metaclass that:
#    - implements the singleton pattern
#    - ensures only one instance exists
#    - handles thread safety

# 2. create a metaclass that:
#    - implements interface checking
#    - ensures required methods are implemented
#    - validates method signatures

# 3. create a metaclass that:
#    - adds serialization capabilities
#    - converts objects to/from json
#    - handles nested objects 