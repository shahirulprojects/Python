# error handling in concurrent programming
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future
from queue import Queue, Empty
from typing import Any, List, Dict, Optional, Callable, TypeVar
import time
import logging
import traceback
from dataclasses import dataclass
from contextlib import contextmanager

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(threadName)s - %(levelname)s - %(message)s'
)

T = TypeVar('T')

class ConcurrencyError(Exception):
    """base class for concurrency-related errors."""
    pass

class ThreadError(ConcurrencyError):
    """error in thread execution."""
    
    def __init__(self, thread_name: str, original_error: Exception):
        self.thread_name = thread_name
        self.original_error = original_error
        super().__init__(f"error in thread '{thread_name}': {str(original_error)}")

class ProcessError(ConcurrencyError):
    """error in process execution."""
    
    def __init__(self, process_name: str, original_error: Exception):
        self.process_name = process_name
        self.original_error = original_error
        super().__init__(f"error in process '{process_name}': {str(original_error)}")

@dataclass
class TaskResult:
    """container for task execution results."""
    success: bool
    result: Optional[Any] = None
    error: Optional[Exception] = None
    traceback: Optional[str] = None

class ThreadSafeCounter:
    """thread-safe counter implementation."""
    
    def __init__(self, initial: int = 0):
        self._value = initial
        self._lock = threading.Lock()
    
    def increment(self) -> int:
        """increment counter in thread-safe way."""
        with self._lock:
            self._value += 1
            return self._value
    
    def decrement(self) -> int:
        """decrement counter in thread-safe way."""
        with self._lock:
            self._value -= 1
            return self._value
    
    @property
    def value(self) -> int:
        """get current value."""
        with self._lock:
            return self._value

class WorkerPool:
    """pool of workers with error handling."""
    
    def __init__(self, num_workers: int, use_processes: bool = False):
        self.num_workers = num_workers
        self.use_processes = use_processes
        self.executor = (ProcessPoolExecutor if use_processes else ThreadPoolExecutor)(
            max_workers=num_workers
        )
        self.futures: List[Future] = []
    
    def submit(self, func: Callable, *args, **kwargs) -> Future:
        """submit task to pool."""
        future = self.executor.submit(func, *args, **kwargs)
        self.futures.append(future)
        return future
    
    def wait_all(self) -> List[TaskResult]:
        """wait for all tasks to complete."""
        results = []
        for future in self.futures:
            try:
                result = future.result()
                results.append(TaskResult(True, result=result))
            except Exception as e:
                results.append(TaskResult(
                    False,
                    error=e,
                    traceback=traceback.format_exc()
                ))
        return results
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.executor.shutdown(wait=True)

@contextmanager
def thread_error_handler(thread_name: str):
    """context manager for handling thread errors."""
    try:
        yield
    except Exception as e:
        logging.error(f"error in thread {thread_name}: {str(e)}")
        raise ThreadError(thread_name, e)

def run_in_thread(func: Callable[..., T], *args, **kwargs) -> T:
    """run function in thread with error handling."""
    result_queue: Queue = Queue()
    
    def worker():
        try:
            result = func(*args, **kwargs)
            result_queue.put(('success', result))
        except Exception as e:
            result_queue.put(('error', e))
    
    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()
    
    status, value = result_queue.get()
    if status == 'error':
        raise ThreadError(thread.name, value)
    return value

def parallel_map(func: Callable, items: List[Any], 
                num_workers: int = None, 
                use_processes: bool = False) -> List[TaskResult]:
    """map function over items in parallel with error handling."""
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()
    
    with WorkerPool(num_workers, use_processes) as pool:
        for item in items:
            pool.submit(func, item)
        return pool.wait_all()

class SafeQueue:
    """thread-safe queue with timeout and error handling."""
    
    def __init__(self, maxsize: int = 0):
        self.queue = Queue(maxsize)
        self.active = True
    
    def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        """put item in queue with timeout."""
        try:
            self.queue.put(item, timeout=timeout)
            return True
        except Exception as e:
            logging.error(f"error putting item in queue: {str(e)}")
            return False
    
    def get(self, timeout: Optional[float] = None) -> Optional[Any]:
        """get item from queue with timeout."""
        try:
            return self.queue.get(timeout=timeout)
        except Empty:
            return None
        except Exception as e:
            logging.error(f"error getting item from queue: {str(e)}")
            return None
    
    def close(self):
        """mark queue as inactive."""
        self.active = False

# example usage
def main():
    """demonstrate concurrent error handling."""
    # 1. thread-safe counter
    print("1. testing thread-safe counter:")
    counter = ThreadSafeCounter()
    
    def increment_counter():
        with thread_error_handler("counter_thread"):
            for _ in range(1000):
                counter.increment()
    
    threads = [
        threading.Thread(target=increment_counter)
        for _ in range(5)
    ]
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    print(f"final counter value: {counter.value}")
    
    # 2. parallel processing with error handling
    print("\n2. testing parallel processing:")
    def process_item(x: int) -> int:
        if x == 3:
            raise ValueError("invalid value")
        return x * x
    
    items = list(range(5))
    results = parallel_map(process_item, items)
    
    for item, result in zip(items, results):
        if result.success:
            print(f"item {item} -> {result.result}")
        else:
            print(f"item {item} failed: {result.error}")
    
    # 3. thread pool with error handling
    print("\n3. testing thread pool:")
    def risky_operation(x: int) -> int:
        if x % 2 == 0:
            raise ValueError(f"even number not allowed: {x}")
        return x * 2
    
    with WorkerPool(3) as pool:
        for i in range(5):
            pool.submit(risky_operation, i)
        
        results = pool.wait_all()
        for i, result in enumerate(results):
            if result.success:
                print(f"task {i} succeeded: {result.result}")
            else:
                print(f"task {i} failed: {result.error}")
    
    # 4. safe queue usage
    print("\n4. testing safe queue:")
    queue = SafeQueue(maxsize=2)
    
    def producer():
        for i in range(5):
            if not queue.put(i, timeout=1):
                print(f"failed to put item {i}")
            time.sleep(0.1)
        queue.close()
    
    def consumer():
        while queue.active:
            item = queue.get(timeout=0.5)
            if item is not None:
                print(f"processed item: {item}")
    
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a thread pool that:
#    - handles worker crashes
#    - implements task priorities
#    - provides progress updates
#    - supports task cancellation

# 2. create a producer-consumer system that:
#    - handles multiple producers
#    - handles multiple consumers
#    - implements backpressure
#    - recovers from failures

# 3. create a distributed task processor that:
#    - handles network failures
#    - manages worker lifecycle
#    - provides task monitoring
#    - implements fault tolerance 
 