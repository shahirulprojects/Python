# distributed caching in python
from typing import Any, Dict, List, Callable, TypeVar, cast, Optional, Union
import logging
import time
import json
import asyncio
import aioredis
import hashlib
from datetime import datetime
from functools import wraps
from abc import ABC, abstractmethod

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# type variables for better type hints
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')

class CacheBackend(ABC):
    """abstract base class for cache backends."""
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """get value from cache."""
        pass
    
    @abstractmethod
    async def set(
        self,
        key: str,
        value: str,
        ttl: Optional[int] = None
    ) -> None:
        """set value in cache."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """delete value from cache."""
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """clear all values from cache."""
        pass

class RedisBackend(CacheBackend):
    """redis cache backend implementation."""
    def __init__(self, url: str = "redis://localhost"):
        self.url = url
        self.client: Optional[aioredis.Redis] = None
    
    async def connect(self) -> None:
        """connect to redis."""
        if not self.client:
            self.client = await aioredis.from_url(self.url)
    
    async def disconnect(self) -> None:
        """disconnect from redis."""
        if self.client:
            await self.client.close()
            self.client = None
    
    async def get(self, key: str) -> Optional[str]:
        """get value from redis."""
        await self.connect()
        value = await self.client.get(key)
        return value.decode() if value else None
    
    async def set(
        self,
        key: str,
        value: str,
        ttl: Optional[int] = None
    ) -> None:
        """set value in redis."""
        await self.connect()
        await self.client.set(key, value, ex=ttl)
    
    async def delete(self, key: str) -> None:
        """delete value from redis."""
        await self.connect()
        await self.client.delete(key)
    
    async def clear(self) -> None:
        """clear all values from redis."""
        await self.connect()
        await self.client.flushdb()

class DistributedCache:
    """distributed cache implementation."""
    def __init__(
        self,
        backend: CacheBackend,
        namespace: str = "cache"
    ):
        self.backend = backend
        self.namespace = namespace
    
    def make_key(self, key: str) -> str:
        """create namespaced cache key."""
        return f"{self.namespace}:{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        """get value from cache."""
        full_key = self.make_key(key)
        value = await self.backend.get(full_key)
        return json.loads(value) if value else None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """set value in cache."""
        full_key = self.make_key(key)
        json_value = json.dumps(value)
        await self.backend.set(full_key, json_value, ttl)
    
    async def delete(self, key: str) -> None:
        """delete value from cache."""
        full_key = self.make_key(key)
        await self.backend.delete(full_key)
    
    async def clear(self) -> None:
        """clear all values from cache."""
        await self.backend.clear()

def distributed_cache(
    namespace: str = "cache",
    ttl: Optional[int] = None,
    backend: Optional[CacheBackend] = None
) -> Callable[[F], F]:
    """decorator for distributed caching."""
    def decorator(func: F) -> F:
        cache = DistributedCache(
            backend or RedisBackend(),
            namespace=namespace
        )
        
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # create cache key
            key = hashlib.md5(
                f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
                .encode()
            ).hexdigest()
            
            # check cache
            result = await cache.get(key)
            if result is not None:
                logging.info(f"cache hit for {func.__name__}")
                return result
            
            # compute result
            logging.info(f"cache miss for {func.__name__}")
            result = await func(*args, **kwargs)
            
            # cache result
            await cache.set(key, result, ttl)
            return result
        
        # attach cache to wrapper
        wrapper.cache = cache
        return cast(F, wrapper)
    
    return decorator

class CacheCluster:
    """distributed cache cluster."""
    def __init__(self, backends: List[CacheBackend]):
        self.backends = backends
        self.num_backends = len(backends)
    
    def get_backend(self, key: str) -> CacheBackend:
        """get backend for key using consistent hashing."""
        hash_value = int(
            hashlib.md5(key.encode()).hexdigest(),
            16
        )
        return self.backends[hash_value % self.num_backends]
    
    async def get(self, key: str) -> Optional[Any]:
        """get value from cluster."""
        backend = self.get_backend(key)
        value = await backend.get(key)
        return json.loads(value) if value else None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """set value in cluster."""
        backend = self.get_backend(key)
        json_value = json.dumps(value)
        await backend.set(key, json_value, ttl)
    
    async def delete(self, key: str) -> None:
        """delete value from cluster."""
        backend = self.get_backend(key)
        await backend.delete(key)
    
    async def clear(self) -> None:
        """clear all values from cluster."""
        await asyncio.gather(
            *(backend.clear() for backend in self.backends)
        )

async def main():
    """demonstrate distributed caching."""
    # 1. basic distributed cache
    print("1. testing basic distributed cache:")
    backend = RedisBackend()
    cache = DistributedCache(backend, namespace="test")
    
    # set value
    await cache.set("key1", "value1")
    
    # get value
    value = await cache.get("key1")
    print(f"got value: {value}")
    
    # delete value
    await cache.delete("key1")
    value = await cache.get("key1")
    print(f"value after deletion: {value}")
    
    # 2. distributed cache decorator
    print("\n2. testing distributed cache decorator:")
    @distributed_cache(namespace="test", ttl=5)
    async def slow_operation(x: int) -> int:
        await asyncio.sleep(1)  # simulate work
        return x * x
    
    # first call
    result1 = await slow_operation(5)
    print(f"first call result: {result1}")
    
    # second call (cached)
    result2 = await slow_operation(5)
    print(f"second call result: {result2}")
    
    # 3. cache cluster
    print("\n3. testing cache cluster:")
    backends = [
        RedisBackend("redis://localhost:6379/0"),
        RedisBackend("redis://localhost:6379/1"),
        RedisBackend("redis://localhost:6379/2")
    ]
    cluster = CacheCluster(backends)
    
    # set values
    await cluster.set("key1", "value1")
    await cluster.set("key2", "value2")
    await cluster.set("key3", "value3")
    
    # get values
    for key in ["key1", "key2", "key3"]:
        value = await cluster.get(key)
        backend = cluster.get_backend(key)
        print(f"key: {key}, value: {value}, backend: {backend.url}")
    
    # cleanup
    await backend.disconnect()
    for backend in backends:
        await backend.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

# practice exercises:
# 1. create a distributed cache that:
#    - implements cache replication
#    - handles failover
#    - supports master-slave setup
#    - manages consistency

# 2. create a distributed cache that:
#    - implements cache partitioning
#    - handles data migration
#    - supports dynamic scaling
#    - manages load balancing

# 3. create a distributed cache that:
#    - implements cache coherence
#    - handles write-through/write-back
#    - supports cache invalidation
#    - manages cache consistency 