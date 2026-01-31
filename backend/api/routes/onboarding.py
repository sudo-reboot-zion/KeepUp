from sqlalchemy.ext.asyncio import AsyncSession
from schemas.onboarding_schema import OnboardingRequest, OnboardingResponse
from models.user import User
from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_current_user
from core.database import get_db
from workflows.onboarding_workflow import OnboardingWorkflow
from agents.coordination.chat_agent import chat_agent
from typing import Dict, Any, List


router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.get("/")
async def onboarding_status():
    return {"message": "Onboarding route working"}


@router.post("/step")
async def onboarding_conversational_step(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """
    Handle a single conversational step in the onboarding process.
    """
    message = request.get("message", "")
    extracted_data = request.get("extracted_data", {})
    
    response = await chat_agent.respond(
        user_id=str(current_user.id),
        message=message,
        context={
            "stage": "onboarding",
            "extracted_data": extracted_data
        }
    )
    
    return response


@router.post("/start", response_model=OnboardingResponse) 
async def start_onboarding(
    request: OnboardingRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Start onboarding workflow - runs multi-agent debate
    """
    try:
        # Check if user has already completed onboarding
        if current_user.has_completed_onboarding:
            raise HTTPException(
                status_code=400, 
                detail="You have already completed onboarding. To update your goals or preferences, please visit the Settings page."
            )
        
        workflow = OnboardingWorkflow()

        initial_state = {
            "user_id": str(current_user.id),
            "primary_goal": request.primary_goal,  # NEW
            "goal_details": request.goal_details,  # NEW
            "resolution_text": request.goal_details,  # Use goal_details as resolution_text
            "past_attempts": request.past_attempts,
            "life_constraints": request.life_constraints or [],
            "occupation": request.occupation,
            "occupation_details": request.occupation_details,
            "goal_analysis": None,
            "failure_risk": None,
            "final_plan": None,
            "confidence_score": None,
            "timestamp": None,
            "errors": None,
            "_user_profile": None
        }

        result = await workflow.run(initial_state, db)
        
        # Mark user as having completed onboarding
        current_user.has_completed_onboarding = True
        
        # Store primary goal (MVP Core Feature)
        current_user.primary_goal = request.primary_goal
        current_user.goal_details = {
            "details": request.goal_details,
            "past_attempts": request.past_attempts,
            "life_constraints": request.life_constraints
        }
        from datetime import datetime, timezone
        current_user.goal_set_at = datetime.now(timezone.utc)
        
        # NEW: Create the actual Resolution record to unblock Dashboard
        from services.resolution_service import ResolutionService
        await ResolutionService.confirm_resolution(
            user_id=current_user.id,
            resolution_text=request.goal_details,
            final_plan=result["final_plan"],
            db=db,
            past_attempts=request.past_attempts,
            life_constraints=request.life_constraints,
            debate_summary=result.get("debate_summary"),
            confidence_score=result["confidence_score"]
        )
        
        # Save occupation data if provided
        if request.occupation:
            current_user.occupation = request.occupation
        if request.occupation_details:
            current_user.occupation_details = request.occupation_details
            
        await db.commit()
        
        return OnboardingResponse(
            final_plan=result["final_plan"],
            debate_summary=result.get("debate_summary", {}),
            confidence_score=result["confidence_score"]
        ) 

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"❌ ONBOARDING ERROR: {str(e)}")
        print(f"❌ TRACEBACK:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_onboarding_status(
    current_user: User = Depends(get_current_user)
):
    """
    Check if user has completed onboarding
    """
    return {
        "has_completed_onboarding": current_user.has_completed_onboarding,
        "user_id": current_user.id
    }
