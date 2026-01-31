from typing import List
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from core.database import get_db
from api.dependencies import get_current_user
from models.user import User
from models.daily_log import UserDailyLog, DailyTask, TaskSource
from schemas.checkin_schema import (
    DailyCheckInCreate, DailyCheckInResponse, CheckInStatus,
    DailyTaskCreate, DailyTaskUpdate, DailyTaskResponse, DailyTasksList
)
from services.safety_guardrails import SafetyGuardrails, AlertLevel

router = APIRouter()

# ============================================================================
# DAILY CHECK-IN
# ============================================================================

@router.post("/daily", response_model=DailyCheckInResponse)
async def create_daily_checkin(
    checkin_data: DailyCheckInCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Submit daily check-in.
    If a check-in already exists for today, it will be updated.
    """
    today = date.today()
    
    # Check if exists
    query = select(UserDailyLog).where(
        and_(UserDailyLog.user_id == current_user.id, UserDailyLog.date == today)
    )
    result = await db.execute(query)
    existing_checkin = result.scalar_one_or_none()
    
    if existing_checkin:
        # Update existing
        existing_checkin.sleep_quality = checkin_data.sleep_quality
        existing_checkin.energy_level = checkin_data.energy_level
        existing_checkin.soreness_level = checkin_data.soreness_level
        existing_checkin.stress_level = checkin_data.stress_level
        existing_checkin.notes = checkin_data.notes
        
        # Mental Health
        existing_checkin.mood_score = checkin_data.mood_score
        existing_checkin.anxiety_level = checkin_data.anxiety_level
        existing_checkin.gratitude_log = checkin_data.gratitude_log
        existing_checkin.wins_log = checkin_data.wins_log
        existing_checkin.challenges_log = checkin_data.challenges_log
        
        checkin = existing_checkin
    else:
        # Create new
        checkin = UserDailyLog(
            user_id=current_user.id,
            date=today,
            **checkin_data.model_dump()
        )
        db.add(checkin)
    
    await db.commit()
    await db.refresh(checkin)
    
    # PHASE 3: Check biometric safety
    guardrails = SafetyGuardrails(db)
    biometric_alerts = guardrails.check_biometric_safety(
        resolution_id=current_user.active_resolution_id if hasattr(current_user, 'active_resolution_id') else None,
        bp_systolic=checkin_data.bp_systolic if hasattr(checkin_data, 'bp_systolic') else None,
        bp_diastolic=checkin_data.bp_diastolic if hasattr(checkin_data, 'bp_diastolic') else None,
        resting_hr=checkin_data.resting_hr if hasattr(checkin_data, 'resting_hr') else None,
        weight_kg=checkin_data.weight_kg if hasattr(checkin_data, 'weight_kg') else None
    )
    
    # Log critical alerts
    critical = [a for a in biometric_alerts if a.level == AlertLevel.CRITICAL]
    if critical:
        # TODO: Send urgent notification to user
        # TODO: Alert support team
        pass
    
    # TODO: Trigger daily workflow here to generate workout/tasks based on check-in
    
    return checkin

@router.get("/status", response_model=CheckInStatus)
async def get_checkin_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Check if user has checked in today
    """
    today = date.today()
    
    query = select(UserDailyLog).where(
        and_(UserDailyLog.user_id == current_user.id, UserDailyLog.date == today)
    )
    result = await db.execute(query)
    checkin = result.scalar_one_or_none()
    
    # Get last checkin date
    last_query = select(UserDailyLog.date).where(
        UserDailyLog.user_id == current_user.id
    ).order_by(UserDailyLog.date.desc()).limit(1)
    last_result = await db.execute(last_query)
    last_date = last_result.scalar_one_or_none()
    
    return CheckInStatus(
        has_checked_in=bool(checkin),
        last_checkin_date=last_date
    )

# ============================================================================
# DAILY TASKS
# ============================================================================

@router.get("/tasks/today", response_model=DailyTasksList)
async def get_today_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all tasks for today
    """
    today = date.today()
    
    query = select(DailyTask).where(
        and_(DailyTask.user_id == current_user.id, DailyTask.date == today)
    ).order_by(DailyTask.is_completed, DailyTask.created_at)
    
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    completed_count = sum(1 for t in tasks if t.is_completed)
    
    return DailyTasksList(
        date=today,
        tasks=tasks,
        completed_count=completed_count,
        total_count=len(tasks)
    )

@router.post("/tasks", response_model=DailyTaskResponse)
async def create_task(
    task_data: DailyTaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new task (custom user task)
    """
    task_date = task_data.date or date.today()
    
    task = DailyTask(
        user_id=current_user.id,
        date=task_date,
        title=task_data.title,
        description=task_data.description,
        task_type=task_data.task_type,
        source=TaskSource.USER
    )
    
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    return task

@router.patch("/tasks/{task_id}", response_model=DailyTaskResponse)
async def update_task(
    task_id: int,
    task_update: DailyTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update task (mark complete, etc)
    """
    query = select(DailyTask).where(
        and_(DailyTask.id == task_id, DailyTask.user_id == current_user.id)
    )
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_update.is_completed is not None:
        task.is_completed = task_update.is_completed
        if task.is_completed:
            task.completed_at = datetime.now()
        else:
            task.completed_at = None
            
    if task_update.title is not None:
        task.title = task_update.title
        
    if task_update.description is not None:
        task.description = task_update.description
        
    await db.commit()
    await db.refresh(task)
    
    return task
