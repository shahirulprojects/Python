# async context managers in python
from typing import Any, AsyncGenerator, Optional, List, Dict
import logging
import asyncio
import aiohttp
import aiofiles
from contextlib import asynccontextmanager
from datetime import datetime
import time

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AsyncResource:
    """async resource class."""
    def __init__(self, name: str):
        self.name = name
    
    async def initialize(self) -> None:
        """initialize resource."""
        logging.info(f"initializing {self.name}")
        await asyncio.sleep(0.1)  # simulate initialization
    
    async def cleanup(self) -> None:
        """cleanup resource."""
        logging.info(f"cleaning up {self.name}")
        await asyncio.sleep(0.1)  # simulate cleanup

class AsyncResourceManager:
    """async context manager for resource."""
    def __init__(self, name: str):
        self.resource = AsyncResource(name)
    
    async def __aenter__(self) -> AsyncResource:
        """enter async context."""
        await self.resource.initialize()
        return self.resource
    
    async def __aexit__(
        self,
        exc_type: Any,
        exc_val: Any,
        exc_tb: Any
    ) -> bool:
        """exit async context."""
        await self.resource.cleanup()
        return False

class AsyncConnectionPool:
    """async connection pool."""
    def __init__(self, size: int):
        self.size = size
        self.connections: List[Any] = []
        self.available: asyncio.Queue = asyncio.Queue()
        self._lock = asyncio.Lock()
    
    async def initialize(self) -> None:
        """initialize connection pool."""
        async with self._lock:
            for i in range(self.size):
                conn = f"connection_{i}"
                self.connections.append(conn)
                await self.available.put(conn)
    
    async def acquire(self) -> Any:
        """acquire connection."""
        return await self.available.get()
    
    async def release(self, conn: Any) -> None:
        """release connection."""
        await self.available.put(conn)
    
    async def cleanup(self) -> None:
        """cleanup connection pool."""
        async with self._lock:
            self.connections.clear()
            while not self.available.empty():
                await self.available.get()

class AsyncPoolManager:
    """async context manager for connection pool."""
    def __init__(self, size: int):
        self.pool = AsyncConnectionPool(size)
    
    async def __aenter__(self) -> AsyncConnectionPool:
        """enter async context."""
        await self.pool.initialize()
        return self.pool
    
    async def __aexit__(
        self,
        exc_type: Any,
        exc_val: Any,
        exc_tb: Any
    ) -> bool:
        """exit async context."""
        await self.pool.cleanup()
        return False

@asynccontextmanager
async def http_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """async context manager for http session."""
    async with aiohttp.ClientSession() as session:
        try:
            yield session
        finally:
            await session.close()

@asynccontextmanager
async def async_timer(name: str) -> AsyncGenerator[float, None]:
    """async context manager for timing."""
    start = time.time()
    try:
        yield start
    finally:
        duration = time.time() - start
        logging.info(f"{name} took {duration:.4f} seconds")

class AsyncFileHandler:
    """async context manager for file handling."""
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    async def __aenter__(self) -> Any:
        """enter async context."""
        self.file = await aiofiles.open(self.filename, self.mode)
        return self.file
    
    async def __aexit__(
        self,
        exc_type: Any,
        exc_val: Any,
        exc_tb: Any
    ) -> bool:
        """exit async context."""
        if self.file:
            await self.file.close()
        return False

class AsyncTransaction:
    """async context manager for transactions."""
    def __init__(self):
        self.operations: List[str] = []
    
    async def __aenter__(self) -> 'AsyncTransaction':
        """enter async context."""
        logging.info("starting transaction")
        return self
    
    async def __aexit__(
        self,
        exc_type: Any,
        exc_val: Any,
        exc_tb: Any
    ) -> bool:
        """exit async context."""
        if exc_type is None:
            logging.info(f"committing transaction: {self.operations}")
            await asyncio.sleep(0.1)  # simulate commit
        else:
            logging.error(f"rolling back transaction: {str(exc_val)}")
            await asyncio.sleep(0.1)  # simulate rollback
        return False
    
    async def add_operation(self, operation: str) -> None:
        """add operation to transaction."""
        self.operations.append(operation)
        await asyncio.sleep(0.1)  # simulate operation

async def main():
    """demonstrate async context manager usage."""
    # 1. async resource
    print("1. testing async resource:")
    async with AsyncResourceManager("test_resource") as resource:
        print(f"using resource: {resource.name}")
    
    # 2. async connection pool
    print("\n2. testing async connection pool:")
    async with AsyncPoolManager(2) as pool:
        # acquire connections
        conn1 = await pool.acquire()
        print(f"acquired: {conn1}")
        
        conn2 = await pool.acquire()
        print(f"acquired: {conn2}")
        
        # release connection
        await pool.release(conn1)
        print(f"released: {conn1}")
        
        # acquire again
        conn3 = await pool.acquire()
        print(f"acquired: {conn3}")
    
    # 3. http session
    print("\n3. testing http session:")
    async with http_session() as session:
        async with session.get('http://example.com') as response:
            print(f"status: {response.status}")
    
    # 4. async timer
    print("\n4. testing async timer:")
    async with async_timer("sleep_operation"):
        await asyncio.sleep(0.5)
    
    # 5. async file handling
    print("\n5. testing async file handling:")
    # create test file
    async with AsyncFileHandler('async_test.txt', 'w') as f:
        await f.write('hello async world')
    
    async with AsyncFileHandler('async_test.txt', 'r') as f:
        content = await f.read()
        print(f"file content: {content}")
    
    # 6. async transaction
    print("\n6. testing async transaction:")
    try:
        async with AsyncTransaction() as transaction:
            await transaction.add_operation("operation 1")
            await transaction.add_operation("operation 2")
            if True:  # simulate error
                raise ValueError("transaction error")
    except ValueError as e:
        print(f"transaction failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())

# practice exercises:
# 1. create an async context manager that:
#    - implements connection pooling
#    - handles reconnection
#    - supports health checks
#    - manages load balancing

# 2. create an async context manager that:
#    - implements distributed cache
#    - handles cache invalidation
#    - supports cache replication
#    - manages consistency

# 3. create an async context manager that:
#    - implements rate limiting
#    - handles distributed counters
#    - supports dynamic limits
#    - manages fairness 