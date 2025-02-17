# advanced function caching in python
from typing import Any, Dict, List, Callable, TypeVar, cast, Optional
import logging
import time
from datetime import datetime
from functools import wraps
from collections import OrderedDict, defaultdict
import threading
import weakref

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# type variables for better type hints
F = TypeVar('F', bound=Callable[..., Any])

class CacheStats:
    """class to track cache statistics."""
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    @property
    def total(self) -> int:
        """total number of cache accesses."""
        return self.hits + self.misses
    
    @property
    def hit_rate(self) -> float:
        """cache hit rate."""
        if self.total == 0:
            return 0.0
        return self.hits / self.total
    
    def __str__(self) -> str:
        return (
            f"hits: {self.hits}, misses: {self.misses}, "
            f"evictions: {self.evictions}, hit rate: {self.hit_rate:.2%}"
        )

class LRUCache:
    """least recently used cache implementation."""
    def __init__(self, maxsize: int):
        self.maxsize = maxsize
        self.cache = OrderedDict()
        self.stats = CacheStats()
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """get item from cache."""
        with self._lock:
            if key in self.cache:
                self.stats.hits += 1
                self.cache.move_to_end(key)
                return self.cache[key]
            self.stats.misses += 1
            return None
    
    def put(self, key: str, value: Any) -> None:
        """put item in cache."""
        with self._lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            else:
                if len(self.cache) >= self.maxsize:
                    self.cache.popitem(last=False)
                    self.stats.evictions += 1
            self.cache[key] = value

class LFUCache:
    """least frequently used cache implementation."""
    def __init__(self, maxsize: int):
        self.maxsize = maxsize
        self.cache: Dict[str, Any] = {}
        self.frequencies = defaultdict(set)
        self.counts: Dict[str, int] = {}
        self.min_freq = 0
        self.stats = CacheStats()
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """get item from cache."""
        with self._lock:
            if key in self.cache:
                self.stats.hits += 1
                self._increment_frequency(key)
                return self.cache[key]
            self.stats.misses += 1
            return None
    
    def put(self, key: str, value: Any) -> None:
        """put item in cache."""
        with self._lock:
            if key in self.cache:
                self.cache[key] = value
                self._increment_frequency(key)
            else:
                if len(self.cache) >= self.maxsize:
                    self._evict()
                self.cache[key] = value
                self.counts[key] = 1
                self.frequencies[1].add(key)
                self.min_freq = 1
    
    def _increment_frequency(self, key: str) -> None:
        """increment frequency of key."""
        freq = self.counts[key]
        self.frequencies[freq].remove(key)
        
        if not self.frequencies[freq] and freq == self.min_freq:
            self.min_freq += 1
        
        self.counts[key] = freq + 1
        self.frequencies[freq + 1].add(key)
    
    def _evict(self) -> None:
        """evict least frequently used item."""
        key = self.frequencies[self.min_freq].pop()
        del self.cache[key]
        del self.counts[key]
        self.stats.evictions += 1

def memoize_with_ttl(
    ttl: int,
    maxsize: Optional[int] = None
) -> Callable[[F], F]:
    """memoize function with time-to-live."""
    def decorator(func: F) -> F:
        cache: Dict[str, tuple] = {}
        stats = CacheStats()
        lock = threading.Lock()
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = str(args) + str(sorted(kwargs.items()))
            
            with lock:
                # check cache
                if key in cache:
                    result, timestamp = cache[key]
                    if time.time() - timestamp < ttl:
                        stats.hits += 1
                        return result
                    del cache[key]
                
                # compute result
                stats.misses += 1
                result = func(*args, **kwargs)
                
                # manage cache size
                if maxsize and len(cache) >= maxsize:
                    oldest_key = next(iter(cache))
                    del cache[oldest_key]
                    stats.evictions += 1
                
                # cache result
                cache[key] = (result, time.time())
                return result
        
        # attach stats to wrapper
        wrapper.stats = stats
        return cast(F, wrapper)
    
    return decorator

class WeakCache:
    """cache using weak references."""
    def __init__(self):
        self.cache = weakref.WeakValueDictionary()
        self.stats = CacheStats()
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """get item from cache."""
        with self._lock:
            if key in self.cache:
                self.stats.hits += 1
                return self.cache[key]
            self.stats.misses += 1
            return None
    
    def put(self, key: str, value: Any) -> None:
        """put item in cache."""
        with self._lock:
            self.cache[key] = value

def async_cache(
    maxsize: Optional[int] = None
) -> Callable[[F], F]:
    """cache for async functions."""
    def decorator(func: F) -> F:
        cache = LRUCache(maxsize or 128)
        
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = str(args) + str(sorted(kwargs.items()))
            
            # check cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # compute result
            result = await func(*args, **kwargs)
            cache.put(key, result)
            return result
        
        # attach cache to wrapper
        wrapper.cache = cache
        return cast(F, wrapper)
    
    return decorator

def main():
    """demonstrate advanced caching techniques."""
    # 1. LRU cache
    print("1. testing LRU cache:")
    cache = LRUCache(maxsize=2)
    
    # add items
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # evicts "a"
    
    print(f"get 'a': {cache.get('a')}")  # None
    print(f"get 'b': {cache.get('b')}")  # 2
    print(f"get 'c': {cache.get('c')}")  # 3
    print(f"stats: {cache.stats}")
    
    # 2. LFU cache
    print("\n2. testing LFU cache:")
    cache = LFUCache(maxsize=2)
    
    # add items
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # increase frequency
    cache.put("c", 3)  # evicts "b"
    
    print(f"get 'a': {cache.get('a')}")  # 1
    print(f"get 'b': {cache.get('b')}")  # None
    print(f"get 'c': {cache.get('c')}")  # 3
    print(f"stats: {cache.stats}")
    
    # 3. memoize with TTL
    print("\n3. testing memoize with TTL:")
    @memoize_with_ttl(ttl=2, maxsize=2)
    def slow_function(x: int) -> int:
        time.sleep(0.1)  # simulate work
        return x * x
    
    # first call
    result1 = slow_function(5)
    print(f"first call result: {result1}")
    
    # second call (cached)
    result2 = slow_function(5)
    print(f"second call result: {result2}")
    
    # wait for TTL to expire
    print("waiting for TTL to expire...")
    time.sleep(3)
    
    # third call (cache expired)
    result3 = slow_function(5)
    print(f"third call result: {result3}")
    print(f"stats: {slow_function.stats}")
    
    # 4. weak cache
    print("\n4. testing weak cache:")
    cache = WeakCache()
    
    class Data:
        def __init__(self, value: int):
            self.value = value
    
    # add items
    data = Data(42)
    cache.put("data", data)
    print(f"get 'data': {cache.get('data').value}")
    
    # remove reference
    del data
    print(f"get 'data' after deletion: {cache.get('data')}")
    print(f"stats: {cache.stats}")
    
    # 5. async cache
    print("\n5. testing async cache:")
    @async_cache(maxsize=2)
    async def async_operation(x: int) -> int:
        await asyncio.sleep(0.1)  # simulate async work
        return x * x
    
    async def run_async():
        # first call
        result1 = await async_operation(5)
        print(f"first call result: {result1}")
        
        # second call (cached)
        result2 = await async_operation(5)
        print(f"second call result: {result2}")
        
        print(f"stats: {async_operation.cache.stats}")
    
    import asyncio
    asyncio.run(run_async())

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a cache implementation that:
#    - supports multiple eviction policies
#    - handles cache warming
#    - implements cache prefetching
#    - manages cache coherence

# 2. create a cache implementation that:
#    - supports distributed caching
#    - handles network failures
#    - implements cache sharding
#    - manages replication

# 3. create a cache implementation that:
#    - supports hierarchical caching
#    - implements cache levels
#    - handles cache inclusion
#    - manages cache exclusion