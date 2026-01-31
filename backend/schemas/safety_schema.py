"""Safety and guardrails schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BiometricCheckRequest(BaseModel):
    """Request to check biometric safety"""
    bp_systolic: Optional[int] = Field(None, ge=0, le=300, description="Systolic blood pressure in mmHg")
    bp_diastolic: Optional[int] = Field(None, ge=0, le=200, description="Diastolic blood pressure in mmHg")
    resting_hr: Optional[int] = Field(None, ge=30, le=200, description="Resting heart rate in bpm")
    weight_kg: Optional[float] = Field(None, gt=0, description="Weight in kilograms")
    
    recommendation_confidence: Optional[float] = Field(None, ge=0, le=1, description="Confidence score 0-1")
    recommendation_type: Optional[str] = Field(None, description="Type of recommendation: workout, rest, reduce_intensity, etc")
    
    proposed_workout_minutes: Optional[int] = Field(None, ge=0, description="Minutes of workout being proposed")
    proposed_intensity: Optional[str] = Field("moderate", description="Intensity: easy, moderate, hard")


class SafetyCheckRequest(BaseModel):
    """Request to run all safety checks"""
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    resting_hr: Optional[int] = None
    weight_kg: Optional[float] = None
    recommendation_confidence: Optional[float] = None
    recommendation_type: Optional[str] = None
    proposed_workout_minutes: int = 0
    proposed_intensity: str = "moderate"


class SafetyAlertResponse(BaseModel):
    """Single safety alert in response"""
    level: str  # "critical", "warning", "blocked"
    category: str  # "medical", "confidence", "overtraining", "disclaimer"
    message: str
    action_required: Optional[str] = None
    metric: Optional[str] = None  # e.g., "bp_systolic", "weight_change"
    timestamp: Optional[datetime] = None


class SafetyReportResponse(BaseModel):
    """Comprehensive safety report"""
    cleared_for_activity: bool = Field(
        description="True if safe to proceed, False if critical alerts or blocks"
    )
    critical_alerts: List[SafetyAlertResponse] = Field(
        default=[],
        description="Critical alerts requiring immediate attention"
    )
    warnings: List[SafetyAlertResponse] = Field(
        default=[],
        description="Warnings to be aware of"
    )
    medical_disclaimer: Optional[str] = Field(
        None,
        description="Medical disclaimer if applicable to this recommendation"
    )
    blocked_reason: Optional[str] = Field(
        None,
        description="Reason recommendation is blocked if not cleared"
    )


class ConfidenceCheckRequest(BaseModel):
    """Check if confidence score is acceptable"""
    confidence_score: float = Field(ge=0, le=1, description="Score 0-1")


class OverttrainingCheckRequest(BaseModel):
    """Check for overtraining risk"""
    proposed_workout_minutes: int = Field(ge=0, description="Minutes of workout")
    proposed_intensity: str = Field("moderate", description="Intensity level")


class SafetyThresholdsResponse(BaseModel):
    """Safety thresholds for a resolution"""
    medical_thresholds: dict
    confidence_thresholds: dict
    training_thresholds: dict


class CriticalAlertAcknowledgmentRequest(BaseModel):
    """User acknowledging a critical alert"""
    alert_category: str
    user_notes: Optional[str] = None


class AlertHistoryResponse(BaseModel):
    """Historical record of alerts for a user"""
    id: int
    resolution_id: int
    alert_type: str  # "critical", "warning", "blocked"
    category: str
    message: str
    metric: Optional[str]
    value: Optional[float]
    threshold: Optional[float]
    acknowledged: bool
    acknowledged_at: Optional[datetime]
    created_at: datetime
