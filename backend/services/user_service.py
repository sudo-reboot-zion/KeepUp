from typing import Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession



class UserService:
    """Service for user-related operations"""
    
    @staticmethod
    async def get_user(user_id: int, db: AsyncSession) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_profile(user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get user profile data for agents"""
        user = await UserService.get_user(user_id, db)
        
        if not user:
            return {}
        
        return {
            "age": user.age,
            "gender": user.gender,
            "tracks_cycle": user.tracks_menstrual_cycle,
            "cycle_day": user.cycle_day,
            "last_period_date": user.last_period_date
        }
    
    @staticmethod
    async def update_health_tracking(
        user_id: int,
        db: AsyncSession,
        cycle_day: Optional[int] = None,
        tracks_cycle: Optional[bool] = None
    ) -> Optional[User]:
        """Update user health tracking info"""
        user = await UserService.get_user(user_id, db)
        
        if not user:
            return None
        
        if cycle_day is not None:
            user.cycle_day = cycle_day
        
        if tracks_cycle is not None:
            user.tracks_menstrual_cycle = tracks_cycle
        
        await db.commit()
        await db.refresh(user)
        return user
