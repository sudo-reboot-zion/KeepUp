# api/routes/workout.py

"""
Workout API Routes
Handles workout modification requests
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from api.dependencies import get_db, get_current_user
from agents.adaptive_intervention.workout_modification_agent import workout_modification_agent
from models.user import User
from models.workout import WorkoutModificationResponse, WorkoutModificationRequest
from services.safety_guardrails import SafetyGuardrails, AlertLevel

router = APIRouter(prefix="/api/workout", tags=["workout"])





@router.post("/modify", response_model=WorkoutModificationResponse)
async def modify_workout(
    request: WorkoutModificationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Modify a workout plan for safety based on user profile and context.
    
    The Workout Modification Agent will:
    1. Assess risks (injuries, fatigue, fitness level)
    2. Query knowledge base for safety guidelines
    3. Modify exercises if needed
    4. Provide transparent reasoning
    
    **Example Request:**
```json
    {
        "workout_plan": [
            {
                "name": "Barbell Back Squat",
                "sets": 4,
                "reps": 8,
                "weight_lbs": 185,
                "rest_seconds": 120
            },
            {
                "name": "Overhead Press",
                "sets": 3,
                "reps": 10,
                "weight_lbs": 95,
                "rest_seconds": 90
            }
        ],
        "context": {
            "sleep_hours": 5,
            "stress_level": "high",
            "days_since_last_workout": 3
        }
    }
```
    """
    try:
        # Get user profile from database
        from services.user_service import UserService
        user_profile = await UserService.get_user_profile(current_user.id, db)
        
        # PHASE 3: Check overtraining risk
        guardrails = SafetyGuardrails(db)
        total_duration = sum([ex.duration_minutes for ex in request.workout_plan if hasattr(ex, 'duration_minutes')]) or 60
        intensity = request.context.get('intensity', 'moderate') if request.context else 'moderate'
        
        overtraining_alerts = guardrails.check_overtraining_risk(
            resolution_id=current_user.active_resolution_id if hasattr(current_user, 'active_resolution_id') else None,
            proposed_workout_minutes=total_duration,
            proposed_intensity=intensity
        )
        
        blocked = [a for a in overtraining_alerts if a.level == AlertLevel.BLOCKED]
        if blocked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Workout blocked: {blocked[0].message}"
            )
        
        # Convert request to dict for agent
        workout_plan = [ex.model_dump() for ex in request.workout_plan]
        
        # Prepare input for agent
        agent_input = {
            "user_profile": user_profile,
            "workout_plan": workout_plan,
            "context": request.context,
            "overtraining_warnings": [a.message for a in overtraining_alerts if a.level == AlertLevel.WARNING]
        }
        
        # Call agent
        result = await workout_modification_agent.analyze(agent_input)
        
        return WorkoutModificationResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workout modification failed: {str(e)}"
        )


@router.get("/example")
async def get_example_workout():
    """
    Get an example workout plan for testing.
    Useful for frontend developers.
    """
    return {
        "workout_plan": [
            {
                "name": "Barbell Back Squat",
                "sets": 4,
                "reps": 8,
                "weight_lbs": 185,
                "rest_seconds": 120,
                "notes": "Focus on depth and knee tracking"
            },
            {
                "name": "Romanian Deadlift",
                "sets": 3,
                "reps": 10,
                "weight_lbs": 135,
                "rest_seconds": 90,
                "notes": "Keep back neutral"
            },
            {
                "name": "Overhead Press",
                "sets": 3,
                "reps": 10,
                "weight_lbs": 95,
                "rest_seconds": 90,
                "notes": "Full lockout at top"
            }
        ],
        "context": {
            "sleep_hours": 7,
            "stress_level": "moderate",
            "days_since_last_workout": 2
        }
    }
