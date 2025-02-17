# advanced context managers in python
from typing import Any, Generator, Dict, List, Optional, Type
import logging
from contextlib import contextmanager, ContextDecorator, ExitStack
import threading
import time
from datetime import datetime
import os
from abc import ABC, abstractmethod

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ContextBase(ABC):
    """abstract base class for context managers."""
    @abstractmethod
    def __enter__(self):
        """enter the context."""
        pass
    
    @abstractmethod
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """exit the context."""
        pass

class ResourcePool:
    """resource pool implementation."""
    def __init__(self, size: int, resource_factory: callable):
        self.resources = [resource_factory() for _ in range(size)]
        self.available = self.resources.copy()
        self._lock = threading.Lock()
    
    def acquire(self) -> Any:
        """acquire a resource."""
        with self._lock:
            if not self.available:
                raise RuntimeError("no resources available")
            return self.available.pop()
    
    def release(self, resource: Any) -> None:
        """release a resource."""
        with self._lock:
            self.available.append(resource)

class ResourceManager(ContextBase):
    """context manager for resource pool."""
    def __init__(self, pool: ResourcePool):
        self.pool = pool
        self.resource = None
    
    def __enter__(self):
        """acquire resource."""
        self.resource = self.pool.acquire()
        return self.resource
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """release resource."""
        if self.resource:
            self.pool.release(self.resource)
        return False

class MultiContext(ContextBase):
    """context manager for multiple contexts."""
    def __init__(self, *contexts: ContextBase):
        self.contexts = contexts
        self.stack = ExitStack()
    
    def __enter__(self):
        """enter all contexts."""
        return tuple(
            self.stack.enter_context(context)
            for context in self.contexts
        )
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """exit all contexts."""
        return self.stack.__exit__(exc_type, exc_val, exc_tb)

class RetryContext(ContextDecorator):
    """context manager with retry logic."""
    def __init__(
        self,
        retries: int = 3,
        delay: float = 1.0,
        exceptions: tuple = (Exception,)
    ):
        self.retries = retries
        self.delay = delay
        self.exceptions = exceptions
    
    def __enter__(self):
        """enter the context."""
        self.attempts = 0
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """handle retries on exception."""
        if exc_type is None:
            return False
        
        if not issubclass(exc_type, self.exceptions):
            return False
        
        self.attempts += 1
        if self.attempts >= self.retries:
            return False
        
        time.sleep(self.delay)
        return True

class EnvironmentContext(ContextBase):
    """context manager for environment variables."""
    def __init__(self, **kwargs: str):
        self.env_vars = kwargs
        self.previous = {}
    
    def __enter__(self):
        """set environment variables."""
        for key, value in self.env_vars.items():
            self.previous[key] = os.environ.get(key)
            os.environ[key] = value
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """restore environment variables."""
        for key, value in self.previous.items():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value
        return False

class Measurement:
    """class to store measurements."""
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.start_memory = None
        self.end_memory = None
    
    @property
    def duration(self) -> float:
        """calculate duration."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    @property
    def memory_usage(self) -> int:
        """calculate memory usage."""
        if self.start_memory and self.end_memory:
            return self.end_memory - self.start_memory
        return 0

class MeasureBlock(ContextBase):
    """context manager for measuring performance."""
    def __init__(self, name: str):
        self.name = name
        self.measurement = Measurement()
    
    def __enter__(self):
        """start measurements."""
        import psutil
        process = psutil.Process()
        
        self.measurement.start_time = time.time()
        self.measurement.start_memory = process.memory_info().rss
        return self.measurement
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """end measurements."""
        import psutil
        process = psutil.Process()
        
        self.measurement.end_time = time.time()
        self.measurement.end_memory = process.memory_info().rss
        
        logging.info(
            f"{self.name} - duration: {self.measurement.duration:.4f}s, "
            f"memory: {self.measurement.memory_usage / 1024 / 1024:.2f}MB"
        )
        return False

def main():
    """demonstrate advanced context manager usage."""
    # 1. resource pool
    print("1. testing resource pool:")
    pool = ResourcePool(2, lambda: "resource")
    
    with ResourceManager(pool) as r1:
        print(f"acquired resource: {r1}")
        with ResourceManager(pool) as r2:
            print(f"acquired resource: {r2}")
            try:
                with ResourceManager(pool) as r3:
                    print("this should not happen")
            except RuntimeError as e:
                print(f"expected error: {e}")
    
    # 2. multiple contexts
    print("\n2. testing multiple contexts:")
    with MultiContext(
        ResourceManager(pool),
        Timer()
    ) as (resource, timer):
        print(f"using resource: {resource}")
        time.sleep(0.1)
    
    # 3. retry context
    print("\n3. testing retry context:")
    attempt = 0
    
    @RetryContext(retries=3, delay=0.1)
    def unstable_operation():
        nonlocal attempt
        attempt += 1
        if attempt < 3:
            raise ValueError("temporary error")
        return "success"
    
    result = unstable_operation()
    print(f"operation result: {result}")
    
    # 4. environment context
    print("\n4. testing environment context:")
    with EnvironmentContext(TEST_VAR="test_value"):
        print(f"TEST_VAR: {os.environ.get('TEST_VAR')}")
    print(f"TEST_VAR after: {os.environ.get('TEST_VAR')}")
    
    # 5. measurement context
    print("\n5. testing measurement context:")
    with MeasureBlock("test_block") as measurement:
        # allocate some memory
        data = [0] * 1000000
        time.sleep(0.1)
    
    print(
        f"measurements - duration: {measurement.duration:.4f}s, "
        f"memory: {measurement.memory_usage / 1024 / 1024:.2f}MB"
    )

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create an advanced context manager that:
#    - implements dependency injection container
#    - manages object lifecycle
#    - handles circular dependencies
#    - supports scoped instances

# 2. create an advanced context manager that:
#    - implements distributed lock
#    - handles network failures
#    - supports lease renewal
#    - manages cleanup

# 3. create an advanced context manager that:
#    - implements configuration management
#    - supports hierarchical configs
#    - handles hot reloading
#    - manages validation 