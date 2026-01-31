"""
WeeklyPlan Model
Represents one week (7 days) within a quarterly phase
Tracks planned workouts and adherence
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from models.user import Base
import enum


class WeeklyStatus(str, enum.Enum):
    """Status of a week"""
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    UPCOMING = "upcoming"
    SKIPPED = "skipped"


class WeeklyPlan(Base):
    """
    Week-level breakdown (7 days)
    
    Example Week 17 (Q2: Progression):
    - Mon: Easy Run, 3 miles, 30 min
    - Wed: Strength, 25 min
    - Thu: Tempo Run, 2.5 miles, 22 min
    - Sat: Long Run, 3.5 miles, 35 min
    - Total: 4 workouts, 112 minutes
    """
    __tablename__ = "weekly_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    quarterly_phase_id = Column(Integer, ForeignKey("quarterly_phases.id"), nullable=False, index=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id"), nullable=False, index=True)
    
    # Week identifier
    week_number = Column(Integer, nullable=False)  # 1-52 across entire year
    quarter_week = Column(Integer, nullable=False)  # 1-13 within quarter
    week_start_date = Column(DateTime, nullable=False)  # Monday of week
    week_end_date = Column(DateTime, nullable=False)   # Sunday of week
    
    # Weekly targets
    target_workouts = Column(Integer, nullable=False)  # e.g., 3 or 4
    target_duration_minutes = Column(Integer, nullable=False)  # Total minutes for week
    focus = Column(String(100), nullable=True)  # "Foundation", "Speed Work", "Long Runs"
    
    # Weekly metrics (from agents)
    estimated_difficulty = Column(String(20), nullable=False)  # "easy", "moderate", "hard"
    intensity_progression = Column(String(100), nullable=True)  # "Increase from 70% to 75% effort"
    
    # Risk assessments (from Failure Pattern Agent)
    risk_level = Column(String(20), nullable=False)  # "low", "medium", "high"
    critical_week = Column(String(255), nullable=True)  # "Week 3 cliff", "Week 7 plateau", None
    
    # Protective strategies (what to do if risk detected)
    protective_measures = Column(JSON, nullable=False)  # ["extra_accountability_check", "variation"]
    
    # Progress tracking
    workouts_completed = Column(Integer, default=0, nullable=False)
    workouts_planned = Column(Integer, default=0, nullable=False)
    adherence_rate = Column(Float, default=0.0, nullable=False)  # 0.0 to 1.0
    total_minutes_completed = Column(Integer, default=0, nullable=False)
    
    # User feedback (after week completes)
    user_feedback = Column(JSON, nullable=True)  # {"energy_level": "good", "mood": "positive", "notes": "..."}
    
    # Agent reasoning (why this week is structured this way)
    agent_reasoning = Column(JSON, nullable=True)  # {
    #   "meta_coordinator": "Balanced intensity, building consistency",
    #   "progress_tracking": "On pace for year-end goal",
    #   "failure_pattern": "Watch for motivation cliff this week"
    # }
    
    # Status
    status = Column(SQLEnum(WeeklyStatus), default=WeeklyStatus.UPCOMING, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    resolution = relationship("Resolution", backref="weekly_plans")
    quarterly_phase = relationship("QuarterlyPhase", back_populates="weekly_plans")
    daily_workouts = relationship("DailyWorkout", back_populates="weekly_plan", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "quarterly_phase_id": self.quarterly_phase_id,
            "week_number": self.week_number,
            "quarter_week": self.quarter_week,
            "week_start_date": self.week_start_date.isoformat() if self.week_start_date else None,
            "target_workouts": self.target_workouts,
            "target_duration_minutes": self.target_duration_minutes,
            "focus": self.focus,
            "workouts_completed": self.workouts_completed,
            "workouts_planned": self.workouts_planned,
            "adherence_rate": self.adherence_rate,
            "status": self.status.value,
            "risk_level": self.risk_level,
            "critical_week": self.critical_week,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    @property
    def completion_percentage(self) -> float:
        """Calculate week completion percentage"""
        if self.target_workouts == 0:
            return 0.0
        return (self.workouts_completed / self.target_workouts) * 100
    
    @property
    def remaining_workouts(self) -> int:
        """Get remaining workouts for week"""
        return max(0, self.target_workouts - self.workouts_completed)
