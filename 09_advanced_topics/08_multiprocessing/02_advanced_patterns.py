import multiprocessing as mp
from multiprocessing import (
    Pool, Process, Queue, Lock, Value, Array,
    Pipe, Manager, Event, Semaphore
)
from multiprocessing.managers import SyncManager
from typing import Any, Dict, List, Optional, Tuple, Callable
import time
import logging
import numpy as np
from dataclasses import dataclass
import os
import signal
import queue
import threading
from contextlib import contextmanager

# welcome to advanced multiprocessing patterns! here we'll explore complex
# scenarios and patterns for parallel processing :D

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 1. worker pool with dynamic task allocation
class WorkerPool:
    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or mp.cpu_count()
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.workers: List[Process] = []
        self.running = Value('b', True)
        self._init_workers()
    
    def _init_workers(self):
        for i in range(self.num_workers):
            worker = Process(
                target=self._worker_loop,
                args=(i, self.task_queue, self.result_queue, self.running)
            )
            worker.start()
            self.workers.append(worker)
    
    @staticmethod
    def _worker_loop(
        worker_id: int,
        task_queue: Queue,
        result_queue: Queue,
        running: Value
    ):
        while running.value:
            try:
                # get task with timeout
                task = task_queue.get(timeout=1)
                
                # process task
                func, args = task
                result = func(*args)
                
                # send result
                result_queue.put((worker_id, result))
            except queue.Empty:
                continue
            except Exception as e:
                result_queue.put((worker_id, e))
    
    def submit(self, func: Callable, *args: Any):
        self.task_queue.put((func, args))
    
    def get_results(self) -> List[Tuple[int, Any]]:
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        return results
    
    def shutdown(self):
        with self.running.get_lock():
            self.running.value = False
        
        for worker in self.workers:
            worker.join()

# 2. shared memory manager with custom types
class SharedState:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self._lock = Lock()
    
    def set(self, key: str, value: Any):
        with self._lock:
            self.data[key] = value
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            return self.data.get(key)

class CustomManager(SyncManager):
    pass

CustomManager.register('SharedState', SharedState)

# 3. process pool with resource management
@contextmanager
def managed_pool(
    processes: int = None,
    initializer: Callable = None,
    initargs: tuple = ()
):
    pool = Pool(
        processes=processes,
        initializer=initializer,
        initargs=initargs
    )
    try:
        yield pool
    finally:
        pool.close()
        pool.join()

# 4. inter-process communication patterns
class MessageBroker:
    def __init__(self):
        self.subscribers: Dict[str, List[Pipe]] = {}
        self._lock = Lock()
    
    def subscribe(self, topic: str) -> Pipe:
        parent_conn, child_conn = Pipe()
        with self._lock:
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            self.subscribers[topic].append(parent_conn)
        return child_conn
    
    def publish(self, topic: str, message: Any):
        with self._lock:
            if topic in self.subscribers:
                for conn in self.subscribers[topic]:
                    conn.send(message)

# 5. process synchronization patterns
class Barrier:
    def __init__(self, parties: int):
        self.parties = parties
        self.count = Value('i', 0)
        self.generation = Value('i', 0)
        self.lock = Lock()
        self.event = Event()
    
    def wait(self):
        generation = self.generation.value
        
        with self.lock:
            self.count.value += 1
            if self.count.value == self.parties:
                # last thread to arrive
                self.event.set()
                self.count.value = 0
                self.generation.value += 1
        
        # wait for barrier
        while (
            generation == self.generation.value
            and not self.event.is_set()
        ):
            self.event.wait(timeout=0.1)
        
        # reset event for next generation
        if generation != self.generation.value:
            self.event.clear()

# now let's see these patterns in action
def example_advanced_patterns():
    # example 1: worker pool
    print("worker pool example:")
    pool = WorkerPool(num_workers=3)
    
    def cpu_intensive(x: int) -> int:
        time.sleep(0.1)  # simulate work
        return x * x
    
    # submit tasks
    for i in range(5):
        pool.submit(cpu_intensive, i)
    
    # get results
    time.sleep(1)  # wait for tasks to complete
    results = pool.get_results()
    print(f"worker pool results: {results}")
    
    pool.shutdown()
    
    # example 2: shared state
    print("\nshared state example:")
    with CustomManager() as manager:
        shared_state = manager.SharedState()
        
        def update_state(key: str, value: Any):
            shared_state.set(key, value)
            print(f"process {os.getpid()} set {key} = {value}")
            print(f"process {os.getpid()} get {key} = {shared_state.get(key)}")
        
        processes = [
            Process(target=update_state, args=(f"key{i}", i))
            for i in range(3)
        ]
        
        for p in processes:
            p.start()
        
        for p in processes:
            p.join()
    
    # example 3: managed pool
    print("\nmanaged pool example:")
    def init_worker():
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    with managed_pool(processes=2, initializer=init_worker) as pool:
        results = pool.map(cpu_intensive, range(5))
        print(f"managed pool results: {results}")
    
    # example 4: message broker
    print("\nmessage broker example:")
    broker = MessageBroker()
    
    def subscriber_process(name: str, conn):
        while True:
            try:
                message = conn.recv()
                print(f"{name} received: {message}")
                if message == "stop":
                    break
            except EOFError:
                break
    
    # create subscribers
    conns = [
        broker.subscribe("topic1")
        for _ in range(2)
    ]
    
    processes = [
        Process(
            target=subscriber_process,
            args=(f"subscriber{i}", conn)
        )
        for i, conn in enumerate(conns)
    ]
    
    for p in processes:
        p.start()
    
    # publish messages
    broker.publish("topic1", "hello")
    broker.publish("topic1", "world")
    broker.publish("topic1", "stop")
    
    for p in processes:
        p.join()
    
    # example 5: barrier
    print("\nbarrier example:")
    barrier = Barrier(parties=3)
    
    def worker_process(name: str):
        print(f"{name} waiting at barrier")
        barrier.wait()
        print(f"{name} passed barrier")
    
    processes = [
        Process(target=worker_process, args=(f"worker{i}",))
        for i in range(3)
    ]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()

if __name__ == "__main__":
    example_advanced_patterns()

# practice exercises:
# 1. implement a process pool that:
#    - handles worker failures
#    - supports task priorities
#    - provides progress monitoring

# 2. create a shared memory system that:
#    - implements copy-on-write
#    - handles concurrent access
#    - manages memory limits

# 3. implement a message passing system that:
#    - supports pub/sub patterns
#    - handles message routing
#    - provides flow control 