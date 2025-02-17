import asyncio
from typing import Any, List, Dict, Optional, TypeVar, Generic
from dataclasses import dataclass
from datetime import datetime
import random
import logging
from contextlib import asynccontextmanager

# welcome to advanced async patterns! here we'll explore more complex scenarios
# and learn how to handle errors, timeouts, and cancellations properly :D

# configure logging for better visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# custom exceptions for our examples
class TaskTimeoutError(Exception):
    """raised when a task times out"""
    pass

class RetryExhaustedError(Exception):
    """raised when all retry attempts fail"""
    pass

# type variable for our generic retry decorator
T = TypeVar('T')

# helper to retry async operations with exponential backoff
async def retry_with_backoff(
    operation: callable,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    exponential_base: float = 2.0
) -> Any:
    # keep track of attempts and last error
    last_error = None
    
    for attempt in range(max_attempts):
        try:
            # try the operation
            return await operation()
        except Exception as e:
            last_error = e
            
            # calculate delay with exponential backoff
            delay = min(
                base_delay * (exponential_base ** attempt),
                max_delay
            )
            
            # log the retry attempt
            logging.warning(
                f"attempt {attempt + 1}/{max_attempts} failed: {str(e)}, "
                f"retrying in {delay:.2f}s"
            )
            
            # wait before retrying
            await asyncio.sleep(delay)
    
    # if we get here, all attempts failed
    raise RetryExhaustedError(f"operation failed after {max_attempts} attempts") from last_error

# advanced pattern: task with timeout and cleanup
@asynccontextmanager
async def managed_task(timeout: float):
    # create a task group for cleanup
    async with asyncio.TaskGroup() as tg:
        try:
            # start the timeout timer
            timer_task = tg.create_task(asyncio.sleep(timeout))
            yield tg
        except* Exception as exc:
            # handle any exceptions
            logging.error(f"task failed: {exc}")
            raise
        finally:
            # ensure timer is cancelled
            timer_task.cancel()

# example: rate limiter for async operations
class RateLimiter:
    def __init__(self, rate_limit: int, time_window: float = 1.0):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.tokens = rate_limit
        self.last_update = asyncio.get_event_loop().time()
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        async with self._lock:
            now = asyncio.get_event_loop().time()
            
            # replenish tokens based on time passed
            time_passed = now - self.last_update
            self.tokens = min(
                self.rate_limit,
                self.tokens + int(time_passed / self.time_window * self.rate_limit)
            )
            
            if self.tokens <= 0:
                # wait for next token
                await asyncio.sleep(self.time_window / self.rate_limit)
                self.tokens = 1
            
            self.tokens -= 1
            self.last_update = now

# example: priority queue for async tasks
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    data: Any

class PriorityTaskQueue:
    def __init__(self):
        self.queue = asyncio.PriorityQueue()
    
    async def put(self, item: Any, priority: int = 0):
        await self.queue.put(PrioritizedItem(priority, item))
    
    async def get(self) -> Any:
        item = await self.queue.get()
        return item.data

# example: circuit breaker pattern
class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        reset_timeout: float = 60.0
    ):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure = 0
        self.state = "closed"  # closed, open, half-open
        self._lock = asyncio.Lock()
    
    async def __call__(self, func: callable) -> Any:
        async with self._lock:
            now = asyncio.get_event_loop().time()
            
            # check if we should reset
            if (
                self.state == "open"
                and now - self.last_failure > self.reset_timeout
            ):
                self.state = "half-open"
            
            # if circuit is open, fail fast
            if self.state == "open":
                raise Exception("circuit breaker is open")
            
            try:
                result = await func()
                
                # success in half-open state closes the circuit
                if self.state == "half-open":
                    self.state = "closed"
                    self.failures = 0
                
                return result
            except Exception as e:
                self.failures += 1
                self.last_failure = now
                
                # check if we should open the circuit
                if self.failures >= self.failure_threshold:
                    self.state = "open"
                
                raise

# now let's see these patterns in action
async def example_with_patterns():
    # example 1: retry with backoff
    async def unreliable_operation():
        if random.random() < 0.7:  # 70% chance of failure
            raise ConnectionError("network error")
        return "success!"
    
    try:
        result = await retry_with_backoff(
            unreliable_operation,
            max_attempts=3
        )
        logging.info(f"retry result: {result}")
    except RetryExhaustedError as e:
        logging.error(f"retry failed: {e}")
    
    # example 2: rate limited operations
    limiter = RateLimiter(rate_limit=2)  # 2 operations per second
    
    async def rate_limited_task(name: str):
        await limiter.acquire()
        logging.info(f"executing {name}")
        await asyncio.sleep(0.1)
    
    # run multiple tasks with rate limiting
    tasks = [
        rate_limited_task(f"task{i}")
        for i in range(5)
    ]
    await asyncio.gather(*tasks)
    
    # example 3: priority queue
    queue = PriorityTaskQueue()
    
    # add tasks with different priorities
    await queue.put("low priority task", 3)
    await queue.put("high priority task", 1)
    await queue.put("medium priority task", 2)
    
    # process tasks in priority order
    for _ in range(3):
        task = await queue.get()
        logging.info(f"processing: {task}")
    
    # example 4: circuit breaker
    breaker = CircuitBreaker(failure_threshold=2)
    
    async def fragile_operation():
        if random.random() < 0.8:  # 80% chance of failure
            raise ConnectionError("service unavailable")
        return "success!"
    
    # try operations with circuit breaker
    for _ in range(5):
        try:
            result = await breaker(fragile_operation)
            logging.info(f"circuit breaker result: {result}")
        except Exception as e:
            logging.error(f"circuit breaker error: {e}")
        await asyncio.sleep(0.1)

async def main():
    # run our examples with proper error handling
    try:
        async with managed_task(timeout=10) as tg:
            await tg.create_task(example_with_patterns())
    except TimeoutError:
        logging.error("operation timed out")
    except Exception as e:
        logging.error(f"unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

# practice exercises:
# 1. implement an async resource pool that:
#    - manages a fixed number of resources
#    - handles timeouts for resource acquisition
#    - implements fair scheduling

# 2. create an async task scheduler that:
#    - supports task dependencies
#    - handles task cancellation
#    - provides progress monitoring

# 3. implement an async cache that:
#    - supports time-based expiration
#    - handles concurrent access
#    - implements cache eviction strategies 