import sys
import gc
import weakref
from typing import Any, Dict, List, Optional
import psutil
import os
import time
import logging
from dataclasses import dataclass
from contextlib import contextmanager
import tracemalloc

# welcome to memory management in python! here we'll learn how to:
# 1. track memory usage
# 2. find and fix memory leaks
# 3. optimize memory usage
# 4. use weak references
# 5. understand garbage collection

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# example 1: memory tracking context manager
@contextmanager
def track_memory_usage(name: str = "operation"):
    # start tracking memory
    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss / 1024 / 1024  # MB
    
    # start tracemalloc for detailed tracking
    tracemalloc.start()
    start_time = time.time()
    
    try:
        yield
    finally:
        # get memory stats
        current, peak = tracemalloc.get_traced_memory()
        duration = time.time() - start_time
        end_mem = process.memory_info().rss / 1024 / 1024
        
        # log memory usage
        logging.info(f"{name} memory usage:")
        logging.info(f"duration: {duration:.2f}s")
        logging.info(f"current memory: {current / 1024 / 1024:.2f} MB")
        logging.info(f"peak memory: {peak / 1024 / 1024:.2f} MB")
        logging.info(f"memory change: {end_mem - start_mem:.2f} MB")
        
        # get top 3 memory snapshots
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        logging.info("top 3 memory allocations:")
        for stat in top_stats[:3]:
            logging.info(stat)
        
        tracemalloc.stop()

# example 2: memory-efficient data structures
class MemoryEfficientList:
    def __init__(self, max_size: int = 1000):
        self._data = []
        self._max_size = max_size
        self._current_size = 0
    
    def append(self, item: Any) -> None:
        if self._current_size >= self._max_size:
            # implement circular buffer behavior
            self._data[self._current_size % self._max_size] = item
        else:
            self._data.append(item)
            self._current_size += 1
    
    def __len__(self) -> int:
        return self._current_size
    
    def __getitem__(self, index: int) -> Any:
        if not 0 <= index < self._current_size:
            raise IndexError("list index out of range")
        return self._data[index]

# example 3: weak references to prevent memory leaks
class Cache:
    def __init__(self):
        # use weak references for values
        self._cache: Dict[str, weakref.ref] = {}
    
    def set(self, key: str, value: Any) -> None:
        # store weak reference
        self._cache[key] = weakref.ref(value)
    
    def get(self, key: str) -> Optional[Any]:
        # get value from weak reference
        if key in self._cache:
            value = self._cache[key]()
            if value is not None:
                return value
            # clean up dead reference
            del self._cache[key]
        return None

# example 4: object pooling for memory reuse
class ObjectPool:
    def __init__(self, factory: callable, initial_size: int = 5):
        self._factory = factory
        self._pool: List[Any] = []
        self._in_use: Dict[int, Any] = {}
        
        # create initial objects
        for _ in range(initial_size):
            self._pool.append(factory())
    
    def acquire(self) -> Any:
        if not self._pool:
            # create new object if pool is empty
            obj = self._factory()
        else:
            # reuse existing object
            obj = self._pool.pop()
        
        # track object usage
        self._in_use[id(obj)] = obj
        return obj
    
    def release(self, obj: Any) -> None:
        obj_id = id(obj)
        if obj_id in self._in_use:
            # return object to pool
            del self._in_use[obj_id]
            self._pool.append(obj)

# example 5: memory-efficient data processing
def process_large_file(
    filename: str,
    chunk_size: int = 1024
) -> int:
    total = 0
    with open(filename, 'r') as f:
        while True:
            # process file in chunks to save memory
            chunk = f.read(chunk_size)
            if not chunk:
                break
            # process chunk
            total += len(chunk.split())
    return total

def main():
    # example 1: track memory usage
    with track_memory_usage("list creation"):
        # create a large list
        large_list = list(range(1000000))
        time.sleep(0.1)  # simulate work
    
    # example 2: memory-efficient list
    efficient_list = MemoryEfficientList(max_size=1000)
    with track_memory_usage("efficient list"):
        for i in range(2000):
            efficient_list.append(i)
    
    # example 3: weak references
    cache = Cache()
    
    class LargeObject:
        def __init__(self, data: List[int]):
            self.data = data
    
    # create and cache large object
    obj = LargeObject(list(range(1000000)))
    cache.set("large_obj", obj)
    
    # object is still accessible
    cached_obj = cache.get("large_obj")
    logging.info(f"cached object exists: {cached_obj is not None}")
    
    # remove reference to original object
    del obj
    
    # force garbage collection
    gc.collect()
    
    # object should be gone
    cached_obj = cache.get("large_obj")
    logging.info(f"cached object exists after gc: {cached_obj is not None}")
    
    # example 4: object pooling
    @dataclass
    class ExpensiveObject:
        data: List[int]
    
    def create_expensive_object():
        return ExpensiveObject(list(range(1000)))
    
    pool = ObjectPool(create_expensive_object, initial_size=2)
    
    with track_memory_usage("object pool"):
        # use objects from pool
        obj1 = pool.acquire()
        obj2 = pool.acquire()
        
        # release objects back to pool
        pool.release(obj1)
        pool.release(obj2)
        
        # reuse objects
        obj3 = pool.acquire()
        obj4 = pool.acquire()
    
    # example 5: efficient file processing
    with open("test.txt", "w") as f:
        f.write("hello world " * 1000)
    
    with track_memory_usage("file processing"):
        word_count = process_large_file("test.txt")
        logging.info(f"word count: {word_count}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. implement a memory profiler that:
#    - tracks memory usage over time
#    - identifies memory leaks
#    - generates memory usage reports

# 2. create a memory-efficient cache that:
#    - implements LRU eviction
#    - uses weak references
#    - handles size limits

# 3. implement a memory pool that:
#    - supports different object types
#    - handles concurrent access
#    - implements cleanup strategies 