"""
Dashboard API Routes
Hierarchical access to yearly plans: resolution → quarters → weeks → days
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User
from models.resolution import Resolution
from models.quarterly_phase import QuarterlyPhase
from models.weekly_plan import WeeklyPlan
from models.daily_workout import DailyWorkout
from schemas.hierarchy_schema import (
    QuarterlyPhaseResponse,
    QuarterlyPhaseDetailResponse,
    WeeklyPlanResponse,
    WeeklyPlanDetailResponse,
    DailyWorkoutResponse,
    DailyWorkoutDetailResponse,
    DashboardHierarchyResponse,
    YearlyGoalSummary
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=DashboardHierarchyResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get complete dashboard hierarchy for current user.
    
    Returns:
    - Yearly goal summary
    - All 4 quarters (Q1-Q4)
    - Current quarter details with nested weeks
    - Current week details with nested daily workouts
    - Upcoming weeks preview
    """
    
    # Get active resolution
    stmt = select(Resolution).where(
        Resolution.user_id == current_user.id,
        Resolution.status == "active"
    )
    result = await db.execute(stmt)
    resolution = result.scalar_one_or_none()
    
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active resolution found. Start onboarding first."
        )
    
    # Build yearly goal summary
    yearly_goal = YearlyGoalSummary(
        id=resolution.id,
        resolution_id=resolution.id,
        resolution_text=resolution.resolution_text,
        target_completion_date="2026-12-31",  # TODO: Make dynamic
        current_week=resolution.current_week,
        progress_percentage=(resolution.current_week / 52) * 100,
        status=resolution.status.value,
        confidence_score=resolution.confidence_score,
        created_at=resolution.created_at
    )
    
    # Get all quarters
    stmt = select(QuarterlyPhase).where(
        QuarterlyPhase.resolution_id == resolution.id
    ).order_by(QuarterlyPhase.week_start)
    result = await db.execute(stmt)
    quarters = result.scalars().all()
    
    quarterly_phases = [
        QuarterlyPhaseResponse.from_orm(q) for q in quarters
    ]
    
    # Get current quarter (based on current_week)
    current_quarter = None
    for quarter in quarters:
        if quarter.week_start <= resolution.current_week <= quarter.week_end:
            # Get nested weekly plans
            stmt = select(WeeklyPlan).where(
                WeeklyPlan.quarterly_phase_id == quarter.id
            ).order_by(WeeklyPlan.week_number)
            result = await db.execute(stmt)
            weeks = result.scalars().all()
            
            current_quarter = QuarterlyPhaseDetailResponse(
                **QuarterlyPhaseResponse.from_orm(quarter).model_dump(),
                weekly_plans=[WeeklyPlanResponse.from_orm(w) for w in weeks]
            )
            break
    
    # Get current week
    current_week = None
    upcoming_weeks = []
    
    stmt = select(WeeklyPlan).where(
        WeeklyPlan.resolution_id == resolution.id,
        WeeklyPlan.week_number == resolution.current_week
    )
    result = await db.execute(stmt)
    current_week_record = result.scalar_one_or_none()
    
    if current_week_record:
        # Get daily workouts for current week
        stmt = select(DailyWorkout).where(
            DailyWorkout.weekly_plan_id == current_week_record.id
        ).order_by(DailyWorkout.date)
        result = await db.execute(stmt)
        daily = result.scalars().all()
        
        current_week = WeeklyPlanDetailResponse(
            **WeeklyPlanResponse.from_orm(current_week_record).model_dump(),
            daily_workouts=[DailyWorkoutResponse.from_orm(d) for d in daily],
            agent_reasoning=current_week_record.agent_reasoning or {}
        )
    
    # Get next 2 weeks as preview
    stmt = select(WeeklyPlan).where(
        WeeklyPlan.resolution_id == resolution.id,
        WeeklyPlan.week_number.in_([resolution.current_week + 1, resolution.current_week + 2])
    ).order_by(WeeklyPlan.week_number)
    result = await db.execute(stmt)
    upcoming = result.scalars().all()
    upcoming_weeks = [WeeklyPlanResponse.from_orm(w) for w in upcoming]
    
    return DashboardHierarchyResponse(
        yearly_goal=yearly_goal,
        quarterly_phases=quarterly_phases,
        current_quarter=current_quarter,
        current_week=current_week,
        upcoming_weeks=upcoming_weeks
    )


@router.get("/quarter/{quarter_id}", response_model=QuarterlyPhaseDetailResponse)
async def get_quarter_detail(
    quarter_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed view of a quarter with all nested weeks"""
    
    stmt = select(QuarterlyPhase).where(
        QuarterlyPhase.id == quarter_id,
        QuarterlyPhase.resolution_id.in_(
            select(Resolution.id).where(Resolution.user_id == current_user.id)
        )
    )
    result = await db.execute(stmt)
    quarter = result.scalar_one_or_none()
    
    if not quarter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarter not found"
        )
    
    # Get all weeks in this quarter
    stmt = select(WeeklyPlan).where(
        WeeklyPlan.quarterly_phase_id == quarter.id
    ).order_by(WeeklyPlan.week_number)
    result = await db.execute(stmt)
    weeks = result.scalars().all()
    
    return QuarterlyPhaseDetailResponse(
        **QuarterlyPhaseResponse.from_orm(quarter).model_dump(),
        weekly_plans=[WeeklyPlanResponse.from_orm(w) for w in weeks]
    )


@router.get("/week/{week_id}", response_model=WeeklyPlanDetailResponse)
async def get_week_detail(
    week_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed view of a week with all nested daily workouts"""
    
    stmt = select(WeeklyPlan).where(
        WeeklyPlan.id == week_id,
        WeeklyPlan.resolution_id.in_(
            select(Resolution.id).where(Resolution.user_id == current_user.id)
        )
    )
    result = await db.execute(stmt)
    week = result.scalar_one_or_none()
    
    if not week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Week not found"
        )
    
    # Get all daily workouts in this week
    stmt = select(DailyWorkout).where(
        DailyWorkout.weekly_plan_id == week.id
    ).order_by(DailyWorkout.date)
    result = await db.execute(stmt)
    daily_workouts = result.scalars().all()
    
    return WeeklyPlanDetailResponse(
        **WeeklyPlanResponse.from_orm(week).model_dump(),
        daily_workouts=[DailyWorkoutResponse.from_orm(d) for d in daily_workouts],
        agent_reasoning=week.agent_reasoning or {}
    )


@router.get("/workout/{workout_id}", response_model=DailyWorkoutDetailResponse)
async def get_workout_detail(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed view of a daily workout with full agent reasoning"""
    
    stmt = select(DailyWorkout).where(
        DailyWorkout.id == workout_id,
        DailyWorkout.resolution_id.in_(
            select(Resolution.id).where(Resolution.user_id == current_user.id)
        )
    )
    result = await db.execute(stmt)
    workout = result.scalar_one_or_none()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    return DailyWorkoutDetailResponse.from_orm(workout)


@router.get("/week/{week_id}/workouts", response_model=List[DailyWorkoutResponse])
async def get_week_workouts(
    week_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all workouts for a specific week"""
    
    stmt = select(DailyWorkout).where(
        DailyWorkout.weekly_plan_id == week_id,
        DailyWorkout.resolution_id.in_(
            select(Resolution.id).where(Resolution.user_id == current_user.id)
        )
    ).order_by(DailyWorkout.date)
    result = await db.execute(stmt)
    workouts = result.scalars().all()
    
    return [DailyWorkoutResponse.from_orm(w) for w in workouts]


@router.patch("/workout/{workout_id}/complete")
async def complete_workout(
    workout_id: int,
    feedback: Optional[dict] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark a workout as completed with optional user feedback"""
    
    stmt = select(DailyWorkout).where(
        DailyWorkout.id == workout_id,
        DailyWorkout.resolution_id.in_(
            select(Resolution.id).where(Resolution.user_id == current_user.id)
        )
    )
    result = await db.execute(stmt)
    workout = result.scalar_one_or_none()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    # Update workout
    from datetime import datetime
    workout.status = "completed"
    workout.completed_at = datetime.utcnow()
    if feedback:
        workout.user_feedback = feedback
    
    await db.commit()
    await db.refresh(workout)
    
    return DailyWorkoutResponse.from_orm(workout)


@router.patch("/workout/{workout_id}/skip")
async def skip_workout(
    workout_id: int,
    reason: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark a workout as skipped with optional reason"""
    
    stmt = select(DailyWorkout).where(
        DailyWorkout.id == workout_id,
        DailyWorkout.resolution_id.in_(
            select(Resolution.id).where(Resolution.user_id == current_user.id)
        )
    )
    result = await db.execute(stmt)
    workout = result.scalar_one_or_none()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    # Update workout
    workout.status = "skipped"
    if reason:
        workout.notes = reason
    
    await db.commit()
    await db.refresh(workout)
    
    return DailyWorkoutResponse.from_orm(workout)
