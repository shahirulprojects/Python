# method decorators in python
from typing import Any, Callable, TypeVar, cast
from functools import wraps
import logging
import time
import asyncio
from datetime import datetime

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# type variables for better type hints
F = TypeVar('F', bound=Callable[..., Any])

def property_cached(method: F) -> property:
    """decorator to cache property values."""
    name = f"_{method.__name__}"
    
    @property
    @wraps(method)
    def wrapper(self: Any) -> Any:
        try:
            return getattr(self, name)
        except AttributeError:
            value = method(self)
            setattr(self, name, value)
            return value
    
    return wrapper

def synchronized(lock: Any = None) -> Callable[[F], F]:
    """decorator to synchronize method access."""
    def decorator(method: F) -> F:
        # create lock if not provided
        nonlocal lock
        if lock is None:
            lock = asyncio.Lock()
        
        @wraps(method)
        async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            async with lock:
                return await method(self, *args, **kwargs)
        
        return cast(F, wrapper)
    return decorator

def validate_self(method: F) -> F:
    """decorator to validate instance attributes."""
    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        # check if required attributes exist
        required_attrs = getattr(method, '__required_attrs__', [])
        for attr in required_attrs:
            if not hasattr(self, attr):
                raise AttributeError(
                    f"missing required attribute '{attr}'"
                )
        
        return method(self, *args, **kwargs)
    
    return wrapper

def requires_attrs(*attrs: str) -> Callable[[F], F]:
    """decorator to specify required attributes."""
    def decorator(method: F) -> F:
        method.__required_attrs__ = attrs
        return validate_self(method)
    return decorator

def async_retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[F], F]:
    """decorator to retry async methods."""
    def decorator(method: F) -> F:
        @wraps(method)
        async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            last_error = None
            
            for attempt in range(max_attempts):
                try:
                    return await method(self, *args, **kwargs)
                except Exception as e:
                    last_error = e
                    logging.warning(
                        f"attempt {attempt + 1}/{max_attempts} failed: {str(e)}"
                    )
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay)
            
            raise last_error
        
        return cast(F, wrapper)
    return decorator

def method_timeout(seconds: float) -> Callable[[F], F]:
    """decorator to set method timeout."""
    def decorator(method: F) -> F:
        @wraps(method)
        async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            try:
                return await asyncio.wait_for(
                    method(self, *args, **kwargs),
                    timeout=seconds
                )
            except asyncio.TimeoutError:
                raise TimeoutError(
                    f"{method.__name__} timed out after {seconds} seconds"
                )
        
        return cast(F, wrapper)
    return decorator

# example usage
class DataProcessor:
    """class demonstrating method decorators."""
    def __init__(self, data: list):
        self.data = data
        self._lock = asyncio.Lock()
    
    @property_cached
    def processed_data(self) -> list:
        """expensive data processing."""
        logging.info("processing data...")
        time.sleep(1)  # simulate work
        return [x * 2 for x in self.data]
    
    @synchronized()
    async def update_data(self, new_data: list) -> None:
        """synchronized data update."""
        logging.info("updating data...")
        await asyncio.sleep(0.1)  # simulate work
        self.data = new_data
    
    @requires_attrs('data')
    def validate_data(self) -> bool:
        """validate data with required attributes."""
        return all(isinstance(x, (int, float)) for x in self.data)
    
    @async_retry(max_attempts=3)
    async def fetch_data(self) -> list:
        """fetch data with retry."""
        if time.time() % 2 > 1:  # randomly fail
            raise ConnectionError("network error")
        return self.data
    
    @method_timeout(1.0)
    async def slow_process(self) -> None:
        """slow process with timeout."""
        await asyncio.sleep(2)  # will timeout

async def main():
    """demonstrate method decorator usage."""
    processor = DataProcessor([1, 2, 3, 4, 5])
    
    # 1. cached property decorator
    print("1. testing cached property decorator:")
    print("first access:", processor.processed_data)
    print("second access:", processor.processed_data)  # uses cached value
    
    # 2. synchronized decorator
    print("\n2. testing synchronized decorator:")
    await processor.update_data([6, 7, 8, 9, 10])
    print("updated data:", processor.data)
    
    # 3. requires attributes decorator
    print("\n3. testing requires attributes decorator:")
    try:
        valid = processor.validate_data()
        print("data is valid:", valid)
        
        # remove required attribute
        delattr(processor, 'data')
        valid = processor.validate_data()  # should raise AttributeError
    except AttributeError as e:
        print("validation error:", str(e))
    
    # 4. async retry decorator
    print("\n4. testing async retry decorator:")
    try:
        result = await processor.fetch_data()
        print("fetched data:", result)
    except ConnectionError as e:
        print("fetch error:", str(e))
    
    # 5. method timeout decorator
    print("\n5. testing method timeout decorator:")
    try:
        await processor.slow_process()
    except TimeoutError as e:
        print("timeout error:", str(e))

if __name__ == "__main__":
    asyncio.run(main())

# practice exercises:
# 1. create a method decorator that:
#    - implements method chaining
#    - validates return values
#    - supports method composition
#    - handles method dependencies

# 2. create a method decorator that:
#    - implements memoization
#    - supports cache invalidation
#    - handles cache size limits
#    - manages cache cleanup

# 3. create a method decorator that:
#    - implements aspect-oriented programming
#    - supports before/after advice
#    - handles cross-cutting concerns
#    - manages method interception 