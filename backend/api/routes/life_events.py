"""
Life Events API Routes
Track major life changes that affect health goals
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User


router = APIRouter(prefix="/life-events", tags=["Life Events"])


class LifeEventCreate(BaseModel):
    event_type: str  # "job_change", "moving", "relationship", "health", "family"
    description: str
    impact_level: str  # "low", "medium", "high"
    start_date: Optional[datetime] = None


class LifeEventResponse(BaseModel):
    id: int
    user_id: int
    event_type: str
    description: str
    impact_level: str
    start_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


from agents.contextual_awareness.life_event_agent import LifeEventAgent
from models.life_event import LifeEvent, EventType, ImpactLevel

@router.post("/", response_model=LifeEventResponse)
async def create_life_event(
    event: LifeEventCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Record a major life event and analyze its impact
    """
    # Create event record
    db_event = LifeEvent(
        user_id=current_user.id,
        event_type=event.event_type,
        description=event.description,
        impact_level=event.impact_level,
        start_date=event.start_date or datetime.now()
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    
    # Analyze impact with Agent
    agent = LifeEventAgent()
    analysis = await agent.analyze({
        "event_type": event.event_type,
        "description": event.description,
        "impact_level": event.impact_level,
        "user_profile": {
            "occupation": current_user.occupation,
            "goals": [] # TODO: Get goals
        }
    })
    
    # TODO: Store analysis/recommendations
    
    return db_event


@router.get("/", response_model=List[LifeEventResponse])
async def get_life_events(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all life events for current user
    """
    # TODO: Query from database
    return []


@router.get("/active")
async def get_active_life_events(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get currently active life events affecting the user
    """
    # TODO: Query active events (within last 3 months)
    return {"active_events": []}
