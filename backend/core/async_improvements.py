"""
Async Improvements & Concurrency Utilities
Optimizes async operations, concurrent execution, and event loop management
"""

import asyncio
import time
from typing import Callable, List, Dict, Any, TypeVar, Coroutine, Optional
from functools import wraps
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])


class AsyncBatcher:
    """Batches async operations for concurrent execution"""
    
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.pending_tasks: List[asyncio.Task] = []
    
    async def add_task(
        self,
        coro: Coroutine,
        name: str = None
    ) -> None:
        """Add task to batch"""
        # Wait if we have too many pending
        while len(self.pending_tasks) >= self.max_concurrent:
            done, self.pending_tasks = await asyncio.wait(
                self.pending_tasks,
                return_when=asyncio.FIRST_COMPLETED
            )
        
        # Create task
        task = asyncio.create_task(coro)
        if name:
            task.set_name(name)
        self.pending_tasks.append(task)
    
    async def gather_all(self) -> List[Any]:
        """Wait for all tasks to complete and gather results"""
        if not self.pending_tasks:
            return []
        
        results = await asyncio.gather(*self.pending_tasks, return_exceptions=True)
        self.pending_tasks = []
        return results
    
    async def wait_all(self) -> None:
        """Wait for all tasks without returning results"""
        if self.pending_tasks:
            await asyncio.gather(*self.pending_tasks, return_exceptions=True)
            self.pending_tasks = []


class AsyncTimer:
    """Utility for timing async operations"""
    
    def __init__(self, operation_name: str = "Operation"):
        self.operation_name = operation_name
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
    
    async def __aenter__(self):
        self.start_time = time.time()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        elapsed = self.elapsed_seconds
        
        if exc_type:
            logger.error(
                f"{self.operation_name} failed after {elapsed:.2f}s: {exc_type.__name__}"
            )
        else:
            logger.info(f"{self.operation_name} completed in {elapsed:.2f}s")
    
    @property
    def elapsed_seconds(self) -> float:
        if self.start_time is None:
            return 0
        end = self.end_time or time.time()
        return end - self.start_time


class ConcurrencyLimiter:
    """Limits concurrent operations to prevent overwhelming resources"""
    
    def __init__(self, max_concurrent: int = 20):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def execute(self, coro: Coroutine) -> Any:
        """Execute coroutine with concurrency limit"""
        async with self.semaphore:
            return await coro
    
    async def execute_many(
        self,
        coros: List[Coroutine]
    ) -> List[Any]:
        """Execute multiple coroutines with concurrency limit"""
        tasks = [self.execute(coro) for coro in coros]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    def __repr__(self) -> str:
        return f"ConcurrencyLimiter(available={self.semaphore._value})"


class AsyncCache:
    """In-memory cache for async function results"""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl_seconds
    
    def _get_key(self, func_name: str, *args, **kwargs) -> str:
        """Generate cache key"""
        key_parts = [func_name]
        for arg in args:
            key_parts.append(str(arg))
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        return "|".join(key_parts)
    
    async def get_or_execute(
        self,
        func_name: str,
        coro: Coroutine,
        *args,
        **kwargs
    ) -> Any:
        """Get from cache or execute coroutine"""
        key = self._get_key(func_name, *args, **kwargs)
        
        # Check cache
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["timestamp"] < self.ttl:
                logger.debug(f"Async cache HIT: {key}")
                return entry["value"]
            else:
                del self.cache[key]
        
        # Execute
        result = await coro
        
        # Cache result
        self.cache[key] = {
            "value": result,
            "timestamp": time.time()
        }
        logger.debug(f"Async cache SET: {key}")
        
        return result
    
    def clear(self) -> None:
        """Clear cache"""
        self.cache.clear()


# ============================================================================
# ASYNC DECORATORS
# ============================================================================

def async_timer(func: F) -> F:
    """Decorator to time async function execution"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start
            logger.debug(f"{func.__name__} completed in {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"{func.__name__} failed after {elapsed:.2f}s: {e}")
            raise
    
    return wrapper  # type: ignore


def async_retry(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """
    Decorator to retry async function with exponential backoff
    
    Usage:
        @async_retry(max_retries=3, delay=1.0)
        async def fetch_data():
            ...
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        logger.error(
                            f"{func.__name__} failed after {max_retries} attempts: {e}"
                        )
                        raise
                    
                    logger.warning(
                        f"{func.__name__} attempt {attempt + 1} failed, "
                        f"retrying in {current_delay}s: {e}"
                    )
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
        
        return wrapper  # type: ignore
    
    return decorator


def async_timeout(seconds: float) -> Callable:
    """
    Decorator to add timeout to async function
    
    Usage:
        @async_timeout(5.0)
        async def long_operation():
            ...
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=seconds
                )
            except asyncio.TimeoutError:
                logger.error(
                    f"{func.__name__} exceeded timeout of {seconds}s"
                )
                raise
        
        return wrapper  # type: ignore
    
    return decorator


# ============================================================================
# BATCH ASYNC OPERATIONS
# ============================================================================

async def batch_async_operations(
    operations: List[Coroutine],
    batch_size: int = 10,
    delay_between_batches: float = 0.1
) -> List[Any]:
    """
    Execute async operations in batches to prevent overwhelming resources
    
    Usage:
        coros = [fetch_user(i) for i in range(100)]
        results = await batch_async_operations(coros, batch_size=20)
    """
    results = []
    
    for i in range(0, len(operations), batch_size):
        batch = operations[i : i + batch_size]
        batch_results = await asyncio.gather(*batch, return_exceptions=True)
        results.extend(batch_results)
        
        if i + batch_size < len(operations):
            await asyncio.sleep(delay_between_batches)
    
    return results


async def race_operations(
    operations: Dict[str, Coroutine],
    timeout: float = 30.0
) -> Dict[str, Any]:
    """
    Execute operations concurrently and return results as soon as ready
    
    Usage:
        results = await race_operations({
            "api1": fetch_from_api1(),
            "api2": fetch_from_api2(),
        })
    """
    tasks = {
        name: asyncio.create_task(coro)
        for name, coro in operations.items()
    }
    
    results = {}
    pending = set(tasks.values())
    
    try:
        while pending:
            done, pending = await asyncio.wait(
                pending,
                timeout=timeout,
                return_when=asyncio.FIRST_COMPLETED
            )
            
            for task in done:
                # Find task name
                for name, t in tasks.items():
                    if t == task:
                        try:
                            results[name] = task.result()
                        except Exception as e:
                            results[name] = {"error": str(e)}
                        break
    except asyncio.TimeoutError:
        logger.warning(f"Race operations timeout after {timeout}s")
    
    return results


async def gather_with_concurrency(
    semaphore: asyncio.Semaphore,
    *tasks: Coroutine
) -> List[Any]:
    """
    Gather coroutines with concurrency limit using semaphore
    
    Usage:
        semaphore = asyncio.Semaphore(10)
        results = await gather_with_concurrency(
            semaphore,
            *[fetch_data(i) for i in range(100)]
        )
    """
    async def bounded_task(task):
        async with semaphore:
            return await task
    
    return await asyncio.gather(
        *[bounded_task(task) for task in tasks],
        return_exceptions=True
    )


# ============================================================================
# ASYNC DATABASE HELPERS
# ============================================================================

async def bulk_insert_async(
    db,
    models_list: List[Any],
    batch_size: int = 100
) -> int:
    """
    Efficiently bulk insert models with batching
    """
    total_inserted = 0
    
    for i in range(0, len(models_list), batch_size):
        batch = models_list[i : i + batch_size]
        db.add_all(batch)
        await db.flush()
        total_inserted += len(batch)
        
        logger.debug(f"Inserted batch of {len(batch)} items")
    
    return total_inserted


async def bulk_update_async(
    db,
    updates: List[Dict[str, Any]],
    model_class,
    id_field: str = "id",
    batch_size: int = 50
) -> int:
    """
    Efficiently bulk update models with batching
    """
    from sqlalchemy import update
    
    total_updated = 0
    
    for i in range(0, len(updates), batch_size):
        batch = updates[i : i + batch_size]
        
        for update_data in batch:
            id_val = update_data.pop(id_field)
            stmt = (
                update(model_class)
                .where(getattr(model_class, id_field) == id_val)
                .values(**update_data)
            )
            await db.execute(stmt)
        
        await db.flush()
        total_updated += len(batch)
        logger.debug(f"Updated batch of {len(batch)} items")
    
    return total_updated


# ============================================================================
# ASYNC CONTEXT MANAGERS
# ============================================================================

class AsyncResourcePool:
    """Manage pool of async resources"""
    
    def __init__(self, factory: Callable, pool_size: int = 10):
        self.factory = factory
        self.pool_size = pool_size
        self.available: asyncio.Queue = asyncio.Queue(maxsize=pool_size)
        self.initialized = False
    
    async def initialize(self) -> None:
        """Initialize the resource pool"""
        for _ in range(self.pool_size):
            resource = await self.factory()
            await self.available.put(resource)
        self.initialized = True
        logger.info(f"Resource pool initialized with {self.pool_size} items")
    
    async def acquire(self) -> Any:
        """Acquire a resource from the pool"""
        if not self.initialized:
            await self.initialize()
        return await self.available.get()
    
    async def release(self, resource: Any) -> None:
        """Return a resource to the pool"""
        await self.available.put(resource)
    
    async def close_all(self) -> None:
        """Close all resources in pool"""
        while not self.available.empty():
            try:
                resource = self.available.get_nowait()
                if hasattr(resource, 'close'):
                    await resource.close()
            except asyncio.QueueEmpty:
                break
