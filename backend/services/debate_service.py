# services/debate_service.py

"""
Debate Service - Stores and retrieves agent debates
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


class DebateService:
    """Service for managing agent debates"""
    
    @staticmethod
    async def create_debate_record(
        db: AsyncSession,
        user_id: int,
        debate_type: str,
        debate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Store a debate record (onboarding, daily, intervention)
        
        For now, just returns the data. 
        TODO: Add database model for debates later.
        """
        return {
            "user_id": user_id,
            "debate_type": debate_type,
            "timestamp": datetime.utcnow().isoformat(),
            "debate_data": debate_data
        }
    
    @staticmethod
    async def get_user_debates(
        db: AsyncSession,
        user_id: int,
        debate_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get user's debate history
        
        TODO: Query database when debate model exists
        """
        return []


# Export singleton
debate_service = DebateService()
