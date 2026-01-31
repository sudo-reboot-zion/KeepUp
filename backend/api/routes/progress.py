# api/routes/progress.py

"""
Progress Tracking API Routes
Analyzes user adherence and patterns
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

from api.dependencies import get_db, get_current_user
from agents.resolution_tracking.progress_tracking_agent import progress_tracking_agent
from models.user import User

router = APIRouter(prefix="/api/progress", tags=["progress"])


# ============================================================================
# REQUEST/RESPONSE SCHEMAS
# ============================================================================

class ProgressAnalysisRequest(BaseModel):
    """Request body for progress analysis"""
    current_week: int = Field(ge=1, description="Current week of resolution")
    workouts_completed: int = Field(ge=0, description="Workouts completed this week")
    workouts_target: int = Field(ge=1, description="Target workouts per week")
    skip_pattern: List[bool] = Field(
        default_factory=list,
        description="Last 14 days: True=completed, False=skipped"
    )


class ProgressAnalysisResponse(BaseModel):
    """Response from progress analysis"""
    analysis: Dict[str, Any]
    metrics: Dict[str, Any]
    agent_name: str
    confidence: float


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/analyze", response_model=ProgressAnalysisResponse)
async def analyze_progress(
    request: ProgressAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze user's workout adherence and detect patterns.
    
    The Progress Tracking Agent will:
    1. Calculate adherence metrics
    2. Identify skip patterns and streaks
    3. Assess trend (improving/stable/declining)
    4. Reference habit formation research
    5. Provide recommendations
    
    **Example Request:**
```json
    {
        "current_week": 3,
        "workouts_completed": 2,
        "workouts_target": 3,
        "skip_pattern": [true, false, true, true, false, false, true, true, true, false, true, false, true, true]
    }
```
    """
    try:
        # Get user profile
        from services.user_service import UserService
        user_profile = await UserService.get_user_profile(current_user.id, db)
        
        # Calculate adherence rate
        adherence_rate = (
            request.workouts_completed / request.workouts_target 
            if request.workouts_target > 0 else 0.0
        )
        
        # Prepare input for agent
        agent_input = {
            "current_week": request.current_week,
            "workouts_completed": request.workouts_completed,
            "workouts_target": request.workouts_target,
            "adherence_rate": adherence_rate,
            "skip_pattern": request.skip_pattern,
            "user_profile": user_profile
        }
        
        # Call agent
        result = await progress_tracking_agent.analyze(agent_input)
        
        return ProgressAnalysisResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Progress analysis failed: {str(e)}"
        )


@router.get("/example")
async def get_example_progress():
    """Example progress data for testing"""
    return {
        "current_week": 3,
        "workouts_completed": 2,
        "workouts_target": 3,
        "skip_pattern": [
            True, False, True,   # Week 1
            True, True, False,   # Week 2
            True, False, True,   # Week 3 (partial)
            True, True, False,
            False, False
        ]
    }


@router.get("/me/current")
async def get_my_current_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's progress data.
    TODO: Implement actual database queries for workout history.
    """
    # TODO: Query workout_sessions table for user's actual data
    # For now, return mock data
    return {
        "user_id": current_user.id,
        "current_week": 2,
        "workouts_this_week": 2,
        "target_per_week": 3,
        "adherence_rate": 0.67,
        "message": "TODO: Connect to actual workout tracking data"
    }