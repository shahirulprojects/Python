# basic function caching in python
from typing import Any, Dict, Callable, TypeVar, cast
import logging
import time
from datetime import datetime
from functools import lru_cache, wraps

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# type variables for better type hints
F = TypeVar('F', bound=Callable[..., Any])

def simple_cache(func: F) -> F:
    """simple function cache using dictionary."""
    cache: Dict[str, Any] = {}
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # create cache key
        key = str(args) + str(sorted(kwargs.items()))
        
        # check cache
        if key in cache:
            logging.info(f"cache hit for {func.__name__}")
            return cache[key]
        
        # compute and cache result
        result = func(*args, **kwargs)
        cache[key] = result
        logging.info(f"cache miss for {func.__name__}")
        return result
    
    return cast(F, wrapper)

def timed_cache(seconds: int) -> Callable[[F], F]:
    """cache with timeout."""
    def decorator(func: F) -> F:
        cache: Dict[str, tuple] = {}
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # create cache key
            key = str(args) + str(sorted(kwargs.items()))
            
            # check cache
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < seconds:
                    logging.info(f"cache hit for {func.__name__}")
                    return result
            
            # compute and cache result
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            logging.info(f"cache miss for {func.__name__}")
            return result
        
        return cast(F, wrapper)
    return decorator

def size_limited_cache(maxsize: int) -> Callable[[F], F]:
    """cache with size limit."""
    def decorator(func: F) -> F:
        cache: Dict[str, Any] = {}
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # create cache key
            key = str(args) + str(sorted(kwargs.items()))
            
            # check cache
            if key in cache:
                logging.info(f"cache hit for {func.__name__}")
                return cache[key]
            
            # compute result
            result = func(*args, **kwargs)
            
            # manage cache size
            if len(cache) >= maxsize:
                # remove oldest entry
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            # cache result
            cache[key] = result
            logging.info(f"cache miss for {func.__name__}")
            return result
        
        return cast(F, wrapper)
    return decorator

@lru_cache(maxsize=None)
def fibonacci_lru(n: int) -> int:
    """compute fibonacci number using lru_cache."""
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

@simple_cache
def factorial(n: int) -> int:
    """compute factorial using simple cache."""
    if n < 2:
        return 1
    return n * factorial(n - 1)

@timed_cache(seconds=5)
def slow_operation(x: int) -> int:
    """simulate slow operation with timed cache."""
    time.sleep(1)  # simulate work
    return x * x

@size_limited_cache(maxsize=2)
def limited_operation(x: int) -> int:
    """operation with size-limited cache."""
    time.sleep(0.1)  # simulate work
    return x * x

def measure_time(func: Callable[..., Any], *args: Any) -> float:
    """measure function execution time."""
    start = time.time()
    func(*args)
    return time.time() - start

def main():
    """demonstrate function caching."""
    # 1. lru_cache
    print("1. testing lru_cache:")
    n = 35
    time_without_cache = measure_time(
        lambda: sum(fibonacci_lru(i) for i in range(n))
    )
    time_with_cache = measure_time(
        lambda: sum(fibonacci_lru(i) for i in range(n))
    )
    
    print(f"time without cache: {time_without_cache:.4f} seconds")
    print(f"time with cache: {time_with_cache:.4f} seconds")
    print(f"speedup: {time_without_cache / time_with_cache:.2f}x")
    
    # 2. simple cache
    print("\n2. testing simple cache:")
    for i in range(5):
        result = factorial(10)
        print(f"factorial(10) = {result}")
    
    # 3. timed cache
    print("\n3. testing timed cache:")
    # first call
    result1 = slow_operation(5)
    print(f"first call result: {result1}")
    
    # second call (cached)
    result2 = slow_operation(5)
    print(f"second call result: {result2}")
    
    # wait for cache to expire
    print("waiting for cache to expire...")
    time.sleep(6)
    
    # third call (cache expired)
    result3 = slow_operation(5)
    print(f"third call result: {result3}")
    
    # 4. size-limited cache
    print("\n4. testing size-limited cache:")
    # first two calls
    result1 = limited_operation(1)
    print(f"first call result: {result1}")
    result2 = limited_operation(2)
    print(f"second call result: {result2}")
    
    # third call (exceeds cache size)
    result3 = limited_operation(3)
    print(f"third call result: {result3}")
    
    # try to access first result (should be evicted)
    result4 = limited_operation(1)
    print(f"fourth call result: {result4}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a cache decorator that:
#    - implements least recently used (LRU) policy
#    - handles cache eviction
#    - supports cache statistics
#    - manages memory usage

# 2. create a cache decorator that:
#    - implements least frequently used (LFU) policy
#    - tracks access frequency
#    - supports cache warming
#    - handles cache cleanup

# 3. create a cache decorator that:
#    - implements distributed caching
#    - handles cache synchronization
#    - supports cache invalidation
#    - manages cache consistency 