"""
Safety & Guardrails Endpoints
Handles medical threshold checks, confidence validation, and overtraining prevention
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from api.dependencies import get_db, get_current_user
from schemas.safety_schema import (
    BiometricCheckRequest,
    SafetyCheckRequest,
    SafetyReportResponse,
    SafetyAlertResponse
)
from services.safety_guardrails import SafetyGuardrails
from models.resolution import Resolution
from models.user import User


router = APIRouter(prefix="/api/safety", tags=["safety"])


@router.post("/check-biometrics/{resolution_id}", response_model=SafetyReportResponse)
async def check_biometric_safety(
    resolution_id: int,
    request: BiometricCheckRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check biometric readings against medical safety thresholds.
    Returns alerts and warnings.
    
    ## Critical Alerts
    - Blood pressure > 180/120 mmHg
    - Resting heart rate > 120 or < 40 bpm
    - Rapid weight changes (>2 kg/week)
    
    ## Warnings
    - Elevated blood pressure
    - High resting heart rate
    - Moderate weight changes
    """
    # Verify resolution belongs to user
    resolution = db.query(Resolution).filter(
        Resolution.id == resolution_id,
        Resolution.user_id == current_user.id
    ).first()
    
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resolution not found"
        )
    
    # Run biometric safety checks
    guardrails = SafetyGuardrails(db)
    report = guardrails.apply_all_checks(
        resolution_id=resolution_id,
        bp_systolic=request.bp_systolic,
        bp_diastolic=request.bp_diastolic,
        resting_hr=request.resting_hr,
        weight_kg=request.weight_kg,
        recommendation_confidence=request.recommendation_confidence,
        recommendation_type=request.recommendation_type,
        proposed_workout_minutes=request.proposed_workout_minutes or 0,
        proposed_intensity=request.proposed_intensity or "moderate"
    )
    
    # Format response
    return SafetyReportResponse(
        cleared_for_activity=report["safe_to_proceed"],
        critical_alerts=[
            SafetyAlertResponse(
                level="critical",
                message=alert["message"],
                action_required=alert["action"],
                metric=alert.get("metric"),
                category=alert["category"]
            )
            for alert in report["critical_alerts"]
        ],
        warnings=[
            SafetyAlertResponse(
                level="warning",
                message=alert["message"],
                action_required=alert["action"],
                category=alert["category"]
            )
            for alert in report["warnings"]
        ],
        medical_disclaimer=report.get("medical_disclaimer"),
        blocked_reason=report.get("blocked_reason")
    )


@router.post("/check-confidence/{resolution_id}", response_model=SafetyReportResponse)
async def check_recommendation_confidence(
    resolution_id: int,
    confidence_score: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if recommendation confidence is acceptable.
    
    - Score < 0.5: BLOCKED - recommendation is not shown
    - Score 0.5-0.7: WARNING - shown with caution notice
    - Score > 0.7: SAFE - shown normally
    """
    resolution = db.query(Resolution).filter(
        Resolution.id == resolution_id,
        Resolution.user_id == current_user.id
    ).first()
    
    if not resolution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    guardrails = SafetyGuardrails(db)
    safe, alert = guardrails.check_recommendation_confidence(confidence_score)
    
    report = {
        "safe_to_proceed": safe,
        "critical_alerts": [],
        "warnings": [],
        "medical_disclaimer": None,
        "blocked_reason": None
    }
    
    if alert:
        if alert.level.value == "warning":
            report["warnings"].append({
                "message": alert.message,
                "action": alert.action_required,
                "category": alert.category
            })
        else:
            report["blocked_reason"] = alert.message
    
    return SafetyReportResponse(
        cleared_for_activity=safe,
        critical_alerts=[],
        warnings=report["warnings"],
        blocked_reason=report["blocked_reason"]
    )


@router.post("/check-overtraining/{resolution_id}", response_model=SafetyReportResponse)
async def check_overtraining_risk(
    resolution_id: int,
    proposed_workout_minutes: int = 0,
    proposed_intensity: str = "moderate",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check for overtraining risk based on weekly volume.
    
    Monitors:
    - Total weekly minutes (max 450)
    - High-intensity session count (max 2/week)
    - Recovery days (minimum 2/week)
    """
    resolution = db.query(Resolution).filter(
        Resolution.id == resolution_id,
        Resolution.user_id == current_user.id
    ).first()
    
    if not resolution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    guardrails = SafetyGuardrails(db)
    alerts = guardrails.check_overtraining_risk(
        resolution_id,
        proposed_workout_minutes,
        proposed_intensity
    )
    
    report = {
        "safe_to_proceed": not any(a.level.value == "blocked" for a in alerts),
        "critical_alerts": [],
        "warnings": [],
        "medical_disclaimer": None,
        "blocked_reason": None
    }
    
    for alert in alerts:
        if alert.level.value == "blocked":
            report["safe_to_proceed"] = False
            report["blocked_reason"] = alert.message
        elif alert.level.value == "warning":
            report["warnings"].append({
                "message": alert.message,
                "action": alert.action_required,
                "category": alert.category
            })
    
    return SafetyReportResponse(
        cleared_for_activity=report["safe_to_proceed"],
        critical_alerts=[],
        warnings=report["warnings"],
        blocked_reason=report["blocked_reason"]
    )


@router.get("/get-thresholds/{resolution_id}")
async def get_safety_thresholds(
    resolution_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized safety thresholds for this resolution.
    Shows default and any custom thresholds set for the user.
    """
    resolution = db.query(Resolution).filter(
        Resolution.id == resolution_id,
        Resolution.user_id == current_user.id
    ).first()
    
    if not resolution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return {
        "medical_thresholds": {
            "blood_pressure": {
                "critical_high": f"{SafetyGuardrails.BP_SYSTOLIC_CRITICAL_HIGH}/{SafetyGuardrails.BP_DIASTOLIC_CRITICAL_HIGH} mmHg",
                "critical_low": f"{SafetyGuardrails.BP_SYSTOLIC_CRITICAL_LOW}/{SafetyGuardrails.BP_DIASTOLIC_CRITICAL_LOW} mmHg",
                "warning_high": f"{SafetyGuardrails.BP_SYSTOLIC_HIGH}/{SafetyGuardrails.BP_DIASTOLIC_CRITICAL_HIGH} mmHg"
            },
            "heart_rate": {
                "resting_critical_high": f"{SafetyGuardrails.HR_RESTING_CRITICAL_HIGH} bpm",
                "resting_critical_low": f"{SafetyGuardrails.HR_RESTING_CRITICAL_LOW} bpm",
                "resting_warning_high": f"{SafetyGuardrails.HR_RESTING_WARNING_HIGH} bpm"
            },
            "weight_change": {
                "critical_weekly": f"{SafetyGuardrails.WEIGHT_CHANGE_CRITICAL} kg/week",
                "warning_weekly": f"{SafetyGuardrails.WEIGHT_CHANGE_WARNING} kg/week"
            }
        },
        "confidence_thresholds": {
            "minimum_safe": SafetyGuardrails.CONFIDENCE_MIN_SAFE,
            "minimum_show": SafetyGuardrails.CONFIDENCE_MIN_SHOW,
            "recommendation": "Scores below 0.5 are blocked, 0.5-0.7 shown with warnings, above 0.7 shown normally"
        },
        "training_thresholds": {
            "max_weekly_minutes": SafetyGuardrails.WORKOUT_MINUTES_MAX_WEEKLY,
            "warning_weekly_minutes": SafetyGuardrails.WORKOUT_MINUTES_WARNING,
            "max_high_intensity_sessions": SafetyGuardrails.INTENSITY_HIGH_MAX_WEEKLY,
            "min_recovery_days": SafetyGuardrails.RECOVERY_DAYS_MIN
        }
    }


@router.post("/acknowledge-critical-alert/{resolution_id}")
async def acknowledge_critical_alert(
    resolution_id: int,
    alert_category: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    User acknowledges understanding of a critical alert.
    Logs acknowledgment for record-keeping and follow-up.
    """
    resolution = db.query(Resolution).filter(
        Resolution.id == resolution_id,
        Resolution.user_id == current_user.id
    ).first()
    
    if not resolution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    # Log acknowledgment
    # TODO: Create AlertAcknowledgment model for tracking
    
    return {
        "success": True,
        "message": f"Alert acknowledged: {alert_category}",
        "note": "Please follow the recommended actions and seek medical attention if needed"
    }
