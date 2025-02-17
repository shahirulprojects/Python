import asyncio
from typing import List, Any
import time
import aiohttp
import random

# welcome to async programming in python! this is where things get really exciting :D
# async programming lets us do multiple things at once without blocking each other
# think of it like cooking: you can start boiling water while chopping vegetables

# first, let's understand the basic concepts:
# 1. coroutines: special functions that can pause and resume
# 2. async/await: keywords that make async code look like normal code
# 3. event loop: the "chef" that manages all our async tasks

# here's a simple coroutine that simulates some work
async def do_work(name: str, duration: float) -> str:
    # this is like starting a task that takes some time
    print(f"{name} starting work...")
    await asyncio.sleep(duration)  # non-blocking sleep
    print(f"{name} finished work!")
    return f"{name} result"

# let's see how to run multiple coroutines
async def main_simple():
    # create some work items
    work_items = [
        do_work("task1", 2),
        do_work("task2", 1),
        do_work("task3", 3)
    ]
    
    # run them all at once and wait for results
    results = await asyncio.gather(*work_items)
    print(f"all results: {results}")

# now let's see a real-world example: fetching data from websites
async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    # this simulates fetching data from a website
    print(f"starting to fetch {url}")
    
    try:
        async with session.get(url) as response:
            # simulate varying response times
            await asyncio.sleep(random.uniform(0.5, 2))
            return {
                'url': url,
                'status': response.status,
                'length': len(await response.text())
            }
    except Exception as e:
        return {'url': url, 'error': str(e)}

async def fetch_multiple_urls(urls: List[str]) -> List[dict]:
    # create a session for all requests
    async with aiohttp.ClientSession() as session:
        # create tasks for all urls
        tasks = [
            fetch_url(session, url)
            for url in urls
        ]
        
        # run all tasks concurrently
        return await asyncio.gather(*tasks)

# example of handling multiple async operations
async def main_web():
    # list of urls to fetch
    urls = [
        'http://example.com',
        'http://google.com',
        'http://github.com',
        'http://python.org'
    ]
    
    print("starting to fetch urls...")
    start_time = time.time()
    
    # fetch all urls concurrently
    results = await fetch_multiple_urls(urls)
    
    # show results
    duration = time.time() - start_time
    print(f"\nall fetches completed in {duration:.2f} seconds")
    for result in results:
        print(f"result: {result}")

# example of using asyncio.Queue for task management
async def worker(name: str, queue: asyncio.Queue) -> None:
    while True:
        # get a task from the queue
        task = await queue.get()
        
        if task is None:  # sentinel value to stop worker
            queue.task_done()
            break
        
        # process the task
        print(f"{name} processing task: {task}")
        await asyncio.sleep(random.uniform(0.1, 0.5))
        queue.task_done()

async def main_queue():
    # create a queue
    queue = asyncio.Queue()
    
    # create some workers
    workers = [
        asyncio.create_task(worker(f"worker{i}", queue))
        for i in range(3)
    ]
    
    # add some tasks to the queue
    tasks = list(range(10))
    for task in tasks:
        await queue.put(task)
    
    # add sentinel values to stop workers
    for _ in workers:
        await queue.put(None)
    
    # wait for all tasks to complete
    await queue.join()
    
    # wait for workers to finish
    await asyncio.gather(*workers)

def main():
    # run our async examples
    print("running simple example:")
    asyncio.run(main_simple())
    
    print("\nrunning web example:")
    asyncio.run(main_web())
    
    print("\nrunning queue example:")
    asyncio.run(main_queue())

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create an async program that:
#    - simulates a chat system
#    - handles multiple users
#    - processes messages concurrently

# 2. create an async program that:
#    - downloads multiple files
#    - shows progress bars
#    - handles errors gracefully

# 3. create an async program that:
#    - implements a task scheduler
#    - handles priorities
#    - manages task dependencies 