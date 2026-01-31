"""
Safety Guardrails Service
Enforces medical thresholds, confidence thresholds, and overtraining prevention
Ensures system stays within safe, responsible boundaries
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from sqlalchemy.orm import Session
from enum import Enum

from models.resolution import Resolution
from models.biometric_reading import BiometricReading
from models.daily_workout import DailyWorkout
from models.baseline_metrics import BaselineMetrics


class AlertLevel(str, Enum):
    """Alert severity levels"""
    INFO = "info"  # Informational only
    WARNING = "warning"  # User should be aware
    CRITICAL = "critical"  # Seek medical attention
    BLOCKED = "blocked"  # Recommendation blocked due to safety


class SafetyAlert:
    """Represents a safety alert or warning"""
    
    def __init__(
        self,
        level: AlertLevel,
        category: str,
        message: str,
        metric: Optional[str] = None,
        current_value: Optional[float] = None,
        threshold: Optional[float] = None,
        action_required: Optional[str] = None
    ):
        self.level = level
        self.category = category  # "medical", "confidence", "overtraining", "disclaimer"
        self.message = message
        self.metric = metric
        self.current_value = current_value
        self.threshold = threshold
        self.action_required = action_required
        self.timestamp = datetime.utcnow()


class SafetyGuardrails:
    """
    Comprehensive safety checking system.
    Enforces medical, confidence, and training safety boundaries.
    """
    
    # MEDICAL THRESHOLDS
    BP_SYSTOLIC_CRITICAL_HIGH = 180  # mmHg
    BP_SYSTOLIC_CRITICAL_LOW = 90    # mmHg
    BP_DIASTOLIC_CRITICAL_HIGH = 120  # mmHg
    BP_DIASTOLIC_CRITICAL_LOW = 60    # mmHg
    
    BP_SYSTOLIC_HIGH = 160  # Warning threshold
    BP_SYSTOLIC_LOW = 100   # Warning threshold
    
    HR_RESTING_CRITICAL_HIGH = 120  # bpm
    HR_RESTING_CRITICAL_LOW = 40    # bpm
    HR_RESTING_WARNING_HIGH = 100   # bpm
    
    WEIGHT_CHANGE_CRITICAL = 2.0  # kg per week (rapid change)
    WEIGHT_CHANGE_WARNING = 1.5    # kg per week
    
    # CONFIDENCE THRESHOLDS
    CONFIDENCE_MIN_SHOW = 0.7  # Don't show recommendations below this
    CONFIDENCE_MIN_SAFE = 0.5  # Block recommendations below this
    
    # TRAINING THRESHOLDS
    WORKOUT_MINUTES_MAX_WEEKLY = 450  # 7.5 hours max per week
    WORKOUT_MINUTES_WARNING = 360      # 6 hours warning threshold
    INTENSITY_HIGH_MAX_WEEKLY = 2      # Max 2 high-intensity sessions per week
    RECOVERY_DAYS_MIN = 2              # Min 2 full recovery days per week
    
    def __init__(self, db: Session):
        self.db = db
    
    def check_biometric_safety(
        self,
        resolution_id: int,
        bp_systolic: Optional[int] = None,
        bp_diastolic: Optional[int] = None,
        resting_hr: Optional[int] = None,
        weight_kg: Optional[float] = None
    ) -> List[SafetyAlert]:
        """
        Check biometric readings against medical safety thresholds.
        Returns list of alerts at various severity levels.
        """
        alerts = []
        
        # Get baseline for comparison
        baseline = self.db.query(BaselineMetrics).filter(
            BaselineMetrics.resolution_id == resolution_id
        ).first()
        
        # BLOOD PRESSURE CHECKS
        if bp_systolic is not None:
            if bp_systolic >= self.BP_SYSTOLIC_CRITICAL_HIGH:
                alerts.append(SafetyAlert(
                    level=AlertLevel.CRITICAL,
                    category="medical",
                    message=f"CRITICAL: Blood pressure systolic {bp_systolic} mmHg is dangerously high. Seek immediate medical attention.",
                    metric="bp_systolic",
                    current_value=bp_systolic,
                    threshold=self.BP_SYSTOLIC_CRITICAL_HIGH,
                    action_required="Seek medical attention immediately"
                ))
            elif bp_systolic < self.BP_SYSTOLIC_CRITICAL_LOW:
                alerts.append(SafetyAlert(
                    level=AlertLevel.CRITICAL,
                    category="medical",
                    message=f"CRITICAL: Blood pressure systolic {bp_systolic} mmHg is dangerously low. Seek immediate medical attention.",
                    metric="bp_systolic",
                    current_value=bp_systolic,
                    threshold=self.BP_SYSTOLIC_CRITICAL_LOW,
                    action_required="Seek medical attention immediately"
                ))
            elif bp_systolic >= self.BP_SYSTOLIC_HIGH:
                alerts.append(SafetyAlert(
                    level=AlertLevel.WARNING,
                    category="medical",
                    message=f"WARNING: Blood pressure systolic {bp_systolic} mmHg is elevated. Monitor closely and consult doctor.",
                    metric="bp_systolic",
                    current_value=bp_systolic,
                    threshold=self.BP_SYSTOLIC_HIGH,
                    action_required="Consult your doctor"
                ))
            elif bp_systolic < self.BP_SYSTOLIC_LOW:
                alerts.append(SafetyAlert(
                    level=AlertLevel.WARNING,
                    category="medical",
                    message=f"WARNING: Blood pressure systolic {bp_systolic} mmHg is low. Monitor for dizziness.",
                    metric="bp_systolic",
                    current_value=bp_systolic,
                    threshold=self.BP_SYSTOLIC_LOW,
                    action_required="Increase water intake, monitor symptoms"
                ))
        
        if bp_diastolic is not None:
            if bp_diastolic >= self.BP_DIASTOLIC_CRITICAL_HIGH:
                alerts.append(SafetyAlert(
                    level=AlertLevel.CRITICAL,
                    category="medical",
                    message=f"CRITICAL: Blood pressure diastolic {bp_diastolic} mmHg is dangerously high.",
                    metric="bp_diastolic",
                    current_value=bp_diastolic,
                    threshold=self.BP_DIASTOLIC_CRITICAL_HIGH,
                    action_required="Seek medical attention immediately"
                ))
            elif bp_diastolic < self.BP_DIASTOLIC_CRITICAL_LOW:
                alerts.append(SafetyAlert(
                    level=AlertLevel.CRITICAL,
                    category="medical",
                    message=f"CRITICAL: Blood pressure diastolic {bp_diastolic} mmHg is dangerously low.",
                    metric="bp_diastolic",
                    current_value=bp_diastolic,
                    threshold=self.BP_DIASTOLIC_CRITICAL_LOW,
                    action_required="Seek medical attention immediately"
                ))
        
        # HEART RATE CHECKS
        if resting_hr is not None:
            if resting_hr >= self.HR_RESTING_CRITICAL_HIGH:
                alerts.append(SafetyAlert(
                    level=AlertLevel.CRITICAL,
                    category="medical",
                    message=f"CRITICAL: Resting heart rate {resting_hr} bpm is dangerously high. This may indicate illness or stress.",
                    metric="resting_hr",
                    current_value=resting_hr,
                    threshold=self.HR_RESTING_CRITICAL_HIGH,
                    action_required="Seek medical attention if persistent"
                ))
            elif resting_hr < self.HR_RESTING_CRITICAL_LOW:
                alerts.append(SafetyAlert(
                    level=AlertLevel.CRITICAL,
                    category="medical",
                    message=f"CRITICAL: Resting heart rate {resting_hr} bpm is dangerously low.",
                    metric="resting_hr",
                    current_value=resting_hr,
                    threshold=self.HR_RESTING_CRITICAL_LOW,
                    action_required="Seek medical attention immediately"
                ))
            elif resting_hr >= self.HR_RESTING_WARNING_HIGH:
                alerts.append(SafetyAlert(
                    level=AlertLevel.WARNING,
                    category="medical",
                    message=f"WARNING: Resting heart rate {resting_hr} bpm is elevated. May indicate fatigue or stress.",
                    metric="resting_hr",
                    current_value=resting_hr,
                    threshold=self.HR_RESTING_WARNING_HIGH,
                    action_required="Get more rest and recovery"
                ))
        
        # WEIGHT CHANGE CHECKS
        if weight_kg is not None and baseline:
            # Get previous weight reading
            prev_reading = self.db.query(BiometricReading).filter(
                BiometricReading.resolution_id == resolution_id,
                BiometricReading.weight_kg.isnot(None)
            ).order_by(BiometricReading.date.desc()).limit(2).all()
            
            if len(prev_reading) >= 2:
                weight_change = prev_reading[0].weight_kg - prev_reading[1].weight_kg
                days_between = (prev_reading[0].date - prev_reading[1].date).days
                
                if days_between > 0:
                    # Extrapolate to weekly change
                    weekly_change = (weight_change / days_between) * 7
                    
                    if abs(weekly_change) >= self.WEIGHT_CHANGE_CRITICAL:
                        alerts.append(SafetyAlert(
                            level=AlertLevel.CRITICAL,
                            category="medical",
                            message=f"CRITICAL: Weight changing {abs(weekly_change):.1f} kg/week. This is extremely rapid.",
                            metric="weight_change",
                            current_value=weekly_change,
                            threshold=self.WEIGHT_CHANGE_CRITICAL,
                            action_required="Consult doctor about rapid weight changes"
                        ))
                    elif abs(weekly_change) >= self.WEIGHT_CHANGE_WARNING:
                        alerts.append(SafetyAlert(
                            level=AlertLevel.WARNING,
                            category="medical",
                            message=f"WARNING: Weight changing {abs(weekly_change):.1f} kg/week. Monitor closely.",
                            metric="weight_change",
                            current_value=weekly_change,
                            threshold=self.WEIGHT_CHANGE_WARNING,
                            action_required="Monitor nutrition and hydration"
                        ))
        
        return alerts
    
    def check_recommendation_confidence(
        self,
        confidence_score: float
    ) -> Tuple[bool, Optional[SafetyAlert]]:
        """
        Check if recommendation confidence is safe to display.
        Returns (safe: bool, alert: Optional[SafetyAlert])
        """
        if confidence_score < self.CONFIDENCE_MIN_SAFE:
            # Block the recommendation
            alert = SafetyAlert(
                level=AlertLevel.BLOCKED,
                category="confidence",
                message=f"Recommendation confidence too low ({confidence_score:.0%}). Blocked for safety.",
                metric="confidence_score",
                current_value=confidence_score,
                threshold=self.CONFIDENCE_MIN_SAFE,
                action_required="Wait for more data or check back later"
            )
            return False, alert
        
        elif confidence_score < self.CONFIDENCE_MIN_SHOW:
            # Show warning
            alert = SafetyAlert(
                level=AlertLevel.WARNING,
                category="confidence",
                message=f"Recommendation confidence is moderate ({confidence_score:.0%}). Use as guidance only.",
                metric="confidence_score",
                current_value=confidence_score,
                threshold=self.CONFIDENCE_MIN_SHOW,
                action_required="Consider additional data points"
            )
            return True, alert
        
        return True, None
    
    def check_overtraining_risk(
        self,
        resolution_id: int,
        proposed_workout_minutes: int = 0,
        proposed_intensity: str = "moderate"
    ) -> List[SafetyAlert]:
        """
        Check for overtraining risk based on weekly volume.
        Monitors total minutes and intensity distribution.
        """
        alerts = []
        
        # Get last 7 days of completed workouts
        week_ago = datetime.utcnow() - timedelta(days=7)
        weekly_workouts = self.db.query(DailyWorkout).filter(
            DailyWorkout.resolution_id == resolution_id,
            DailyWorkout.date >= week_ago,
            DailyWorkout.actual_completed == True
        ).all()
        
        # Calculate current weekly volume
        current_volume = sum([w.actual_duration_minutes or w.planned_duration_minutes or 0 for w in weekly_workouts])
        total_volume = current_volume + proposed_workout_minutes
        
        # Count high-intensity sessions
        high_intensity_count = len([w for w in weekly_workouts if w.actual_intensity == "high" or w.planned_intensity == "high"])
        if proposed_intensity == "high":
            high_intensity_count += 1
        
        # Count recovery days
        recovery_days = len([w for w in weekly_workouts if w.planned_type in ["rest", "mobility", "yoga"]])
        
        # Check thresholds
        if total_volume >= self.WORKOUT_MINUTES_MAX_WEEKLY:
            alerts.append(SafetyAlert(
                level=AlertLevel.BLOCKED,
                category="overtraining",
                message=f"Overtraining risk: Weekly volume would reach {total_volume} minutes (max: {self.WORKOUT_MINUTES_MAX_WEEKLY}).",
                metric="weekly_volume",
                current_value=total_volume,
                threshold=self.WORKOUT_MINUTES_MAX_WEEKLY,
                action_required="Rest day recommended instead"
            ))
        elif total_volume >= self.WORKOUT_MINUTES_WARNING:
            alerts.append(SafetyAlert(
                level=AlertLevel.WARNING,
                category="overtraining",
                message=f"Caution: Weekly volume at {total_volume} minutes. Consider lighter activity.",
                metric="weekly_volume",
                current_value=total_volume,
                threshold=self.WORKOUT_MINUTES_WARNING,
                action_required="Consider rest or low-intensity day"
            ))
        
        if high_intensity_count > self.INTENSITY_HIGH_MAX_WEEKLY:
            alerts.append(SafetyAlert(
                level=AlertLevel.WARNING,
                category="overtraining",
                message=f"Too many high-intensity sessions: {high_intensity_count} (max: {self.INTENSITY_HIGH_MAX_WEEKLY})/week.",
                metric="high_intensity_count",
                current_value=high_intensity_count,
                threshold=self.INTENSITY_HIGH_MAX_WEEKLY,
                action_required="Reduce intensity or add recovery days"
            ))
        
        if recovery_days < self.RECOVERY_DAYS_MIN:
            alerts.append(SafetyAlert(
                level=AlertLevel.WARNING,
                category="overtraining",
                message=f"Not enough recovery days: {recovery_days} (need {self.RECOVERY_DAYS_MIN}+)/week.",
                metric="recovery_days",
                current_value=recovery_days,
                threshold=self.RECOVERY_DAYS_MIN,
                action_required="Add rest or light activity days"
            ))
        
        return alerts
    
    def check_medical_disclaimer_needed(
        self,
        recommendation_type: str,
        risk_level: str = "standard"
    ) -> Optional[str]:
        """
        Determine if medical disclaimer is needed for this recommendation.
        Returns disclaimer text if needed.
        """
        # Certain recommendation types always need disclaimer
        if recommendation_type in ["skip_workout", "recovery_focus", "reduce_intensity"]:
            return (
                "⚠️ MEDICAL DISCLAIMER: "
                "This recommendation is based on your reported data and is NOT medical advice. "
                "If you experience chest pain, severe shortness of breath, or other alarming symptoms, "
                "seek immediate medical attention. Always consult your doctor before making significant "
                "changes to your exercise routine or if you have health concerns."
            )
        
        return None
    
    def apply_all_checks(
        self,
        resolution_id: int,
        bp_systolic: Optional[int] = None,
        bp_diastolic: Optional[int] = None,
        resting_hr: Optional[int] = None,
        weight_kg: Optional[float] = None,
        recommendation_confidence: Optional[float] = None,
        recommendation_type: Optional[str] = None,
        proposed_workout_minutes: int = 0,
        proposed_intensity: str = "moderate"
    ) -> Dict:
        """
        Run all safety checks and compile results.
        Returns comprehensive safety report.
        """
        report = {
            "safe_to_proceed": True,
            "alerts": [],
            "critical_alerts": [],
            "warnings": [],
            "recommendations": [],
            "blocked_reason": None,
            "medical_disclaimer": None
        }
        
        # Check biometrics
        biometric_alerts = self.check_biometric_safety(
            resolution_id, bp_systolic, bp_diastolic, resting_hr, weight_kg
        )
        report["alerts"].extend(biometric_alerts)
        
        # Check confidence
        if recommendation_confidence is not None:
            safe, conf_alert = self.check_recommendation_confidence(recommendation_confidence)
            if not safe:
                report["safe_to_proceed"] = False
                report["blocked_reason"] = conf_alert.message
                report["alerts"].append(conf_alert)
            elif conf_alert:
                report["alerts"].append(conf_alert)
        
        # Check overtraining
        overtraining_alerts = self.check_overtraining_risk(
            resolution_id, proposed_workout_minutes, proposed_intensity
        )
        report["alerts"].extend(overtraining_alerts)
        
        # Add medical disclaimer if needed
        if recommendation_type:
            disclaimer = self.check_medical_disclaimer_needed(recommendation_type)
            if disclaimer:
                report["medical_disclaimer"] = disclaimer
        
        # Organize alerts by level
        for alert in report["alerts"]:
            if alert.level == AlertLevel.CRITICAL:
                report["critical_alerts"].append({
                    "message": alert.message,
                    "action": alert.action_required,
                    "category": alert.category,
                    "metric": alert.metric,
                    "value": alert.current_value
                })
                report["safe_to_proceed"] = False
            elif alert.level == AlertLevel.WARNING:
                report["warnings"].append({
                    "message": alert.message,
                    "action": alert.action_required,
                    "category": alert.category
                })
            elif alert.level == AlertLevel.BLOCKED:
                report["safe_to_proceed"] = False
                report["blocked_reason"] = alert.message
        
        return report
    
    def generate_safety_response(self, safety_report: Dict) -> Dict:
        """
        Generate user-friendly safety response for API.
        """
        response = {
            "cleared_for_activity": safety_report["safe_to_proceed"],
            "critical_alerts": safety_report["critical_alerts"],
            "warnings": safety_report["warnings"],
        }
        
        if safety_report["medical_disclaimer"]:
            response["disclaimer"] = safety_report["medical_disclaimer"]
        
        if not safety_report["safe_to_proceed"]:
            response["blocked_reason"] = safety_report["blocked_reason"]
            if safety_report["critical_alerts"]:
                response["urgent_action"] = "Seek medical attention for critical alerts"
        
        return response
