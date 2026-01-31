# models/workout.py

"""
Workout Models - Designed for multi-agent intelligence
"""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
from core.database import Base


# ============================================================================
# ENUMS - Standardized categories for agent reasoning
# ============================================================================

class ExerciseCategory(str, Enum):
    """Exercise type - helps agents understand movement patterns"""
    COMPOUND_PUSH = "compound_push"           # Bench, overhead press
    COMPOUND_PULL = "compound_pull"           # Deadlift, rows, pull-ups
    SQUAT_PATTERN = "squat_pattern"           # Squats, lunges
    HINGE_PATTERN = "hinge_pattern"           # Deadlifts, RDLs
    ISOLATION_UPPER = "isolation_upper"       # Bicep curls, tricep extensions
    ISOLATION_LOWER = "isolation_lower"       # Leg curls, calf raises
    CORE = "core"                             # Planks, ab work
    CARDIO_STEADY = "cardio_steady"           # Running, cycling
    CARDIO_HIIT = "cardio_hiit"               # Sprints, intervals
    MOBILITY = "mobility"                     # Stretching, yoga
    PLYOMETRIC = "plyometric"                 # Box jumps, explosive work


class IntensityZone(str, Enum):
    """Intensity level - for auto-adjustment by agents"""
    RECOVERY = "recovery"           # 50-60% effort, active recovery
    ENDURANCE = "endurance"         # 60-70% effort, high volume
    TEMPO = "tempo"                 # 70-80% effort, controlled pace
    THRESHOLD = "threshold"         # 80-90% effort, lactate threshold
    VO2MAX = "vo2max"              # 90-95% effort, max aerobic
    ANAEROBIC = "anaerobic"        # 95-100% effort, all-out


class ExerciseRiskLevel(str, Enum):
    """Risk classification - injury prevention agent uses this"""
    LOW = "low"                # Machine work, bodyweight
    MODERATE = "moderate"      # Dumbbells, controlled movements
    HIGH = "high"              # Heavy barbell, complex movements
    ADVANCED_ONLY = "advanced" # Olympic lifts, max effort


# ============================================================================
# PYDANTIC SCHEMAS - For API and agent communication
# ============================================================================

class ExerciseModification(BaseModel):
    """
    When an agent modifies an exercise, it creates this
    Tracks WHY something was changed (for transparency)
    """
    original_exercise: str
    modified_exercise: str
    reason: str
    agent_name: str
    confidence: float = Field(ge=0, le=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Exercise(BaseModel):
    """
    Single exercise - the atomic unit of a workout
    Rich metadata enables intelligent agent reasoning
    """
    # Basic info
    name: str = Field(..., description="Exercise name (standardized)")
    category: ExerciseCategory
    risk_level: ExerciseRiskLevel
    
    # Load parameters
    sets: int = Field(ge=1, le=10)
    reps: Optional[int] = Field(None, ge=1, le=100)  # None for AMRAP or timed
    weight_lbs: Optional[float] = Field(None, ge=0)  # None for bodyweight
    duration_seconds: Optional[int] = Field(None)    # For timed exercises (planks, cardio)
    distance_meters: Optional[int] = Field(None)     # For running, rowing
    
    # Intensity control
    intensity_zone: Optional[IntensityZone] = None
    rpe: Optional[int] = Field(None, ge=1, le=10)   # Rate of Perceived Exertion (1-10)
    percentage_1rm: Optional[float] = Field(None, ge=0, le=100)  # % of 1 rep max
    
    # Rest and tempo
    rest_seconds: int = Field(default=60, ge=0, le=600)
    tempo: Optional[str] = Field(None, description="e.g., '3-1-1-0' (eccentric-pause-concentric-pause)")
    
    # Movement quality markers (agents track these)
    target_muscle_groups: List[str] = Field(default_factory=list)
    joint_stress_areas: List[str] = Field(default_factory=list, description="Joints under load: shoulder, knee, etc.")
    
    # Adaptability metadata
    can_superset_with: Optional[str] = None
    alternatives: List[str] = Field(default_factory=list, description="Easier/harder variations")
    equipment_needed: List[str] = Field(default_factory=list)
    
    # Agent modifications
    modifications: List[ExerciseModification] = Field(default_factory=list)
    modified_by_agent: bool = False
    
    # Notes
    cues: Optional[str] = Field(None, description="Form cues for user")
    notes: Optional[str] = None


class WorkoutBlock(BaseModel):
    """
    A logical section of a workout (e.g., Warm-up, Main Lift, Accessory, Cooldown)
    Agents can modify entire blocks
    """
    name: str  # "Warm-up", "Strength Block", "HIIT Finisher", "Cooldown"
    description: Optional[str] = None
    exercises: List[Exercise]
    
    # Block-level metadata
    estimated_duration_minutes: int
    required_equipment: List[str] = Field(default_factory=list)
    
    # Adaptation metadata
    can_skip_if_tired: bool = False
    priority_level: int = Field(default=5, ge=1, le=10)  # 10 = must do, 1 = optional


class WorkoutPlan(BaseModel):
    """
    Complete workout session
    This is what agents modify, debate, and track
    """
    # Identifiers
    workout_id: Optional[str] = None
    user_id: int
    session_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Workout structure
    name: str  # "Full Body A", "Upper Power", "HIIT Cardio"
    workout_type: str  # "strength", "cardio", "hybrid", "recovery"
    blocks: List[WorkoutBlock]
    
    # Session metadata
    total_estimated_duration_minutes: int
    difficulty_level: int = Field(ge=1, le=10)  # 1 = easy recovery, 10 = brutal
    
    # Context for agents
    user_readiness_score: Optional[float] = Field(None, ge=0, le=1, description="0=exhausted, 1=fully recovered")
    environmental_factors: Dict[str, Any] = Field(default_factory=dict)  # weather, gym crowding, etc.
    
    # Agent interaction tracking
    generated_by: str = Field(default="system")
    reviewed_by_agents: List[str] = Field(default_factory=list)
    modifications_history: List[Dict[str, Any]] = Field(default_factory=list)
    agent_debate_summary: Optional[str] = None
    
    # Safety and compliance
    risk_assessment: Optional[str] = None
    contraindications: List[str] = Field(default_factory=list)
    approved_for_execution: bool = False


# ============================================================================
# DATABASE MODELS - For persistence
# ============================================================================

class WorkoutSession(Base):
    """
    Actual workout session in database
    """
    __tablename__ = "workout_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Plan data (stored as JSON for flexibility)
    workout_plan = Column(JSON, nullable=False)  # Serialized WorkoutPlan
    
    # Execution tracking
    scheduled_date = Column(DateTime, nullable=False)
    completed_date = Column(DateTime, nullable=True)
    actual_duration_minutes = Column(Integer, nullable=True)
    
    # Performance
    completion_percentage = Column(Float, default=0.0)  # 0.0 to 1.0
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
    user_notes = Column(String, nullable=True)
    
    # Agent metadata
    generated_by_agent = Column(String, nullable=True)
    modifications_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="workout_sessions")




class WorkoutModificationResponse(BaseModel):
    """Response from workout modification"""
    modified: bool
    modified_workout: List[Dict[str, Any]]
    modifications: List[str]
    risk_assessment: Dict[str, Any]
    safety_score: float
    confidence: float
    reasoning: str
    knowledge_sources: List[str]
    agent_name: str



class ExerciseInput(BaseModel):
    """Single exercise in workout plan"""
    name: str
    sets: int = Field(ge=1, le=10)
    reps: int = Field(ge=1, le=100)
    weight_lbs: float = Field(default=0, ge=0)
    rest_seconds: int = Field(default=60, ge=0)
    notes: str = Field(default="")


class WorkoutModificationRequest(BaseModel):
    """Request body for workout modification"""
    workout_plan: List[ExerciseInput]
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional context: sleep_hours, stress_level, days_since_last_workout"
    )


class ModificationDetail(BaseModel):
    """Single modification made by agent"""
    original_exercise: str
    modified_exercise: str
    reason: str
    confidence: float

