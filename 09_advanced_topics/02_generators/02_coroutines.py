# coroutines in python
from typing import Generator, Any, Optional, Dict, List
import logging
from functools import wraps
import asyncio
from datetime import datetime

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def coroutine(func: callable) -> callable:
    """decorator to automatically prime coroutines."""
    @wraps(func)
    def primer(*args: Any, **kwargs: Any) -> Generator:
        gen = func(*args, **kwargs)
        next(gen)  # prime the generator
        return gen
    return primer

@coroutine
def logger() -> Generator[None, Any, None]:
    """coroutine to log received values."""
    while True:
        value = yield
        logging.info(f"received: {value}")

@coroutine
def filter_values(
    predicate: callable,
    target: Generator
) -> Generator[None, Any, None]:
    """coroutine to filter values."""
    while True:
        value = yield
        if predicate(value):
            target.send(value)

@coroutine
def multiplier(
    factor: float,
    target: Generator
) -> Generator[None, float, None]:
    """coroutine to multiply values."""
    while True:
        value = yield
        target.send(value * factor)

@coroutine
def averager() -> Generator[float, float, None]:
    """coroutine to compute running average."""
    total = 0.0
    count = 0
    average = 0.0
    
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

@coroutine
def broadcast(*targets: Generator) -> Generator[None, Any, None]:
    """coroutine to broadcast values to multiple targets."""
    while True:
        value = yield
        for target in targets:
            target.send(value)

@coroutine
def collect(n: int) -> Generator[List[Any], Any, None]:
    """coroutine to collect n values."""
    values: List[Any] = []
    while True:
        if len(values) >= n:
            values = []
        value = yield values
        values.append(value)

@coroutine
def window(size: int, target: Generator) -> Generator[None, Any, None]:
    """coroutine to maintain sliding window."""
    window: List[Any] = []
    while True:
        value = yield
        window.append(value)
        if len(window) >= size:
            target.send(window)
            window = window[1:]

class Pipeline:
    """class to manage pipeline of coroutines."""
    def __init__(self, *coroutines: Generator):
        self.coroutines = coroutines
    
    def send(self, value: Any) -> None:
        """send value through pipeline."""
        for coroutine in self.coroutines:
            coroutine.send(value)
    
    def close(self) -> None:
        """close all coroutines."""
        for coroutine in self.coroutines:
            coroutine.close()

async def async_producer(
    queue: asyncio.Queue,
    values: List[Any]
) -> None:
    """async producer function."""
    for value in values:
        await queue.put(value)
        await asyncio.sleep(0.1)  # simulate work
    await queue.put(None)  # sentinel value

async def async_consumer(queue: asyncio.Queue) -> None:
    """async consumer function."""
    while True:
        value = await queue.get()
        if value is None:  # check for sentinel
            break
        logging.info(f"consumed: {value}")
        queue.task_done()

def main():
    """demonstrate coroutine usage."""
    # 1. basic logger coroutine
    print("1. testing logger coroutine:")
    log = logger()
    log.send("test message")
    log.send("another message")
    
    # 2. filter and logger pipeline
    print("\n2. testing filter pipeline:")
    log = logger()
    filt = filter_values(lambda x: x > 0, log)
    for i in range(-2, 3):
        filt.send(i)
    
    # 3. multiplier and logger pipeline
    print("\n3. testing multiplier pipeline:")
    log = logger()
    mult = multiplier(2.0, log)
    for i in range(3):
        mult.send(i)
    
    # 4. averager coroutine
    print("\n4. testing averager coroutine:")
    avg = averager()
    for i in range(1, 4):
        result = avg.send(i)
        print(f"current average: {result}")
    
    # 5. broadcast to multiple targets
    print("\n5. testing broadcast:")
    log1 = logger()
    log2 = logger()
    broad = broadcast(log1, log2)
    broad.send("broadcast message")
    
    # 6. collector coroutine
    print("\n6. testing collector:")
    collect_values = collect(3)
    for i in range(5):
        result = collect_values.send(i)
        print(f"collected values: {result}")
    
    # 7. window and logger pipeline
    print("\n7. testing window:")
    log = logger()
    win = window(3, log)
    for i in range(5):
        win.send(i)
    
    # 8. pipeline class
    print("\n8. testing pipeline:")
    log = logger()
    filt = filter_values(lambda x: x > 0, log)
    mult = multiplier(2.0, log)
    pipeline = Pipeline(filt, mult)
    
    for i in range(-2, 3):
        pipeline.send(i)
    pipeline.close()
    
    # 9. async producer-consumer
    print("\n9. testing async producer-consumer:")
    async def run_async():
        queue = asyncio.Queue()
        values = list(range(5))
        
        # create producer and consumer tasks
        producer = asyncio.create_task(async_producer(queue, values))
        consumer = asyncio.create_task(async_consumer(queue))
        
        # wait for both tasks
        await asyncio.gather(producer, consumer)
    
    asyncio.run(run_async())

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a coroutine that:
#    - implements rate limiting
#    - manages token bucket
#    - handles bursts
#    - supports dynamic rates

# 2. create a coroutine that:
#    - implements pub/sub pattern
#    - manages subscriptions
#    - handles message routing
#    - supports wildcards

# 3. create a coroutine that:
#    - implements backpressure
#    - manages buffer size
#    - handles overflow
#    - supports flow control