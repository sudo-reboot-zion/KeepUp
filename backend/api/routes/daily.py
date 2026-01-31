from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from datetime import datetime

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User
from workflows.daily_check_workflow import DailyCheckWorkflow
from schemas.daily_plan_schema import DailyPlanRequest, DailyPlanResponse
from services.safety_guardrails import SafetyGuardrails, AlertLevel


router = APIRouter(prefix="/daily", tags=["Daily"])


@router.get("/plan", response_model=DailyPlanResponse)
async def get_daily_plan(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate today's adaptive workout plan.
    
    Uses multi-agent workflow to:
    - Analyze sleep/recovery
    - Check schedule conflicts
    - Generate safe workout
    - Adapt to user's current state
    """
    try:
        # Initialize workflow
        workflow = DailyCheckWorkflow()
        
        # Prepare initial state
        # In production, these would come from:
        # - Wearable API (sleep_data)
        # - Google Calendar API (calendar_events)
        # - Database (recent_workouts)

        initial_state = {
            "user_id": str(current_user.id),
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            
            # Initialize empty containers
            "checkin_data": {},
            "calendar_events": [],
            "recent_workouts": [],
            
            "stress_score": None, # Will be filled by workflow
            "biometric_analysis": {},
            "schedule_conflicts": [],
            
            "workout_plan": {},
            "adaptations": [],
            "daily_plan": {},
            
            "confidence_score": 0.0,
            "timestamp": None,
            "errors": [],
            
            # Internal only
            "_user_profile": {}
        }

        
        # Run workflow
        result = await workflow.run(initial_state, db)
        
        # Check for errors
        if errors := result.get("errors"):
            raise HTTPException(
                status_code=500,
                detail=f"Workflow errors: {', '.join(errors)}"
            )
        
        # Extract daily plan
        daily_plan = result.get("daily_plan", {})
        
        # PHASE 3: Check confidence and add disclaimers
        guardrails = SafetyGuardrails(db)
        confidence_score = result.get("confidence_score", 0.75)
        safe, conf_alert = guardrails.check_recommendation_confidence(confidence_score)
        
        if not safe:
            raise HTTPException(
                status_code=400,
                detail=f"Daily plan confidence too low: {conf_alert.message}"
            )
        
        # Add medical disclaimer for recovery/rest recommendations
        workout_type = daily_plan.get("type", "standard") if daily_plan else "standard"
        if workout_type in ["recovery", "rest", "mobility"]:
            disclaimer = guardrails.check_medical_disclaimer_needed("recovery_focus")
            if disclaimer:
                daily_plan["medical_disclaimer"] = disclaimer
        
        # Add confidence warning if applicable
        if conf_alert:
            daily_plan["confidence_warning"] = conf_alert.message
        
        if not daily_plan:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate daily plan"
            )
        
        # Format response
        return DailyPlanResponse(
            date=daily_plan.get("date"),
            workout=daily_plan.get("workout", {}),
            adaptations_made=daily_plan.get("adaptations_made", []),
            schedule_notes=daily_plan.get("schedule_notes", []),
            readiness_score=daily_plan.get("readiness_score", 0.0),
            confidence=daily_plan.get("confidence", 0.0),
            generated_at=result.get("timestamp")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating daily plan: {str(e)}"
        )


@router.post("/plan/custom")
async def get_custom_plan(
    request: DailyPlanRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate custom plan with provided context.
    
    Allows frontend to pass:
    - Sleep data from wearable
    - Calendar events
    - Stress level
    """
    try:
        workflow = DailyCheckWorkflow()
        
        initial_state = {
            "user_id": str(current_user.id),
            "current_date": request.date or datetime.now().strftime("%Y-%m-%d"),
            "sleep_data": request.sleep_data,
            "calendar_events": request.calendar_events or [],
            "recent_workouts": [],  # TODO: Fetch from database
            "stress_score": request.stress_score,
            "biometric_analysis": None,
            "schedule_conflicts": None,
            "motivation_level": None,
            "workout_plan": None,
            "adaptations": None,
            "daily_plan": None,
            "confidence_score": None,
            "timestamp": None,
            "errors": None,
            "_user_profile": None
        }
        
        result = await workflow.run(initial_state, db)
        
        if errors := result.get("errors"):
            raise HTTPException(
                status_code=500,
                detail=f"Workflow errors: {', '.join(errors)}"
            )
        
        daily_plan = result.get("daily_plan", {})
        
        return DailyPlanResponse(
            date=daily_plan.get("date"),
            workout=daily_plan.get("workout", {}),
            adaptations_made=daily_plan.get("adaptations_made", []),
            schedule_notes=daily_plan.get("schedule_notes", []),
            readiness_score=daily_plan.get("readiness_score", 0.0),
            confidence=daily_plan.get("confidence", 0.0),
            generated_at=result.get("timestamp")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating custom plan: {str(e)}"
        )


@router.get("/status")
async def daily_status(current_user: User = Depends(get_current_user)):
    """Check if daily plan is available"""
    return {
        "available": True,
        "message": "Daily plan generation ready",
        "user_id": current_user.id
    }