"""
Database Optimization & Indexing Utilities
Provides batch operations, query optimization, and index management
"""

from typing import List, Dict, Any, Optional, TypeVar, Generic
from sqlalchemy import text, Index
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class BatchOperationManager(Generic[T]):
    """Manages batch database operations for better performance"""
    
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self.batch: List[T] = []
    
    def add(self, item: T) -> None:
        """Add item to batch"""
        self.batch.append(item)
    
    def add_many(self, items: List[T]) -> None:
        """Add multiple items to batch"""
        self.batch.extend(items)
    
    async def flush(self, db: AsyncSession) -> int:
        """Flush batch to database"""
        if not self.batch:
            return 0
        
        count = len(self.batch)
        try:
            db.add_all(self.batch)
            await db.flush()
            logger.info(f"Batch operation: Added {count} items")
            self.batch = []
            return count
        except Exception as e:
            logger.error(f"Batch operation error: {e}")
            raise
    
    async def process(self, db: AsyncSession, callback=None) -> int:
        """
        Process batch automatically when it reaches batch_size
        Useful for large operations
        """
        total = 0
        for item in self.batch:
            if callback:
                item = callback(item)
            
            if len(self.batch) >= self.batch_size:
                total += await self.flush(db)
        
        if self.batch:
            total += await self.flush(db)
        
        return total
    
    def clear(self) -> None:
        """Clear batch without flushing"""
        self.batch = []
    
    def __len__(self) -> int:
        return len(self.batch)


class QueryOptimizer:
    """Utilities for optimizing database queries"""
    
    @staticmethod
    def with_eager_loading(query, *relationships):
        """
        Add eager loading to prevent N+1 queries
        
        Usage:
            query = select(User)
            optimized = QueryOptimizer.with_eager_loading(
                query,
                User.resolutions,
                User.daily_logs
            )
        """
        for relationship in relationships:
            query = query.options(selectinload(relationship))
        return query
    
    @staticmethod
    def with_joined_loading(query, *relationships):
        """
        Add joined loading for related data
        Use when you need ALL columns from joined table
        """
        for relationship in relationships:
            query = query.options(joinedload(relationship))
        return query
    
    @staticmethod
    def paginate(query, page: int = 1, page_size: int = 20):
        """Add pagination to query"""
        offset = (page - 1) * page_size
        return query.offset(offset).limit(page_size)
    
    @staticmethod
    async def count_with_cache(
        db: AsyncSession,
        model,
        use_cache: bool = True
    ) -> int:
        """
        Count items efficiently
        Returns count, using cache if available
        """
        stmt = select(func.count()).select_from(model)
        result = await db.execute(stmt)
        return result.scalar()


class IndexManagement:
    """Manage database indexes for query optimization"""
    
    # Define indexes for common queries
    RECOMMENDED_INDEXES = [
        # User queries
        ("users", ["email"], "idx_users_email"),
        ("users", ["id", "created_at"], "idx_users_id_created"),
        
        # Resolution queries
        ("resolutions", ["user_id"], "idx_resolutions_user_id"),
        ("resolutions", ["user_id", "created_at"], "idx_resolutions_user_created"),
        
        # Biometric reading queries
        ("biometric_readings", ["resolution_id"], "idx_biometric_resolution"),
        ("biometric_readings", ["resolution_id", "timestamp"], "idx_biometric_resolution_time"),
        
        # Daily workout queries
        ("daily_workouts", ["weekly_plan_id"], "idx_workout_weekly"),
        ("daily_workouts", ["user_id", "date"], "idx_workout_user_date"),
        
        # Weekly plan queries
        ("weekly_plans", ["quarterly_phase_id"], "idx_weekly_quarterly"),
        ("weekly_plans", ["user_id", "week_number"], "idx_weekly_user_week"),
        
        # Quarterly phase queries
        ("quarterly_phases", ["resolution_id"], "idx_quarterly_resolution"),
        
        # Daily log queries
        ("daily_logs", ["user_id", "date"], "idx_daily_log_user_date"),
        
        # Safety-related queries
        ("biometric_readings", ["systolic", "diastolic"], "idx_biometric_bp"),
        ("biometric_readings", ["heart_rate"], "idx_biometric_hr"),
        
        # Alert acknowledgment queries
        ("alert_acknowledgments", ["user_id", "timestamp"], "idx_alert_user_time"),
    ]
    
    @staticmethod
    async def create_indexes(engine) -> None:
        """Create recommended indexes on database"""
        async with engine.begin() as conn:
            for table, columns, index_name in IndexManagement.RECOMMENDED_INDEXES:
                try:
                    # Create index
                    columns_str = ", ".join(columns)
                    query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table}({columns_str})"
                    await conn.execute(text(query))
                    logger.info(f"✓ Index created: {index_name}")
                except Exception as e:
                    logger.warning(f"Index creation failed ({index_name}): {e}")
    
    @staticmethod
    async def analyze_tables(engine) -> None:
        """
        Analyze table statistics for query optimization
        Helps database optimizer make better decisions
        """
        tables = [
            "users", "resolutions", "biometric_readings",
            "daily_workouts", "weekly_plans", "quarterly_phases",
            "daily_logs", "alert_acknowledgments"
        ]
        
        async with engine.begin() as conn:
            for table in tables:
                try:
                    await conn.execute(text(f"ANALYZE {table}"))
                    logger.info(f"✓ Table analyzed: {table}")
                except Exception as e:
                    logger.warning(f"Table analysis failed ({table}): {e}")
    
    @staticmethod
    async def check_missing_indexes(engine) -> List[Dict[str, Any]]:
        """
        Check for missing indexes on frequently used columns
        Returns list of suggested indexes
        """
        suggestions = []
        
        try:
            async with engine.begin() as conn:
                # Get unused indexes
                result = await conn.execute(text("""
                    SELECT schemaname, tablename, indexname
                    FROM pg_indexes
                    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                """))
                
                for row in result:
                    suggestions.append({
                        "table": row[1],
                        "index": row[2],
                        "status": "exists"
                    })
        except Exception as e:
            logger.warning(f"Could not check indexes: {e}")
        
        return suggestions


class QueryMetrics:
    """Track and log query performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}
    
    def log_query(
        self,
        query_name: str,
        execution_time: float,
        rows_affected: int = 0,
        success: bool = True
    ) -> None:
        """Log a query execution"""
        if query_name not in self.metrics:
            self.metrics[query_name] = {
                "total_time": 0,
                "count": 0,
                "errors": 0,
                "avg_time": 0,
                "max_time": 0,
                "rows_total": 0,
            }
        
        metric = self.metrics[query_name]
        
        if success:
            metric["total_time"] += execution_time
            metric["count"] += 1
            metric["rows_total"] += rows_affected
            metric["max_time"] = max(metric["max_time"], execution_time)
            metric["avg_time"] = metric["total_time"] / metric["count"]
        else:
            metric["errors"] += 1
        
        # Log slow queries
        if execution_time > 1.0:  # Queries slower than 1 second
            logger.warning(
                f"Slow query: {query_name} took {execution_time:.2f}s"
            )
    
    def get_metrics(self, query_name: str = None) -> Dict[str, Any]:
        """Get metrics for a query or all queries"""
        if query_name:
            return self.metrics.get(query_name, {})
        return self.metrics
    
    def get_top_slow_queries(self, limit: int = 10) -> List[tuple]:
        """Get top slowest queries"""
        sorted_metrics = sorted(
            self.metrics.items(),
            key=lambda x: x[1]["avg_time"],
            reverse=True
        )
        return sorted_metrics[:limit]


# Global metrics tracker
query_metrics = QueryMetrics()


# ============================================================================
# QUERY TEMPLATES FOR COMMON OPERATIONS
# ============================================================================

class OptimizedQueries:
    """Pre-optimized queries for common operations"""
    
    @staticmethod
    async def get_user_with_relations(
        db: AsyncSession,
        user_id: int
    ):
        """Get user with all related data efficiently"""
        from models.user import User
        from models.resolution import Resolution
        from models.daily_log import UserDailyLog
        
        query = select(User).where(User.id == user_id)
        query = QueryOptimizer.with_eager_loading(
            query,
            User.resolutions,
            User.daily_logs
        )
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_resolution_with_hierarchy(
        db: AsyncSession,
        resolution_id: int
    ):
        """Get resolution with full quarterly/weekly/daily hierarchy"""
        from models.resolution import Resolution
        from models.quarterly_phase import QuarterlyPhase
        from models.weekly_plan import WeeklyPlan
        from models.daily_workout import DailyWorkout
        
        query = select(Resolution).where(Resolution.id == resolution_id)
        query = QueryOptimizer.with_eager_loading(
            query,
            Resolution.quarterly_phases.and_(
                lambda qp: selectinload(
                    QuarterlyPhase.weekly_plans
                ).selectinload(WeeklyPlan.daily_workouts)
            )
        )
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_daily_workout_batch(
        db: AsyncSession,
        resolution_id: int,
        limit: int = 20,
        offset: int = 0
    ):
        """Get daily workouts with pagination"""
        from models.daily_workout import DailyWorkout
        
        query = (
            select(DailyWorkout)
            .where(DailyWorkout.resolution_id == resolution_id)
            .order_by(DailyWorkout.date.desc())
            .offset(offset)
            .limit(limit)
        )
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_biometric_readings_range(
        db: AsyncSession,
        resolution_id: int,
        days_back: int = 30
    ):
        """Get biometric readings for date range efficiently"""
        from models.biometric_reading import BiometricReading
        from datetime import datetime, timedelta
        
        start_date = datetime.utcnow() - timedelta(days=days_back)
        
        query = (
            select(BiometricReading)
            .where(
                (BiometricReading.resolution_id == resolution_id) &
                (BiometricReading.timestamp >= start_date)
            )
            .order_by(BiometricReading.timestamp.desc())
        )
        
        result = await db.execute(query)
        return result.scalars().all()


from sqlalchemy import func
