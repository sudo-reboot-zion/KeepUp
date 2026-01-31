from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# BaselineMetrics Schemas
class BaselineMetricsCreate(BaseModel):
    """Create baseline metrics for a resolution"""
    bp_systolic_baseline: Optional[int] = None
    bp_diastolic_baseline: Optional[int] = None
    resting_hr_baseline: Optional[int] = None
    weight_baseline_kg: Optional[float] = None
    waist_circumference_cm: Optional[float] = None
    avg_sleep_hours_baseline: Optional[float] = None
    avg_stress_level_baseline: Optional[int] = None
    
    # Goals/targets
    bp_systolic_target: Optional[int] = None
    bp_diastolic_target: Optional[int] = None
    weight_target_kg: Optional[float] = None
    resting_hr_target: Optional[int] = None


class BaselineMetricsResponse(BaseModel):
    """Response for baseline metrics"""
    id: int
    resolution_id: int
    bp_systolic_baseline: Optional[int]
    bp_diastolic_baseline: Optional[int]
    resting_hr_baseline: Optional[int]
    weight_baseline_kg: Optional[float]
    waist_circumference_cm: Optional[float]
    avg_sleep_hours_baseline: Optional[float]
    avg_stress_level_baseline: Optional[int]
    bp_systolic_target: Optional[int]
    bp_diastolic_target: Optional[int]
    weight_target_kg: Optional[float]
    resting_hr_target: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# DailyCheckIn Schemas
class DailyCheckInCreate(BaseModel):
    """Submit daily health check-in"""
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = Field(None, ge=1, le=10)
    stress_level: Optional[int] = Field(None, ge=1, le=10)
    mood: Optional[str] = None
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    symptoms: Optional[str] = None
    notes: Optional[str] = None
    ready_for_workout: Optional[str] = None  # "yes", "partial", "no"


class DailyCheckInResponse(BaseModel):
    """Response for daily check-in"""
    id: int
    resolution_id: int
    user_id: int
    sleep_hours: Optional[float]
    sleep_quality: Optional[int]
    stress_level: Optional[int]
    mood: Optional[str]
    energy_level: Optional[int]
    symptoms: Optional[str]
    notes: Optional[str]
    ready_for_workout: Optional[str]
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# BiometricReading Schemas
class BiometricReadingCreate(BaseModel):
    """Submit biometric measurement"""
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    resting_hr: Optional[int] = None
    weight_kg: Optional[float] = None
    waist_circumference_cm: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    time_of_day: Optional[str] = None  # "morning", "afternoon", "evening"
    context_notes: Optional[str] = None
    source: Optional[str] = None  # "manual", "apple_watch", "fitbit", etc


class BiometricReadingResponse(BaseModel):
    """Response for biometric reading"""
    id: int
    resolution_id: int
    user_id: int
    bp_systolic: Optional[int]
    bp_diastolic: Optional[int]
    resting_hr: Optional[int]
    weight_kg: Optional[float]
    waist_circumference_cm: Optional[float]
    body_fat_percentage: Optional[float]
    time_of_day: Optional[str]
    context_notes: Optional[str]
    source: Optional[str]
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# NutritionEntry Schemas
class NutritionEntryCreate(BaseModel):
    """Log nutrition entry"""
    quality_rating: Optional[int] = Field(None, ge=1, le=10)
    quality_category: Optional[str] = None  # "poor", "fair", "good", "excellent"
    calories: Optional[int] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    fiber_g: Optional[float] = None
    meal_type: Optional[str] = None
    foods: Optional[str] = None
    notes: Optional[str] = None
    on_track: Optional[str] = None  # "yes", "no", "partial"


class NutritionEntryResponse(BaseModel):
    """Response for nutrition entry"""
    id: int
    resolution_id: int
    user_id: int
    quality_rating: Optional[int]
    quality_category: Optional[str]
    calories: Optional[int]
    protein_g: Optional[float]
    carbs_g: Optional[float]
    fat_g: Optional[float]
    fiber_g: Optional[float]
    meal_type: Optional[str]
    foods: Optional[str]
    notes: Optional[str]
    on_track: Optional[str]
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# WeeklyBiometrics Schemas
class WeeklyBiometricsResponse(BaseModel):
    """Response for weekly aggregated biometrics"""
    id: int
    resolution_id: int
    week_number: int
    year: int
    avg_bp_systolic: Optional[int]
    avg_bp_diastolic: Optional[int]
    min_bp_systolic: Optional[int]
    max_bp_systolic: Optional[int]
    avg_resting_hr: Optional[int]
    avg_weight_kg: Optional[float]
    weight_change_from_baseline: Optional[float]
    avg_waist_circumference_cm: Optional[float]
    bp_reading_count: int
    weight_reading_count: int
    trend_direction: Optional[str]
    trend_strength: Optional[str]
    week_start_date: datetime
    week_end_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# AgentRecommendation Schemas
class AgentRecommendationCreate(BaseModel):
    """Agent recommendation (typically generated by backend)"""
    recommendation_type: str
    recommendation_text: str
    reasoning: str
    agent_name: str
    agent_type: Optional[str] = None
    confidence_score: float = 0.5
    supporting_factors: Optional[str] = None
    opik_trace_id: Optional[str] = None
    recommended_workout_type: Optional[str] = None
    recommended_duration_minutes: Optional[int] = None
    recommended_intensity: Optional[str] = None


class AgentRecommendationResponse(BaseModel):
    """Response for agent recommendation"""
    id: int
    resolution_id: int
    daily_checkin_id: Optional[int]
    recommendation_type: str
    recommendation_text: str
    reasoning: str
    agent_name: str
    agent_type: Optional[str]
    confidence_score: float
    supporting_factors: Optional[str]
    opik_trace_id: Optional[str]
    recommended_workout_type: Optional[str]
    recommended_duration_minutes: Optional[int]
    recommended_intensity: Optional[str]
    user_accepted: Optional[bool]
    user_feedback: Optional[str]
    outcome_notes: Optional[str]
    effectiveness_rating: Optional[int]
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# AgentDecision Schemas
class AgentDecisionCreate(BaseModel):
    """Log agent decision (internal use)"""
    decision_type: str
    agent_name: str
    input_context: dict
    reasoning_chain: str
    decision_output: str
    confidence_score: float
    decision_certainty: Optional[str] = None
    safety_check_passed: str = "yes"
    safety_warnings: Optional[str] = None
    opik_trace_id: Optional[str] = None
    opik_experiment_name: Optional[str] = None
    opik_run_name: Optional[str] = None
    tags: Optional[list] = None
    decision_metadata: Optional[dict] = None


class AgentDecisionResponse(BaseModel):
    """Response for agent decision"""
    id: int
    resolution_id: int
    decision_type: str
    agent_name: str
    input_context: dict
    reasoning_chain: str
    decision_output: str
    confidence_score: float
    decision_certainty: Optional[str]
    safety_check_passed: str
    safety_warnings: Optional[str]
    opik_trace_id: Optional[str]
    opik_experiment_name: Optional[str]
    opik_run_name: Optional[str]
    user_feedback: Optional[str]
    outcome_success: Optional[str]
    tags: Optional[list]
    decision_metadata: Optional[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True


# GoalProgress Schemas
class GoalProgressResponse(BaseModel):
    """Response for goal progress tracking"""
    id: int
    resolution_id: int
    metric_type: str
    metric_unit: str
    baseline_value: float
    target_value: float
    current_value: Optional[float]
    days_elapsed: int
    value_change: Optional[float]
    percentage_progress: Optional[float]
    trend_direction: Optional[str]
    trend_strength: Optional[str]
    days_to_goal_estimate: Optional[int]
    contributing_factors: Optional[str]
    insight_text: Optional[str]
    last_measurement_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Composite Schemas
class ResolutionHealthStatus(BaseModel):
    """Complete health status for a resolution"""
    resolution_id: int
    baseline_metrics: Optional[BaselineMetricsResponse]
    latest_daily_checkin: Optional[DailyCheckInResponse]
    latest_biometric_reading: Optional[BiometricReadingResponse]
    latest_nutrition_entry: Optional[NutritionEntryResponse]
    latest_recommendation: Optional[AgentRecommendationResponse]
    goal_progress: Optional[List[GoalProgressResponse]]
    weekly_biometrics: Optional[List[WeeklyBiometricsResponse]]
    
    class Config:
        from_attributes = True


class WeeklyAnalysis(BaseModel):
    """Analysis of a week's data"""
    week_number: int
    avg_sleep_hours: Optional[float]
    avg_stress_level: Optional[float]
    nutrition_quality_avg: Optional[float]
    workouts_completed: int
    workouts_target: int
    biometric_changes: dict  # {"bp": -5, "weight": -0.5, "hr": -2}
    trend: str  # "improving", "stable", "declining"
    contributing_factors: List[str]  # ["increased_sleep", "consistent_workouts", "better_nutrition"]
    agent_insight: str  # Human-readable insight
    recommendations: List[str]  # Top 3 recommendations
