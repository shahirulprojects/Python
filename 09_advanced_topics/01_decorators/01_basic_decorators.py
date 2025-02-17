# basic decorators in python
# this file explains how to modify or enhance functions using decorators

# key concepts:
# 1. decorators are functions that modify other functions
# 2. they "wrap" a function to add new capabilities
# 3. can be applied using @ syntax or manually
# 4. can take arguments and preserve metadata
# 5. can be class-based or function-based

from typing import Any, Callable, TypeVar, cast
from functools import wraps
import time
import logging
from datetime import datetime

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# type variables for better type hints
F = TypeVar('F', bound=Callable[..., Any])

# 1. basic decorator pattern
def make_bold(func: F) -> F:
    """
    simple decorator that wraps text in bold tags
    demonstrates basic decorator pattern
    
    args:
        func: function to wrap
    
    returns:
        function: wrapped function
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return f"<b>{func(*args, **kwargs)}</b>"
    return cast(F, wrapper)

# example of basic decorator
@make_bold
def say_hello() -> str:
    """basic function that says hello"""
    return "hello!"

def log_calls(func: F) -> F:
    """
    decorator to log function calls with args and results
    demonstrates logging pattern
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # log function call
        logging.info(f"calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        
        # call function
        result = func(*args, **kwargs)
        
        # log result
        logging.info(f"{func.__name__} returned: {result}")
        return result
    
    return cast(F, wrapper)

def timer(func: F) -> F:
    """
    decorator to measure execution time
    demonstrates performance monitoring pattern
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # record start time
        start = time.time()
        
        # call function
        result = func(*args, **kwargs)
        
        # calculate duration
        duration = time.time() - start
        logging.info(f"{func.__name__} took {duration:.2f} seconds")
        
        return result
    
    return cast(F, wrapper)

# 2. decorators with arguments
def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[F], F]:
    """
    decorator to retry failed operations
    demonstrates parameterized decorator pattern
    
    args:
        max_attempts: maximum number of retry attempts
        delay: delay between retries in seconds
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None
            
            # try function multiple times
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    logging.warning(
                        f"attempt {attempt + 1}/{max_attempts} failed: {str(e)}"
                    )
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            
            raise last_error  # re-raise last error if all attempts fail
        
        return cast(F, wrapper)
    return decorator

def validate_args(*types: type) -> Callable[[F], F]:
    """
    decorator to validate argument types
    demonstrates type checking pattern
    
    args:
        *types: expected types for arguments
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # check number of arguments matches types
            if len(args) != len(types):
                raise ValueError(
                    f"expected {len(types)} arguments, got {len(args)}"
                )
            
            # validate each argument
            for arg, expected_type in zip(args, types):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"argument {arg} should be {expected_type.__name__}"
                    )
            
            return func(*args, **kwargs)
        
        return cast(F, wrapper)
    return decorator

# 3. caching decorator with inspection
def cache(func: F) -> F:
    """
    decorator to cache function results
    demonstrates memoization pattern with cache inspection
    """
    cache_data: dict = {}
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # create cache key from arguments
        key = str(args) + str(sorted(kwargs.items()))
        
        # return cached result if available
        if key in cache_data:
            logging.info(f"cache hit for {func.__name__}")
            return cache_data[key]
        
        # compute and cache result
        result = func(*args, **kwargs)
        cache_data[key] = result
        logging.info(f"cache miss for {func.__name__}")
        
        return result
    
    # add cache inspection method
    wrapper.cache_info = lambda: {
        "size": len(cache_data),
        "keys": list(cache_data.keys())
    }
    
    return cast(F, wrapper)

def deprecated(message: str = "") -> Callable[[F], F]:
    """
    decorator to mark functions as deprecated
    demonstrates warning pattern
    
    args:
        message: optional message explaining deprecation
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # warn about deprecation
            warning = f"{func.__name__} is deprecated."
            if message:
                warning += f" {message}"
            logging.warning(warning)
            
            return func(*args, **kwargs)
        
        return cast(F, wrapper)
    return decorator

# 4. class-based decorator example
class Timer:
    """
    class-based decorator that measures execution time
    demonstrates OOP-based decorator pattern
    """
    def __init__(self, func: F):
        wraps(func)(self)
        self.func = func
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = self.func(*args, **kwargs)
        end = time.time()
        print(f"{self.func.__name__} took {end - start:.2f} seconds")
        return result

# example usage and demonstrations
@log_calls
@timer
def fibonacci(n: int) -> int:
    """calculate nth fibonacci number"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@retry(max_attempts=3)
def unstable_operation() -> str:
    """simulate unstable operation"""
    if time.time() % 2 > 1:  # randomly fail
        raise ConnectionError("network error")
    return "operation successful"

@validate_args(int, int)
def divide(a: int, b: int) -> float:
    """divide two numbers"""
    return a / b

@cache
def expensive_operation(n: int) -> int:
    """simulate expensive operation"""
    time.sleep(1)  # simulate work
    return n * n

@deprecated("use new_function() instead")
def old_function() -> None:
    """old function that should not be used"""
    print("this is the old implementation")

# 5. authentication decorator example
def require_auth(func: F) -> F:
    """
    decorator that checks if user is authenticated
    demonstrates authentication pattern
    """
    @wraps(func)
    def wrapper(user: dict, *args: Any, **kwargs: Any) -> Any:
        if not user.get('is_authenticated'):
            return "please log in first"
        return func(user, *args, **kwargs)
    return cast(F, wrapper)

@require_auth
def view_profile(user: dict) -> str:
    """views a user's profile (requires authentication)"""
    return f"profile data for {user['name']}"

def main() -> None:
    """demonstrate decorator usage with comprehensive examples"""
    # 1. basic decorator usage
    print("\n1. testing basic decorator:")
    print(say_hello())  # should show bold text
    
    # 2. logging and timing
    print("\n2. testing logging and timing decorators:")
    result = fibonacci(5)
    print(f"fibonacci(5) = {result}")
    
    # 3. retry mechanism
    print("\n3. testing retry decorator:")
    try:
        result = unstable_operation()
        print(f"result: {result}")
    except ConnectionError as e:
        print(f"operation failed: {e}")
    
    # 4. argument validation
    print("\n4. testing validation decorator:")
    try:
        result = divide(10, 2)
        print(f"10 / 2 = {result}")
        
        # this will fail
        result = divide("10", 2)
        print(f"'10' / 2 = {result}")
    except (TypeError, ValueError) as e:
        print(f"validation error: {e}")
    
    # 5. caching
    print("\n5. testing cache decorator:")
    # first call (cache miss)
    result = expensive_operation(5)
    print(f"first call result: {result}")
    
    # second call (cache hit)
    result = expensive_operation(5)
    print(f"second call result: {result}")
    print(f"cache info: {expensive_operation.cache_info()}")
    
    # 6. deprecation warning
    print("\n6. testing deprecated decorator:")
    old_function()
    
    # 7. authentication
    print("\n7. testing authentication decorator:")
    authenticated_user = {'name': 'alice', 'is_authenticated': True}
    unauthenticated_user = {'name': 'bob', 'is_authenticated': False}
    
    print(view_profile(authenticated_user))
    print(view_profile(unauthenticated_user))

if __name__ == "__main__":
    main()

# advanced exercises and patterns to try:
# 1. memory monitoring decorator:
#    - track memory usage
#    - log memory peaks
#    - handle cleanup
#    - monitor specific objects

# 2. rate limiting decorator:
#    - implement token bucket
#    - handle concurrent requests
#    - support different strategies
#    - provide burst handling

# 3. validation decorator:
#    - check return types
#    - validate against schema
#    - support inheritance
#    - handle async functions

# 4. context management:
#    - preserve state
#    - handle resources
#    - support async
#    - manage transactions

# 5. debugging decorator:
#    - trace execution
#    - log call stack
#    - measure coverage
#    - profile performance 