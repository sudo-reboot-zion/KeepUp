"""
Daily Plan Schemas
Request/Response models for daily workout plan API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DailyPlanRequest(BaseModel):
    """Request for custom daily plan with context"""
    date: Optional[str] = Field(None, description="Date for plan (YYYY-MM-DD)")
    sleep_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Sleep data from wearable",
        example={"hours": 7.5, "quality": "good", "hrv": 65}
    )
    calendar_events: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Calendar events for the day"
    )
    stress_score: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        description="Self-reported stress (0.0-1.0)"
    )


class ExerciseResponse(BaseModel):
    """Single exercise in workout plan"""
    name: str
    sets: int
    reps: Any  # Can be int or string ("30 seconds")
    notes: Optional[str] = None
    risk_level: Optional[str] = None


class WorkoutResponse(BaseModel):
    """Workout plan details"""
    name: str
    exercises: List[ExerciseResponse]
    estimated_duration: Optional[int] = Field(None, description="Minutes")


class DailyPlanResponse(BaseModel):
    """Complete daily plan response"""
    date: str
    workout: WorkoutResponse
    adaptations_made: List[str] = Field(
        default_factory=list,
        description="Modifications made by agents"
    )
    schedule_notes: List[str] = Field(
        default_factory=list,
        description="Calendar conflicts or notes"
    )
    readiness_score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Overall readiness (0.0-1.0)"
    )
    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Agent confidence in plan"
    )
    generated_at: Optional[str] = Field(
        None,
        description="Timestamp of generation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2026-01-01",
                "workout": {
                    "name": "Full Body Beginner",
                    "exercises": [
                        {
                            "name": "Bodyweight Squat",
                            "sets": 3,
                            "reps": 10,
                            "notes": "Focus on form"
                        }
                    ],
                    "estimated_duration": 20
                },
                "adaptations_made": [
                    "Reduced intensity due to poor sleep"
                ],
                "schedule_notes": [],
                "readiness_score": 0.75,
                "confidence": 0.92,
                "generated_at": "2026-01-01T08:00:00"
            }
        }