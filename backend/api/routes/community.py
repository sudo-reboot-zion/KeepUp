"""
Community API Routes
Endpoints for Challenges, Tribes, and The Pulse.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User
from models.challenge import Challenge, UserChallenge
from agents.coordination.community_agent import community_agent

router = APIRouter(prefix="/community", tags=["Community"])

@router.get("/challenges/active")
async def get_active_challenges(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get active challenges for the user's tribe (primary goal)"""
    # 1. Get user's tribe/goal
    tribe = current_user.primary_goal or "wellness"
    
    # 2. Find active challenges for this category
    result = await db.execute(
        select(Challenge).where(Challenge.category == tribe)
    )
    challenges = result.scalars().all()
    
    # 3. If none, generate one on the fly (MVP Magic)
    if not challenges:
        new_challenge_data = await community_agent.generate_challenge(tribe, active_users_count=124)
        
        # Save to DB (Simplified for MVP)
        # In real app, we'd map the JSON to the Model
        # For now, return the generated data directly so frontend has something
        return [new_challenge_data]
        
    return challenges

@router.post("/challenges/{challenge_id}/join")
async def join_challenge(
    challenge_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Join a challenge"""
    # Check if already joined
    existing = await db.execute(
        select(UserChallenge).where(
            UserChallenge.user_id == current_user.id,
            UserChallenge.challenge_id == challenge_id
        )
    )
    if existing.scalar_one_or_none():
        return {"status": "already_joined"}
        
    # Join
    join_entry = UserChallenge(
        user_id=current_user.id,
        challenge_id=challenge_id,
        status="active"
    )
    db.add(join_entry)
    await db.commit()
    
    return {"status": "joined", "message": "Welcome to the tribe!"}

@router.get("/pulse")
async def get_community_pulse(
    current_user: User = Depends(get_current_user)
):
    """Get the 'Pulse' update (activity summary)"""
    # In real app, fetch recent activity from DB
    # For MVP, ask Agent to generate based on mock stats
    pulse = await community_agent.generate_pulse_update(recent_activities=[{}, {}, {}])
    return {"pulse_text": pulse}
