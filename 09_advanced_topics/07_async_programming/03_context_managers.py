import asyncio
from typing import Any, AsyncIterator, Optional, List
from contextlib import asynccontextmanager
import logging
import aiofiles
import aiohttp
from datetime import datetime, timedelta

# hey there! let's learn about async context managers and resource management :D
# these help us handle cleanup and resource management in async code properly

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# example 1: basic async context manager
class AsyncResource:
    def __init__(self, name: str):
        self.name = name
        self._is_initialized = False
    
    async def initialize(self):
        # simulate resource initialization
        logging.info(f"initializing {self.name}...")
        await asyncio.sleep(0.1)
        self._is_initialized = True
    
    async def cleanup(self):
        # simulate resource cleanup
        if self._is_initialized:
            logging.info(f"cleaning up {self.name}...")
            await asyncio.sleep(0.1)
            self._is_initialized = False
    
    async def __aenter__(self) -> 'AsyncResource':
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()

# example 2: resource pool with async context manager
class ResourcePool:
    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self._resources: List[AsyncResource] = []
        self._available = asyncio.Queue()
        self._lock = asyncio.Lock()
    
    async def initialize(self):
        # create initial resources
        async with self._lock:
            for i in range(self.max_size):
                resource = AsyncResource(f"resource{i}")
                await resource.initialize()
                self._resources.append(resource)
                await self._available.put(resource)
    
    async def cleanup(self):
        # cleanup all resources
        async with self._lock:
            while not self._available.empty():
                resource = await self._available.get()
                await resource.cleanup()
            self._resources.clear()
    
    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[AsyncResource]:
        # get a resource from the pool
        resource = await self._available.get()
        try:
            yield resource
        finally:
            # return resource to pool
            await self._available.put(resource)

# example 3: async file context manager with buffering
@asynccontextmanager
async def buffered_file(
    filename: str,
    mode: str = 'r',
    buffer_size: int = 8192
) -> AsyncIterator[aiofiles.threadpool.AsyncBufferedIOBase]:
    async with aiofiles.open(filename, mode) as file:
        # create buffered reader/writer
        if 'r' in mode:
            buffer = []
            try:
                while len(buffer) < buffer_size:
                    chunk = await file.read(buffer_size)
                    if not chunk:
                        break
                    buffer.append(chunk)
                yield ''.join(buffer)
            finally:
                buffer.clear()
        else:
            buffer = ''
            try:
                yield buffer
            finally:
                if buffer:
                    await file.write(buffer)

# example 4: connection pool with timeouts
class DatabaseConnection:
    def __init__(self, name: str):
        self.name = name
        self.connected = False
    
    async def connect(self):
        logging.info(f"connecting to database {self.name}...")
        await asyncio.sleep(0.1)
        self.connected = True
    
    async def disconnect(self):
        if self.connected:
            logging.info(f"disconnecting from database {self.name}...")
            await asyncio.sleep(0.1)
            self.connected = False
    
    async def execute(self, query: str) -> str:
        if not self.connected:
            raise RuntimeError("not connected")
        return f"executed {query} on {self.name}"

class ConnectionPool:
    def __init__(
        self,
        max_size: int = 5,
        timeout: float = 5.0
    ):
        self.max_size = max_size
        self.timeout = timeout
        self._connections: List[DatabaseConnection] = []
        self._available = asyncio.Queue()
        self._lock = asyncio.Lock()
    
    @asynccontextmanager
    async def connection(self) -> AsyncIterator[DatabaseConnection]:
        try:
            # try to get connection with timeout
            connection = await asyncio.wait_for(
                self._available.get(),
                timeout=self.timeout
            )
            try:
                yield connection
            finally:
                await self._available.put(connection)
        except asyncio.TimeoutError:
            raise TimeoutError("connection pool exhausted")

    async def initialize(self):
        async with self._lock:
            for i in range(self.max_size):
                conn = DatabaseConnection(f"db{i}")
                await conn.connect()
                self._connections.append(conn)
                await self._available.put(conn)
    
    async def cleanup(self):
        async with self._lock:
            while not self._available.empty():
                conn = await self._available.get()
                await conn.disconnect()
            self._connections.clear()

# now let's see these in action
async def example_resource_management():
    # example 1: basic async resource
    async with AsyncResource("simple_resource") as resource:
        logging.info(f"using {resource.name}")
    
    # example 2: resource pool
    pool = ResourcePool(max_size=3)
    await pool.initialize()
    
    try:
        async with pool.acquire() as resource1:
            logging.info(f"using {resource1.name}")
            
            # nested resource acquisition
            async with pool.acquire() as resource2:
                logging.info(f"using {resource2.name}")
    finally:
        await pool.cleanup()
    
    # example 3: buffered file operations
    try:
        async with buffered_file("test.txt", "w") as buffer:
            logging.info("writing to buffered file")
            buffer += "hello world\n"
    except Exception as e:
        logging.error(f"file error: {e}")
    
    # example 4: database connection pool
    db_pool = ConnectionPool(max_size=2)
    await db_pool.initialize()
    
    try:
        async with db_pool.connection() as conn1:
            result1 = await conn1.execute("SELECT * FROM table1")
            logging.info(result1)
            
            async with db_pool.connection() as conn2:
                result2 = await conn2.execute("SELECT * FROM table2")
                logging.info(result2)
                
                # this would timeout as pool is exhausted
                try:
                    async with db_pool.connection() as conn3:
                        await conn3.execute("SELECT * FROM table3")
                except TimeoutError as e:
                    logging.error(f"timeout error: {e}")
    finally:
        await db_pool.cleanup()

async def main():
    try:
        await example_resource_management()
    except Exception as e:
        logging.error(f"unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

# practice exercises:
# 1. implement an async connection pool that:
#    - supports different types of connections
#    - implements connection health checks
#    - handles connection recycling

# 2. create an async resource manager that:
#    - supports resource dependencies
#    - implements resource cleanup ordering
#    - handles cleanup failures

# 3. implement an async file manager that:
#    - supports streaming large files
#    - implements backpressure
#    - handles partial writes