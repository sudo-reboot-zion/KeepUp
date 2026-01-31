from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field
from models.daily_log import EnergyLevel, SorenessLevel, StressLevel, TaskType, TaskSource

# CheckIn Schemas
class DailyCheckInCreate(BaseModel):
    sleep_quality: int = Field(..., ge=1, le=5)
    energy_level: EnergyLevel
    soreness_level: SorenessLevel
    stress_level: StressLevel
    notes: Optional[str] = None
    
    # Mental Health
    mood_score: Optional[int] = Field(None, ge=1, le=10)
    anxiety_level: Optional[int] = Field(None, ge=1, le=10)
    gratitude_log: Optional[str] = None
    wins_log: Optional[str] = None
    challenges_log: Optional[str] = None

class DailyCheckInResponse(BaseModel):
    id: int
    date: date
    sleep_quality: int
    energy_level: EnergyLevel
    soreness_level: SorenessLevel
    stress_level: StressLevel
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class CheckInStatus(BaseModel):
    has_checked_in: bool
    last_checkin_date: Optional[date]

# Task Schemas
class DailyTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: TaskType = TaskType.CUSTOM
    date: Optional[date] = None # Defaults to today if None

class DailyTaskUpdate(BaseModel):
    is_completed: Optional[bool] = None
    title: Optional[str] = None
    description: Optional[str] = None

class DailyTaskResponse(BaseModel):
    id: int
    date: date
    title: str
    description: Optional[str]
    task_type: TaskType
    is_completed: bool
    completed_at: Optional[datetime]
    source: TaskSource
    created_at: datetime

    class Config:
        from_attributes = True

class DailyTasksList(BaseModel):
    date: date
    tasks: List[DailyTaskResponse]
    completed_count: int
    total_count: int
