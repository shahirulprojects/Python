# generator expressions and comprehensions in python
from typing import Generator, List, Dict, Set, Any
import sys
import time
import logging
from datetime import datetime

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def compare_memory_usage(name: str, obj: Any) -> None:
    """compare memory usage of object."""
    size = sys.getsizeof(obj)
    logging.info(f"{name} size: {size} bytes")

def measure_time(func: callable) -> float:
    """measure execution time of function."""
    start = time.time()
    func()
    return time.time() - start

def demonstrate_list_vs_generator():
    """compare list comprehension vs generator expression."""
    # list comprehension
    list_comp = [x ** 2 for x in range(1000000)]
    compare_memory_usage("list comprehension", list_comp)
    
    # generator expression
    gen_exp = (x ** 2 for x in range(1000000))
    compare_memory_usage("generator expression", gen_exp)
    
    # measure iteration time
    list_time = measure_time(lambda: [x for x in list_comp])
    gen_time = measure_time(lambda: [x for x in gen_exp])
    
    logging.info(f"list iteration time: {list_time:.4f} seconds")
    logging.info(f"generator iteration time: {gen_time:.4f} seconds")

def nested_generator_expressions():
    """demonstrate nested generator expressions."""
    # nested generator expression
    matrix = ((i + j for j in range(3)) for i in range(3))
    
    # convert to list for display
    result = [list(row) for row in matrix]
    print("nested generator result:")
    for row in result:
        print(row)

def conditional_generator_expressions():
    """demonstrate conditional generator expressions."""
    # with filter
    even_squares = (x ** 2 for x in range(10) if x % 2 == 0)
    print("even squares:", list(even_squares))
    
    # with multiple conditions
    filtered = (
        x for x in range(20)
        if x % 2 == 0
        if x % 3 == 0
    )
    print("numbers divisible by 2 and 3:", list(filtered))

def dict_set_comprehensions():
    """demonstrate dictionary and set comprehensions."""
    # dictionary comprehension
    squares_dict = {x: x ** 2 for x in range(5)}
    print("squares dictionary:", squares_dict)
    
    # set comprehension
    unique_letters = {c.lower() for c in "Hello World"}
    print("unique letters:", unique_letters)
    
    # dictionary with conditions
    even_squares = {
        x: x ** 2
        for x in range(10)
        if x % 2 == 0
    }
    print("even squares dictionary:", even_squares)

def generator_pipeline():
    """demonstrate generator expression pipeline."""
    # create pipeline of transformations
    numbers = range(10)
    doubled = (x * 2 for x in numbers)
    filtered = (x for x in doubled if x % 4 == 0)
    squared = (x ** 2 for x in filtered)
    
    print("pipeline result:", list(squared))

def lazy_file_processing():
    """demonstrate lazy file processing with generators."""
    # create sample file
    with open('numbers.txt', 'w') as f:
        f.write('\n'.join(str(x) for x in range(100)))
    
    # process file lazily
    with open('numbers.txt', 'r') as f:
        numbers = (int(line.strip()) for line in f)
        squared = (x ** 2 for x in numbers if x % 2 == 0)
        
        # process in chunks
        chunk_size = 10
        chunks = list()
        
        while True:
            chunk = list(next(squared) for _ in range(chunk_size))
            if not chunk:
                break
            chunks.append(chunk)
            
            if len(chunks) >= 3:  # limit output
                break
    
    print("first 3 chunks of squared even numbers:")
    for chunk in chunks:
        print(chunk)

def infinite_generator_expression():
    """demonstrate infinite generator expression with takewhile."""
    from itertools import takewhile
    
    # infinite sequence of powers of 2
    powers_of_2 = (2 ** x for x in range(100))
    
    # take values while less than 1000
    result = list(takewhile(lambda x: x < 1000, powers_of_2))
    print("powers of 2 less than 1000:", result)

def main():
    """demonstrate generator expressions and comprehensions."""
    # 1. list comprehension vs generator expression
    print("1. comparing list comprehension vs generator expression:")
    demonstrate_list_vs_generator()
    
    # 2. nested generator expressions
    print("\n2. testing nested generator expressions:")
    nested_generator_expressions()
    
    # 3. conditional generator expressions
    print("\n3. testing conditional generator expressions:")
    conditional_generator_expressions()
    
    # 4. dictionary and set comprehensions
    print("\n4. testing dictionary and set comprehensions:")
    dict_set_comprehensions()
    
    # 5. generator pipeline
    print("\n5. testing generator pipeline:")
    generator_pipeline()
    
    # 6. lazy file processing
    print("\n6. testing lazy file processing:")
    lazy_file_processing()
    
    # 7. infinite generator expression
    print("\n7. testing infinite generator expression:")
    infinite_generator_expression()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a generator expression that:
#    - processes large datasets
#    - implements data transformation
#    - handles filtering
#    - optimizes memory usage

# 2. create a generator expression that:
#    - implements matrix operations
#    - supports element-wise operations
#    - handles sparse matrices
#    - optimizes computation

# 3. create a generator expression that:
#    - implements custom aggregation
#    - supports multiple operations
#    - handles grouping
#    - manages state