# basic generators in python
from typing import Generator, Iterator, List, Any
import time
import logging
from datetime import datetime

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def count_up(start: int, end: int) -> Generator[int, None, None]:
    """generate numbers from start to end."""
    current = start
    while current <= end:
        yield current
        current += 1

def fibonacci_sequence(n: int) -> Generator[int, None, None]:
    """generate fibonacci sequence up to n numbers."""
    a, b = 0, 1
    count = 0
    
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

def read_file_lazy(filename: str) -> Generator[str, None, None]:
    """read file line by line lazily."""
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()

def chunk_list(
    data: List[Any],
    chunk_size: int
) -> Generator[List[Any], None, None]:
    """split list into chunks."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def infinite_counter() -> Generator[int, None, None]:
    """generate an infinite sequence of numbers."""
    counter = 0
    while True:
        yield counter
        counter += 1

def filter_generator(
    predicate: callable,
    iterator: Iterator[Any]
) -> Generator[Any, None, None]:
    """filter items from iterator using predicate."""
    for item in iterator:
        if predicate(item):
            yield item

def map_generator(
    func: callable,
    iterator: Iterator[Any]
) -> Generator[Any, None, None]:
    """apply function to each item in iterator."""
    for item in iterator:
        yield func(item)

def chain_generators(
    *iterators: Iterator[Any]
) -> Generator[Any, None, None]:
    """chain multiple iterators together."""
    for iterator in iterators:
        yield from iterator

def timed_generator(
    iterator: Iterator[Any],
    interval: float
) -> Generator[Any, None, None]:
    """yield items with time interval."""
    for item in iterator:
        yield item
        time.sleep(interval)

def main():
    """demonstrate generator usage."""
    # 1. basic counter generator
    print("1. testing counter generator:")
    for num in count_up(1, 5):
        print(num, end=' ')
    print()
    
    # 2. fibonacci generator
    print("\n2. testing fibonacci generator:")
    for num in fibonacci_sequence(8):
        print(num, end=' ')
    print()
    
    # 3. file reading generator
    print("\n3. testing file reading generator:")
    # create a sample file
    with open('sample.txt', 'w') as f:
        f.write('line 1\nline 2\nline 3')
    
    for line in read_file_lazy('sample.txt'):
        print(line)
    
    # 4. chunk generator
    print("\n4. testing chunk generator:")
    data = list(range(10))
    for chunk in chunk_list(data, 3):
        print(chunk)
    
    # 5. infinite counter with limit
    print("\n5. testing infinite counter:")
    counter = infinite_counter()
    for _ in range(5):
        print(next(counter), end=' ')
    print()
    
    # 6. filter generator
    print("\n6. testing filter generator:")
    numbers = range(10)
    even_numbers = filter_generator(lambda x: x % 2 == 0, numbers)
    print(list(even_numbers))
    
    # 7. map generator
    print("\n7. testing map generator:")
    numbers = range(5)
    squared = map_generator(lambda x: x ** 2, numbers)
    print(list(squared))
    
    # 8. chained generators
    print("\n8. testing chained generators:")
    gen1 = (x for x in range(3))
    gen2 = (x for x in range(3, 6))
    chained = chain_generators(gen1, gen2)
    print(list(chained))
    
    # 9. timed generator
    print("\n9. testing timed generator:")
    numbers = range(3)
    for num in timed_generator(numbers, 0.5):
        print(f"got number: {num}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a generator that:
#    - implements prime number sequence
#    - uses sieve of eratosthenes
#    - optimizes memory usage
#    - supports range limits

# 2. create a generator that:
#    - implements tree traversal
#    - supports different orders
#    - handles cycles
#    - manages state

# 3. create a generator that:
#    - implements custom iteration
#    - supports bidirectional flow
#    - handles backtracking
#    - manages resources 