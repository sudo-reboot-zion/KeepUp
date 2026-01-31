"""
DailyWorkout Model
Represents a single day's workout within a weekly plan
Tracks execution, modifications, and agent reasoning
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from models.user import Base
import enum


class WorkoutStatus(str, enum.Enum):
    """Status of a daily workout"""
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    SCHEDULED = "scheduled"
    SKIPPED = "skipped"
    FAILED = "failed"  # Started but didn't complete


class DayOfWeek(str, enum.Enum):
    """Day of week"""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class DailyWorkout(Base):
    """
    Single day's workout
    
    Example (Thursday, Week 17):
    - Original plan: Tempo Run, 2.5 miles, 22 min @ 8:45/mi
    - Modifications: Sleep 6.5h, stress moderate
    - Modified plan: Tempo Run, 2.5 miles @ 8:45/mi but SHORT tempo (8 min vs 15 min)
    - Actual result: 2.5 miles, 22 min, RPE 7/10
    """
    __tablename__ = "daily_workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    weekly_plan_id = Column(Integer, ForeignKey("weekly_plans.id"), nullable=False, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id"), nullable=False, index=True)
    
    # Date & day info
    date = Column(DateTime, nullable=False, index=True)
    day_of_week = Column(SQLEnum(DayOfWeek), nullable=False)
    
    # Planned workout (from Task Generation Agent)
    planned_workout_type = Column(String(50), nullable=False)  # "easy_run", "tempo_run", "strength", "mobility"
    planned_duration_minutes = Column(Integer, nullable=False)
    planned_exercises = Column(JSON, nullable=False)  # Array of exercises
    # Example: [
    #   {"name": "Tempo Run", "distance": 2.5, "pace": "8:45/mi", "duration": 22}
    # ]
    
    # Original difficulty/intensity
    planned_intensity = Column(String(20), nullable=False)  # "easy", "moderate", "hard", "threshold"
    planned_target = Column(String(255), nullable=True)  # "8:45/mi pace", "Build lactate threshold"
    
    # Context at time of workout (from daily check-in)
    context = Column(JSON, nullable=True)  # {
    #   "sleep_hours": 6.5,
    #   "sleep_quality": "poor",
    #   "energy_level": "low",
    #   "stress_level": 4,
    #   "soreness_level": 2,
    #   "mood": "neutral"
    # }
    
    # MODIFICATIONS (from Workout Modification Agent)
    was_modified = Column(Boolean, default=False, nullable=False)
    modification_reason = Column(String(255), nullable=True)  # "Sleep low, stress moderate"
    
    modified_workout_type = Column(String(50), nullable=True)  # Null if not modified
    modified_duration_minutes = Column(Integer, nullable=True)
    modified_exercises = Column(JSON, nullable=True)  # Changed exercises
    modified_intensity = Column(String(20), nullable=True)  # "easy" (downgraded from "moderate")
    modification_rationale = Column(String(500), nullable=True)  # "Keep tempo SHORT (8min) due to sleep, not quality"
    
    # Agent reasoning (transparency)
    agent_modifications = Column(JSON, nullable=True)  # {
    #   "agent": "Workout Modification Agent",
    #   "reason": "Sleep 6.5h, stress moderate, recovery day yesterday",
    #   "changes": ["Reduce tempo from 15min to 8min"],
    #   "confidence": 0.85
    # }
    
    # Actual execution
    status = Column(SQLEnum(WorkoutStatus), default=WorkoutStatus.SCHEDULED, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    # What actually happened
    actual_duration_minutes = Column(Integer, nullable=True)
    actual_exercises = Column(JSON, nullable=True)  # What was actually done
    actual_intensity_perceived = Column(String(20), nullable=True)  # "RPE 7/10"
    
    # User feedback after workout
    user_feedback = Column(JSON, nullable=True)  # {
    #   "how_felt": "great",
    #   "rpe": 7,
    #   "energy_level": "high",
    #   "difficulty": "moderate",
    #   "would_repeat": true,
    #   "notes": "Felt strong, will increase next week"
    # }
    
    # Progress notes
    notes = Column(String(500), nullable=True)  # Free-form notes
    
    # Relationships
    resolution = relationship("Resolution", backref="daily_workouts")
    weekly_plan = relationship("WeeklyPlan", back_populates="daily_workouts")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "weekly_plan_id": self.weekly_plan_id,
            "date": self.date.isoformat() if self.date else None,
            "day_of_week": self.day_of_week.value if self.day_of_week else None,
            "planned_workout_type": self.planned_workout_type,
            "planned_duration_minutes": self.planned_duration_minutes,
            "planned_intensity": self.planned_intensity,
            "was_modified": self.was_modified,
            "modified_intensity": self.modified_intensity,
            "status": self.status.value,
            "actual_duration_minutes": self.actual_duration_minutes,
            "user_feedback": self.user_feedback,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    @property
    def intensity_change(self) -> str:
        """Return intensity change summary"""
        if not self.was_modified:
            return "No modification"
        return f"Downgraded from {self.planned_intensity} to {self.modified_intensity}"
