"""
Resolution API Routes
Manages user fitness resolutions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User
from models.resolution import ResolutionStatus
from schemas.resolution_schema import (
    CreateResolutionRequest,
    ResolutionResponse,
    ResolutionListResponse,
    UpdateProgressRequest,
    ModifyResolutionRequest,
    ResolutionInsightsResponse,
    ConfirmResolutionRequest
)
from services.resolution_service import ResolutionService
from memory.agent_memory import AgentMemory


router = APIRouter(prefix="/resolution", tags=["Resolution"])


@router.post("/create", response_model=ResolutionResponse, status_code=status.HTTP_201_CREATED)
async def create_resolution(
    request: CreateResolutionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new fitness resolution.
    
    Runs the OnboardingWorkflow to:
    1. Analyze user's goal
    2. Identify failure patterns
    3. Generate AI-optimized plan
    4. Run multi-agent debate
    5. Store resolution with plan
    """
    try:
        # Check if user already has an active resolution
        existing = await ResolutionService.get_active_resolution(current_user.id, db)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have an active resolution. Complete or abandon it first."
            )
        
        # Create resolution (runs workflow)
        resolution = await ResolutionService.create_resolution(
            user_id=current_user.id,
            resolution_text=request.resolution_text,
            past_attempts=request.past_attempts,
            life_constraints=request.life_constraints,
            db=db
        )
        
        return ResolutionResponse.model_validate(resolution)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create resolution: {str(e)}"
        )
    
    
@router.post("/confirm", response_model=ResolutionResponse, status_code=status.HTTP_201_CREATED)
async def confirm_resolution(
    request: ConfirmResolutionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Confirm and save a resolution from onboarding.
    Does NOT re-run the AI workflow.
    """
    try:
        # Check if user already has an active resolution
        existing = await ResolutionService.get_active_resolution(current_user.id, db)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have an active resolution. Complete or abandon it first."
            )
            
        # Update user occupation if provided
        if request.occupation:
            current_user.occupation = request.occupation
        if request.occupation_details:
            current_user.occupation_details = request.occupation_details
            
        # Create resolution directly
        resolution = await ResolutionService.confirm_resolution(
            user_id=current_user.id,
            resolution_text=request.resolution_text,
            final_plan=request.final_plan,
            db=db,
            past_attempts=request.past_attempts,
            life_constraints=request.life_constraints,
            debate_summary=request.debate_summary,
            confidence_score=request.confidence_score
        )
        
        return ResolutionResponse.model_validate(resolution)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to confirm resolution: {str(e)}"
        )


@router.get("/active", response_model=ResolutionResponse)
async def get_active_resolution(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's currently active resolution"""
    resolution = await ResolutionService.get_active_resolution(current_user.id, db)
    
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active resolution found"
        )
    
    return ResolutionResponse.model_validate(resolution)


@router.get("/list", response_model=ResolutionListResponse)
async def list_resolutions(
    status_filter: Optional[ResolutionStatus] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all user's resolutions"""
    resolutions = await ResolutionService.list_resolutions(
        current_user.id,
        status_filter,
        db
    )
    
    stats = await ResolutionService.get_statistics(current_user.id, db)
    
    return ResolutionListResponse(
        resolutions=[ResolutionResponse.model_validate(r) for r in resolutions],
        total=stats["total"],
        active_count=stats["active"],
        completed_count=stats["completed"]
    )


@router.get("/{resolution_id}", response_model=ResolutionResponse)
async def get_resolution(
    resolution_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific resolution by ID"""
    resolution = await ResolutionService.get_resolution(
        resolution_id,
        current_user.id,
        db
    )
    
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resolution not found"
        )
    
    return ResolutionResponse.model_validate(resolution)


@router.put("/{resolution_id}/progress", response_model=ResolutionResponse)
async def update_progress(
    resolution_id: int,
    request: UpdateProgressRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update resolution progress"""
    try:
        resolution = await ResolutionService.update_progress(
            resolution_id=resolution_id,
            user_id=current_user.id,
            workouts_completed=request.workouts_completed,
            current_week=request.current_week,
            adherence_rate=request.adherence_rate,
            streak_days=request.streak_days,
            db=db
        )
        
        return ResolutionResponse.model_validate(resolution)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{resolution_id}/complete", response_model=ResolutionResponse)
async def complete_resolution(
    resolution_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark resolution as completed"""
    try:
        resolution = await ResolutionService.mark_completed(
            resolution_id,
            current_user.id,
            db
        )
        
        return ResolutionResponse.model_validate(resolution)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{resolution_id}/abandon", response_model=ResolutionResponse)
async def abandon_resolution(
    resolution_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark resolution as abandoned"""
    try:
        resolution = await ResolutionService.mark_abandoned(
            resolution_id,
            current_user.id,
            db
        )
        
        return ResolutionResponse.model_validate(resolution)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{resolution_id}/insights", response_model=ResolutionInsightsResponse)
async def get_resolution_insights(
    resolution_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get AI insights about resolution.
    
    Returns:
    - What AI learned about user
    - Failure predictions
    - Recommendations
    """
    resolution = await ResolutionService.get_resolution(
        resolution_id,
        current_user.id,
        db
    )
    
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resolution not found"
        )
    
    # Load memory insights
    memory_data = await AgentMemory.load_to_state(
        user_id=current_user.id,
        db=db,
        state_type="insights"
    )
    
    # Extract insights
    insights = []
    for memory in memory_data.get("all", []):
        if memory["learning_type"] == "failure_pattern":
            content = memory["content"]
            insights.append(f"Pattern detected: {content.get('patterns', [])}")
    
    # Predictions
    predictions = {
        "abandonment_probability": resolution.abandonment_probability,
        "highest_risk_week": resolution.current_week + 2,  # Simple prediction
        "confidence": 0.75
    }
    
    # Recommendations
    recommendations = []
    if resolution.adherence_rate < 0.7:
        recommendations.append("Consider reducing workout frequency to build consistency")
    if resolution.abandonment_probability > 0.5:
        recommendations.append("High risk of abandonment - intervention recommended")
    
    return ResolutionInsightsResponse(
        resolution_id=resolution.id,
        insights=insights,
        predictions=predictions,
        recommendations=recommendations,
        confidence=0.75
    )


@router.get("/stats/summary")
async def get_stats_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's resolution statistics"""
    stats = await ResolutionService.get_statistics(current_user.id, db)
    return stats
