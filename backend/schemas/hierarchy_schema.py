"""
Schemas for Quarterly, Weekly, and Daily Workouts
Used for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# QUARTERLY PHASE SCHEMAS
# ============================================================================

class MilestoneSchema(BaseModel):
    """Milestone within a quarter"""
    week: int = Field(..., ge=1, le=52)
    goal: str
    description: Optional[str] = None


class QuarterlyPhaseResponse(BaseModel):
    """Response for a quarterly phase"""
    id: int
    resolution_id: int
    quarter: str  # "Q1", "Q2", "Q3", "Q4"
    week_start: int
    week_end: int
    phase_name: str
    phase_description: str
    focus_areas: List[str]
    target_workouts: int
    target_metric: Optional[str]
    target_progression: Optional[str]
    workouts_completed: int
    adherence_rate: float
    milestones: List[MilestoneSchema]
    risk_factors: List[str]
    protective_strategies: List[str]
    status: str  # "completed", "in_progress", "locked"
    completion_percentage: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class QuarterlyPhaseDetailResponse(QuarterlyPhaseResponse):
    """Detailed quarterly phase response with nested weekly plans"""
    weekly_plans: List['WeeklyPlanResponse'] = []


# ============================================================================
# WEEKLY PLAN SCHEMAS
# ============================================================================

class ExerciseDetail(BaseModel):
    """Single exercise in a workout"""
    name: str
    distance: Optional[float] = None  # For cardio
    duration: Optional[int] = None  # minutes
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    pace: Optional[str] = None  # "8:45/mi"
    intensity: Optional[str] = None


class WeeklyPlanResponse(BaseModel):
    """Response for a weekly plan"""
    id: int
    quarterly_phase_id: int
    resolution_id: int
    week_number: int
    quarter_week: int
    week_start_date: datetime
    week_end_date: datetime
    target_workouts: int
    target_duration_minutes: int
    focus: Optional[str]
    estimated_difficulty: str
    intensity_progression: Optional[str]
    risk_level: str
    critical_week: Optional[str]
    workouts_completed: int
    workouts_planned: int
    adherence_rate: float
    total_minutes_completed: int
    status: str
    completion_percentage: float
    remaining_workouts: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WeeklyPlanDetailResponse(WeeklyPlanResponse):
    """Detailed weekly plan response with nested daily workouts"""
    daily_workouts: List['DailyWorkoutResponse'] = []
    agent_reasoning: Optional[Dict[str, str]] = None
    protective_measures: List[str] = []


# ============================================================================
# DAILY WORKOUT SCHEMAS
# ============================================================================

class WorkoutContext(BaseModel):
    """Context at time of workout"""
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[str] = None
    energy_level: Optional[str] = None
    stress_level: Optional[int] = Field(None, ge=0, le=10)
    soreness_level: Optional[int] = Field(None, ge=0, le=10)
    mood: Optional[str] = None


class UserFeedback(BaseModel):
    """User feedback after completing workout"""
    how_felt: Optional[str] = None
    rpe: Optional[int] = Field(None, ge=1, le=10, description="Rate of Perceived Exertion")
    energy_level: Optional[str] = None
    difficulty: Optional[str] = None
    would_repeat: Optional[bool] = None
    notes: Optional[str] = None


class AgentModification(BaseModel):
    """Agent modification details"""
    agent: str
    reason: str
    changes: List[str]
    confidence: float = Field(..., ge=0, le=1)


class DailyWorkoutResponse(BaseModel):
    """Response for a daily workout"""
    id: int
    weekly_plan_id: int
    resolution_id: int
    date: datetime
    day_of_week: str
    
    # Planned
    planned_workout_type: str
    planned_duration_minutes: int
    planned_intensity: str
    planned_target: Optional[str]
    planned_exercises: List[ExerciseDetail]
    
    # Context
    context: Optional[WorkoutContext] = None
    
    # Modifications
    was_modified: bool
    modification_reason: Optional[str]
    modified_workout_type: Optional[str]
    modified_duration_minutes: Optional[int]
    modified_intensity: Optional[str]
    modification_rationale: Optional[str]
    
    # Actual
    status: str
    actual_duration_minutes: Optional[int]
    actual_intensity_perceived: Optional[str]
    user_feedback: Optional[UserFeedback] = None
    
    notes: Optional[str]
    intensity_change: str
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DailyWorkoutDetailResponse(DailyWorkoutResponse):
    """Detailed daily workout with full agent reasoning"""
    agent_modifications: Optional[AgentModification] = None


# ============================================================================
# DASHBOARD SUMMARY SCHEMAS
# ============================================================================

class YearlyGoalSummary(BaseModel):
    """Summary of yearly goal for dashboard"""
    id: int
    resolution_id: int
    resolution_text: str
    target_completion_date: str
    current_week: int
    total_weeks: int = 52
    progress_percentage: float
    status: str
    confidence_score: Optional[float]
    created_at: datetime


class DashboardHierarchyResponse(BaseModel):
    """Complete dashboard hierarchy"""
    yearly_goal: YearlyGoalSummary
    quarterly_phases: List[QuarterlyPhaseResponse]
    current_quarter: Optional[QuarterlyPhaseDetailResponse]
    current_week: Optional[WeeklyPlanDetailResponse]
    upcoming_weeks: List[WeeklyPlanResponse]


# Update forward references
QuarterlyPhaseDetailResponse.model_rebuild()
WeeklyPlanDetailResponse.model_rebuild()
DailyWorkoutDetailResponse.model_rebuild()
