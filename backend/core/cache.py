"""
Redis Caching Layer for Performance Optimization
Provides decorators and utilities for caching, with TTL and invalidation support
"""

import json
import hashlib
import pickle
from datetime import timedelta
from functools import wraps
from typing import Any, Callable, Optional, Dict, TypeVar, Union
from enum import Enum
import logging

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from core.config import settings

logger = logging.getLogger(__name__)

F = TypeVar('F', bound=Callable[..., Any])


class CacheLevel(str, Enum):
    """Cache time-to-live levels"""
    SHORT = "short"      # 5 minutes
    MEDIUM = "medium"    # 30 minutes
    LONG = "long"        # 1 hour
    VERY_LONG = "very_long"  # 24 hours


class CacheTTL:
    """Default TTL values for different cache levels"""
    SHORT = 300           # 5 minutes
    MEDIUM = 1800        # 30 minutes
    LONG = 3600          # 1 hour
    VERY_LONG = 86400    # 24 hours


class RedisCache:
    """Redis caching backend with support for sync and async operations"""
    
    def __init__(self, url: str = None):
        """Initialize Redis connection"""
        self.redis_url = url or settings.REDIS_URL
        self.client: Optional[redis.Redis] = None
        self.available = REDIS_AVAILABLE and self.redis_url and self.redis_url != "redis://localhost:6379"
        
        if self.available:
            try:
                self.client = redis.from_url(self.redis_url, decode_responses=False)
                # Test connection
                self.client.ping()
                logger.info("✓ Redis cache connected")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}. Caching disabled.")
                self.available = False
                self.client = None
    
    def _serialize(self, obj: Any) -> bytes:
        """Serialize object to bytes using pickle"""
        try:
            return pickle.dumps(obj)
        except Exception as e:
            logger.warning(f"Serialization error: {e}. Falling back to JSON.")
            return json.dumps(obj).encode('utf-8')
    
    def _deserialize(self, data: bytes) -> Any:
        """Deserialize bytes back to object"""
        try:
            return pickle.loads(data)
        except Exception as e:
            logger.warning(f"Deserialization error: {e}")
            return json.loads(data.decode('utf-8'))
    
    def _make_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from prefix and arguments"""
        # Create key from args and kwargs
        key_parts = [prefix]
        
        # Add positional arguments (skip 'self' and 'db')
        for arg in args:
            if arg is not None and arg != 'self':
                key_parts.append(str(arg))
        
        # Add keyword arguments
        for k, v in sorted(kwargs.items()):
            if k not in ['db', 'self']:
                key_parts.append(f"{k}:{v}")
        
        key_str = ":".join(key_parts)
        # Hash long keys
        if len(key_str) > 100:
            hash_suffix = hashlib.md5(key_str.encode()).hexdigest()[:8]
            key_str = f"{prefix}:{hash_suffix}"
        
        return key_str
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.available or not self.client:
            return None
        
        try:
            data = self.client.get(key)
            if data:
                return self._deserialize(data)
        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {e}")
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = CacheTTL.MEDIUM) -> bool:
        """Set value in cache with TTL"""
        if not self.available or not self.client:
            return False
        
        try:
            serialized = self._serialize(value)
            self.client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {e}")
        
        return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.available or not self.client:
            return False
        
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete error for key {key}: {e}")
        
        return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        if not self.available or not self.client:
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
        except Exception as e:
            logger.warning(f"Cache delete pattern error for {pattern}: {e}")
        
        return 0
    
    def clear(self) -> bool:
        """Clear entire cache"""
        if not self.available or not self.client:
            return False
        
        try:
            self.client.flushdb()
            return True
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
        
        return False
    
    def incr(self, key: str) -> int:
        """Increment counter"""
        if not self.available or not self.client:
            return 0
        
        try:
            return self.client.incr(key)
        except Exception as e:
            logger.warning(f"Cache incr error for key {key}: {e}")
        
        return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.available or not self.client:
            return {"available": False}
        
        try:
            info = self.client.info()
            return {
                "available": True,
                "used_memory": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
            }
        except Exception as e:
            logger.warning(f"Cache stats error: {e}")
            return {"available": False}


# Global cache instance
cache = RedisCache()


# ============================================================================
# CACHE DECORATORS
# ============================================================================

def cache_result(
    prefix: str = "cache",
    ttl: int = CacheTTL.MEDIUM,
    key_args: Optional[list] = None
) -> Callable:
    """
    Decorator for caching function results
    
    Usage:
        @cache_result(prefix="medical_thresholds", ttl=CacheTTL.VERY_LONG)
        async def get_medical_thresholds():
            ...
        
        @cache_result(prefix="user_profile", key_args=[1])
        async def get_user_profile(user_id):
            ...
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache._make_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached = cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache HIT: {cache_key}")
                return cached
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cache SET: {cache_key}")
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache._make_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached = cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache HIT: {cache_key}")
                return cached
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cache SET: {cache_key}")
            
            return result
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore
    
    return decorator


def cache_invalidate(*patterns: str) -> Callable:
    """
    Decorator to invalidate cache patterns after function execution
    
    Usage:
        @cache_invalidate("user_profile:*", "user_settings:*")
        async def update_user(user_id: int):
            ...
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            for pattern in patterns:
                cache.delete_pattern(pattern)
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for pattern in patterns:
                cache.delete_pattern(pattern)
            return result
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore
    
    return decorator


# ============================================================================
# CACHE STRATEGIES FOR COMMON PATTERNS
# ============================================================================

class MedicalThresholdsCache:
    """Specialized cache for medical thresholds (rarely change)"""
    PREFIX = "medical_thresholds"
    TTL = CacheTTL.VERY_LONG  # 24 hours
    
    @staticmethod
    def get_key() -> str:
        return "medical_thresholds:defaults"
    
    @staticmethod
    def set(value: Dict[str, Any]) -> None:
        cache.set(MedicalThresholdsCache.get_key(), value, MedicalThresholdsCache.TTL)
    
    @staticmethod
    def get() -> Optional[Dict[str, Any]]:
        return cache.get(MedicalThresholdsCache.get_key())
    
    @staticmethod
    def invalidate() -> None:
        cache.delete(MedicalThresholdsCache.get_key())


class UserProfileCache:
    """Specialized cache for user profiles (moderate TTL)"""
    PREFIX = "user_profile"
    TTL = CacheTTL.LONG  # 1 hour
    
    @staticmethod
    def get_key(user_id: int) -> str:
        return f"user_profile:{user_id}"
    
    @staticmethod
    def set(user_id: int, value: Dict[str, Any]) -> None:
        cache.set(UserProfileCache.get_key(user_id), value, UserProfileCache.TTL)
    
    @staticmethod
    def get(user_id: int) -> Optional[Dict[str, Any]]:
        return cache.get(UserProfileCache.get_key(user_id))
    
    @staticmethod
    def invalidate(user_id: int) -> None:
        cache.delete(UserProfileCache.get_key(user_id))
    
    @staticmethod
    def invalidate_all() -> None:
        cache.delete_pattern(f"{UserProfileCache.PREFIX}:*")


class SafetyReportCache:
    """Specialized cache for safety reports (short TTL for freshness)"""
    PREFIX = "safety_report"
    TTL = CacheTTL.MEDIUM  # 30 minutes
    
    @staticmethod
    def get_key(resolution_id: int) -> str:
        return f"safety_report:{resolution_id}"
    
    @staticmethod
    def set(resolution_id: int, value: Dict[str, Any]) -> None:
        cache.set(SafetyReportCache.get_key(resolution_id), value, SafetyReportCache.TTL)
    
    @staticmethod
    def get(resolution_id: int) -> Optional[Dict[str, Any]]:
        return cache.get(SafetyReportCache.get_key(resolution_id))
    
    @staticmethod
    def invalidate(resolution_id: int) -> None:
        cache.delete(SafetyReportCache.get_key(resolution_id))


class AgentStateCache:
    """Specialized cache for agent state and decisions"""
    PREFIX = "agent_state"
    TTL = CacheTTL.MEDIUM  # 30 minutes
    
    @staticmethod
    def get_key(agent_name: str, context_id: str) -> str:
        return f"agent_state:{agent_name}:{context_id}"
    
    @staticmethod
    def set(agent_name: str, context_id: str, value: Dict[str, Any]) -> None:
        cache.set(AgentStateCache.get_key(agent_name, context_id), value, AgentStateCache.TTL)
    
    @staticmethod
    def get(agent_name: str, context_id: str) -> Optional[Dict[str, Any]]:
        return cache.get(AgentStateCache.get_key(agent_name, context_id))
    
    @staticmethod
    def invalidate(agent_name: str, context_id: str) -> None:
        cache.delete(AgentStateCache.get_key(agent_name, context_id))
    
    @staticmethod
    def invalidate_agent(agent_name: str) -> None:
        cache.delete_pattern(f"{AgentStateCache.PREFIX}:{agent_name}:*")


class DashboardCache:
    """Specialized cache for dashboard data"""
    PREFIX = "dashboard"
    TTL = CacheTTL.SHORT  # 5 minutes
    
    @staticmethod
    def get_key(user_id: int) -> str:
        return f"dashboard:{user_id}"
    
    @staticmethod
    def set(user_id: int, value: Dict[str, Any]) -> None:
        cache.set(DashboardCache.get_key(user_id), value, DashboardCache.TTL)
    
    @staticmethod
    def get(user_id: int) -> Optional[Dict[str, Any]]:
        return cache.get(DashboardCache.get_key(user_id))
    
    @staticmethod
    def invalidate(user_id: int) -> None:
        cache.delete(DashboardCache.get_key(user_id))


import asyncio
