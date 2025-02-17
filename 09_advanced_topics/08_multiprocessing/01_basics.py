import multiprocessing as mp
from multiprocessing import Pool, Process, Queue, Lock, Value, Array
from typing import List, Any, Callable
import time
import logging
import numpy as np
from dataclasses import dataclass
import os

# welcome to multiprocessing! this is where we learn how to use multiple cpu cores
# to make our programs run faster :D multiprocessing is perfect for cpu-intensive tasks
# that can be split into independent parts

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# example 1: basic process creation
def worker_function(name: str):
    # this function runs in a separate process
    logging.info(f"worker {name} starting (pid: {os.getpid()})")
    time.sleep(1)  # simulate work
    logging.info(f"worker {name} finished")

# example 2: sharing data between processes
@dataclass
class WorkItem:
    id: int
    data: np.ndarray

def process_data(
    work_item: WorkItem,
    result_queue: Queue,
    status: Value
) -> None:
    # simulate cpu-intensive work
    logging.info(f"processing item {work_item.id}")
    result = np.sum(work_item.data)
    
    # update shared counter
    with status.get_lock():
        status.value += 1
    
    # send result back
    result_queue.put((work_item.id, result))

# example 3: process pool for parallel operations
def cpu_intensive_task(x: int) -> int:
    # simulate cpu-intensive computation
    time.sleep(0.1)
    return x * x

def parallel_map(
    func: Callable,
    items: List[Any],
    processes: int = None
) -> List[Any]:
    if processes is None:
        processes = mp.cpu_count()
    
    with Pool(processes=processes) as pool:
        return pool.map(func, items)

# example 4: process synchronization
class SharedCounter:
    def __init__(self, initial_value: int = 0):
        self.count = Value('i', initial_value)
        self.lock = Lock()
    
    def increment(self):
        with self.lock:
            self.count.value += 1
    
    def get_value(self) -> int:
        with self.lock:
            return self.count.value

def increment_counter(counter: SharedCounter, iterations: int):
    for _ in range(iterations):
        counter.increment()
        time.sleep(0.001)  # make race conditions more likely

# example 5: shared memory with arrays
def array_worker(
    shared_array: Array,
    start: int,
    end: int,
    lock: Lock
):
    # process a section of shared array
    local_sum = sum(shared_array[start:end])
    
    # update array with local results
    with lock:
        for i in range(start, end):
            shared_array[i] *= 2

def main():
    # example 1: basic processes
    logging.info(f"main process pid: {os.getpid()}")
    
    processes = [
        Process(target=worker_function, args=(f"worker{i}",))
        for i in range(3)
    ]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
    
    # example 2: data sharing
    result_queue = Queue()
    status = Value('i', 0)
    
    # create some work items
    work_items = [
        WorkItem(i, np.random.rand(1000))
        for i in range(3)
    ]
    
    # create processes for each work item
    data_processes = [
        Process(
            target=process_data,
            args=(item, result_queue, status)
        )
        for item in work_items
    ]
    
    for p in data_processes:
        p.start()
    
    # collect results
    results = []
    for _ in range(len(work_items)):
        results.append(result_queue.get())
    
    for p in data_processes:
        p.join()
    
    logging.info(f"processed items: {status.value}")
    logging.info(f"results: {results}")
    
    # example 3: process pool
    numbers = list(range(10))
    
    logging.info("starting parallel computation...")
    start_time = time.time()
    
    results = parallel_map(cpu_intensive_task, numbers)
    
    duration = time.time() - start_time
    logging.info(f"parallel computation completed in {duration:.2f}s")
    logging.info(f"results: {results}")
    
    # example 4: process synchronization
    counter = SharedCounter()
    
    sync_processes = [
        Process(
            target=increment_counter,
            args=(counter, 100)
        )
        for _ in range(3)
    ]
    
    for p in sync_processes:
        p.start()
    
    for p in sync_processes:
        p.join()
    
    logging.info(f"final counter value: {counter.get_value()}")
    
    # example 5: shared arrays
    array_size = 1000
    shared_array = Array('i', [1] * array_size)
    lock = Lock()
    
    # split work among processes
    chunk_size = array_size // 4
    array_processes = [
        Process(
            target=array_worker,
            args=(
                shared_array,
                i * chunk_size,
                (i + 1) * chunk_size,
                lock
            )
        )
        for i in range(4)
    ]
    
    for p in array_processes:
        p.start()
    
    for p in array_processes:
        p.join()
    
    logging.info(f"shared array sum: {sum(shared_array)}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. implement a parallel processing system that:
#    - handles dynamic task allocation
#    - implements work stealing
#    - provides progress monitoring

# 2. create a shared memory system that:
#    - supports complex data structures
#    - handles concurrent modifications
#    - implements memory management

# 3. implement a process pool that:
#    - supports different scheduling strategies
#    - handles process failures
#    - provides resource limits 