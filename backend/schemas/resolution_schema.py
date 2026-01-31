"""
Resolution Schemas
Pydantic models for resolution API requests/responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ResolutionStatus(str, Enum):
    """Resolution status enum"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    PAUSED = "paused"


class CreateResolutionRequest(BaseModel):
    """Request to create a new resolution"""
    resolution_text: str = Field(..., description="User's fitness goal", min_length=10)
    past_attempts: Optional[str] = Field(None, description="History of past attempts")
    life_constraints: Optional[List[str]] = Field(None, description="Life constraints/barriers")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resolution_text": "I want to lose 20 pounds and build muscle",
                "past_attempts": "Tried gym 3 times, quit after 4 weeks each time",
                "life_constraints": ["busy_schedule", "travel_frequently"]
            }
        }


class ConfirmResolutionRequest(BaseModel):
    """Request to confirm and save a resolution from onboarding"""
    resolution_text: str
    past_attempts: Optional[str] = None
    life_constraints: Optional[List[str]] = None
    final_plan: Dict[str, Any]
    debate_summary: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    occupation: Optional[str] = None
    occupation_details: Optional[Dict[str, Any]] = None


class ResolutionResponse(BaseModel):
    """Response with resolution details"""
    id: int
    user_id: int
    resolution_text: str
    status: ResolutionStatus
    current_week: int
    workouts_completed: int
    adherence_rate: float
    streak_days: int
    abandonment_probability: float
    final_plan: Optional[Dict[str, Any]] = None
    debate_summary: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ResolutionListResponse(BaseModel):
    """List of resolutions"""
    resolutions: List[ResolutionResponse]
    total: int
    active_count: int
    completed_count: int


class UpdateProgressRequest(BaseModel):
    """Update resolution progress"""
    workouts_completed: Optional[int] = None
    current_week: Optional[int] = None
    adherence_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    streak_days: Optional[int] = Field(None, ge=0)


class ModifyResolutionRequest(BaseModel):
    """Modify resolution plan"""
    new_weekly_target: Optional[int] = None
    new_constraints: Optional[List[str]] = None
    reason: str = Field(..., description="Why modifying the plan")


class ResolutionInsightsResponse(BaseModel):
    """AI insights about resolution"""
    resolution_id: int
    insights: List[str]
    predictions: Dict[str, Any]
    recommendations: List[str]
    confidence: float
